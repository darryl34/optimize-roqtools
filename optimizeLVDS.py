import os
from bayes_opt import BayesianOptimization, UtilityFunction

from util import editLVDSNetlist, extractLVDS, penaltyFunc, runCmd


def runLVDS(filename, params):
    editLVDSNetlist(filename, **params)
    data = runCmd().splitlines()[1:]
    return extractLVDS(data)


def optimize(filename, bounds, VOH, VOL):
    # optimizer object initialization
    optimizer = BayesianOptimization(
        f=None,
        pbounds=bounds,
        allow_duplicate_points=True
    )

    # define acquisition function
    utility = UtilityFunction(kind="ucb", kappa=3)

    for _ in range(10):
        next_point = optimizer.suggest(utility)
        lvdsDict = runLVDS(filename, next_point)
        
        # calculate output errors
        target = penaltyFunc(lvdsDict["Output DOUTP"], VOH, -20)
        target += penaltyFunc(lvdsDict["Output DOUTN"], VOL, -20)
        target += penaltyFunc(lvdsDict["Output delta"], VOH-VOL, -10)
        optimizer.register(next_point, target)

    # print("Current best: " + str(optimizer.max['target']))
    return optimizer.max


# main optimization function
def run(filename, bounds, idealValues):
    res = []
    errorThreshold = -0.1  # must be < 0

    for i in range(5):
        print("Calibrating... Iteration " + str(i+1) + "/5", end="\r", flush=True)
        curr = optimize(filename, bounds, **idealValues)
        res.append(curr)
        if curr['target'] > errorThreshold:
            break
    
    # return element with target closest to 0
    res.sort(key=lambda x: x['target'], reverse=True)
    editLVDSNetlist(filename, **res[0]['params'])

    print("\nOptimized parameters: " + str(res[0]))
    print("Running cmd...\n")
    print(runCmd())


if __name__ == "__main__":

    bounds = {'MPD1_W': (1e-6,1e-3),
            'MND1_W': (1e-6,1e-3),
            'P_KP': (1e-6,1e-3),
            'P_RD': (1,300),
            'P_RS': (1,300),
            'N_KP': (1e-6,1e-3),
            'N_RD': (1,300),
            'N_RS': (1,300)}
    
    idealValues = {"VOH": 1.6, 
                   "VOL": 1.15}

    run("1822-4877.inc", bounds, idealValues)
