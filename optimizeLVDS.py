import os
from bayes_opt import BayesianOptimization, SequentialDomainReductionTransformer, UtilityFunction

from util import editLVDSNetlist, extractLVDS, penaltyFunc, runCmd


def runLVDS(filename, params):
    editLVDSNetlist(filename, **params)
    data = runCmd().splitlines()[1:]
    return extractLVDS(data)


def optimizeDelta(filename, bounds, VOH, VOL):
    optimizer = BayesianOptimization(
        f=None,
        pbounds=bounds,
        allow_duplicate_points=True,
        bounds_transformer=SequentialDomainReductionTransformer()
    )

    # define acquisition function
    utility = UtilityFunction(kind="ucb", kappa=5)

    for _ in range(30):
        next_point = optimizer.suggest(utility)
        lvdsDict = runLVDS(filename, next_point)
        
        # calculate output errors
        target = penaltyFunc(lvdsDict["Output delta"], VOH-VOL, -20)
        optimizer.register(next_point, target)

    print(optimizer.max)
    editLVDSNetlist(filename, **optimizer.max['params'])
    return optimizer.max


def optimizeV(filename, bounds, VOH, VOL):
    optimizer = BayesianOptimization(
        f=None,
        pbounds=bounds,
        allow_duplicate_points=True,
        bounds_transformer=SequentialDomainReductionTransformer()
    )

    # define acquisition function
    utility = UtilityFunction(kind="ucb", kappa=5)

    for _ in range(30):
        next_point = optimizer.suggest(utility)
        lvdsDict = runLVDS(filename, next_point)
        
        # calculate output errors
        target = penaltyFunc(lvdsDict["Output DOUTP"], VOH, -20)
        target += penaltyFunc(lvdsDict["Output DOUTN"], VOL, -20)
        optimizer.register(next_point, target)

    print(optimizer.max)
    editLVDSNetlist(filename, **optimizer.max['params'])
    return optimizer.max


def run(filename, boundsDelta, boundsV, idealValues):
    res = []
    errorThreshold = -0.1  # must be < 0

    for i in range(3):
        print("Calibrating... Iteration " + str(i+1) + "/3", end="\r", flush=True)
        delta = optimizeDelta(filename, boundsDelta, **idealValues)
        v = optimizeV(filename, boundsV, **idealValues)
        curr = {'params': {**delta['params'], **v['params']}, 'target': delta['target'] + v['target']}
        res.append(curr)
        if curr['target'] > errorThreshold: break
    
    # return element with target closest to 0
    res.sort(key=lambda x: x['target'], reverse=True)
    editLVDSNetlist(filename, **res[0]['params'])

    print("\nParameters optimized. Running cmd...\n")
    print(runCmd())


def run_with_params(filename: str, 
                    MPD1_L: float, MPD1_H: float,
                    MND1_L: float, MND1_H: float,
                    P_KP_L: float, P_KP_H: float,
                    P_RD_L: float, P_RD_H: float,
                    P_RS_L: float, P_RS_H: float,
                    N_KP_L: float, N_KP_H: float,
                    N_RD_L: float, N_RD_H: float,
                    N_RS_L: float, N_RS_H: float,
                    VOH: float, VOL: float):
    
    boundsDelta = {'MPD1_W': (MPD1_L, MPD1_H),
                   'MND1_W': (MND1_L, MND1_H)}
    
    boundsV = {'P_KP': (P_KP_L, P_KP_H),
               'P_RD': (P_RD_L, P_RD_H),
               'P_RS': (P_RS_L, P_RS_H),
               'N_KP': (N_KP_L, N_KP_H),
               'N_RD': (N_RD_L, N_RD_H),
               'N_RS': (N_RS_L, N_RS_H)}
    
    idealValues = {"VOH": VOH, 
                   "VOL": VOL}
    
    run(filename, boundsDelta, boundsV, idealValues)


if __name__ == "__main__":

    boundsDelta = {'MPD1_W': (1e-6,1e-3),
                   'MND1_W': (1e-6,1e-3)}
    
    boundsV = {'P_KP': (1e-5,10e-3),
               'P_RD': (1,50),
               'P_RS': (1,50),
               'N_KP': (1e-5,10e-3),
               'N_RD': (1,50),
               'N_RS': (1,50)}
    
    idealValues = {"VOH": 1.41, 
                   "VOL": 1.05}
    os.chdir("1822-2408")
    run("1822-2408.inc", boundsDelta, boundsV, idealValues)
