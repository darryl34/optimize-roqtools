import os
from bayes_opt import BayesianOptimization, SequentialDomainReductionTransformer, UtilityFunction
from util import extractECL, editECLNetlist, penaltyFunc, runCmd


def runECL(filename, RB1=None, RB2=None):
    editECLNetlist(filename, RB1, RB2)
    data = runCmd().splitlines()[1:]
    return extractECL(data)


def optimizeVOH(filename, bounds, VOH):
    optimizer = BayesianOptimization(
        f=None,
        pbounds=bounds,
        allow_duplicate_points=True,
        bounds_transformer=SequentialDomainReductionTransformer()
    )

    utility = UtilityFunction(kind="ucb", kappa=5)

    for _ in range(25):
        next_point = optimizer.suggest(utility)
        eclDict = runECL(filename, **next_point)
        target = penaltyFunc(eclDict["Output VOH"], VOH, -30)
        optimizer.register(next_point, target)
    
    print(optimizer.max)
    editECLNetlist(filename, **optimizer.max['params'])
    return optimizer.max


def optimizeVOL(filename, bounds, VOL):
    optimizer = BayesianOptimization(
        f=None,
        pbounds=bounds,
        allow_duplicate_points=True,
        bounds_transformer=SequentialDomainReductionTransformer()
    )

    utility = UtilityFunction(kind="ucb", kappa=5)

    for _ in range(25):
        next_point = optimizer.suggest(utility)
        eclDict = runECL(filename, **next_point)
        target = penaltyFunc(eclDict["Output VOL"], VOL, -30)
        optimizer.register(next_point, target)
    
    print(optimizer.max)
    editECLNetlist(filename, **optimizer.max['params'])
    return optimizer.max

def run(filename, boundsVOH, boundsVOL, idealValues):
    """
    Optimize the parameters of a model file by running a calibration process
    on VOH and VOL outputs sequentially. The best result is then selected and
    the model file is edited to reflect the optimized parameters.

    Args:
        filename (str): The name of the model file.
        boundsVOL (dict): A dictionary specifying the bounds for the VOL parameters.
        boundsVOH (dict): A dictionary specifying the bounds for the VOH parameters.
        idealValues (dict): A dictionary specifying the ideal VOL and VOH values.

    Returns:
        None

    Example Usage:
        filename = "kpn.inc"

        boundsVOL = {"RB1": (1, 1000)}

        boundsVOH = {"RB1": (1, 1000)}
        
        idealValues = {"VOL": 0.1, "VOH": 0.9}

        run(filename, boundsVOL, boundsVOH, idealValues)
    """
    res = []
    optThreshold = -1e-4

    for i in range(2):
        print("Calibrating... Iteration " + str(i+1) + "/2")
        voh = optimizeVOH(filename, boundsVOH, idealValues["VOH"])
        vol = optimizeVOL(filename, boundsVOL, idealValues["VOL"])
        curr = {'target': voh['target'] + vol['target'], 'params': {**voh['params'], **vol['params']}}
        res.append(curr)
        if curr['target'] > optThreshold: break

    # return element with target closest to 0
    res.sort(key=lambda x: x['target'], reverse=True)
    editECLNetlist(filename, **res[0]['params'])

    print("\nParameters optimized. Running cmd...\n")
    print(runCmd())


def run_with_params(filename: str, RB1_L: int, RB1_R: int,
                     RB2_L: int, RB2_R: int, VOH: float, VOL: float):
        run(filename, {"RB1": (RB1_L, RB1_R)},
                      {"RB2": (RB2_L, RB2_R)},
                      {"VOH": VOH, "VOL": VOL})

if __name__ == "__main__":

    boundsVOH = {"RB1": (1, 1000)}
    boundsVOL = {"RB2": (1, 1000)}
    
    idealValues = {"VOH": 2.32,
                    "VOL": 1.5}
    
    run("1822-2408.inc", boundsVOH, boundsVOL, idealValues)
