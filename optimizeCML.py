import os
from bayes_opt import BayesianOptimization, SequentialDomainReductionTransformer, UtilityFunction

from util import extractCML, editCMLNetlist, penaltyFunc, runCmd

def runCML(filename, R1=None, R2=None, R3=None, R4=None, BF=None, RC=None, RE=None, RB=None):
    editCMLNetlist(filename, R1, R2, R3, R4, BF, RC, RE, RB)
    data = runCmd().splitlines()[1:]
    return extractCML(data)

def optimizeVOL(filename, bounds, VOL):
    optimizer = BayesianOptimization(
        f=None,
        pbounds=bounds,
        allow_duplicate_points=True,
        bounds_transformer=SequentialDomainReductionTransformer()
    )

    # define acquisition function
    utility = UtilityFunction(kind="ucb", kappa=5)

    for _ in range(15):
        next_point = optimizer.suggest(utility)
        cmlDict = runCML(filename, **next_point)
        target = penaltyFunc(cmlDict["Output VOL"], VOL, -10)
        optimizer.register(next_point, target)

    print(optimizer.max)
    editCMLNetlist(filename, **optimizer.max['params'])
    return optimizer.max


def optimizeVOH(filename, bounds, VOH):
    optimizer = BayesianOptimization(
        f=None,
        pbounds=bounds,
        allow_duplicate_points=True,
        bounds_transformer=SequentialDomainReductionTransformer()
    )

    utility = UtilityFunction(kind="ucb", kappa=5)

    for _ in range(15):
        next_point = optimizer.suggest(utility)
        cmlDict = runCML(filename, **next_point)
        target = penaltyFunc(cmlDict["Output VOH"], VOH, -10)
        optimizer.register(next_point, target)

    print(optimizer.max)
    editCMLNetlist(filename, **optimizer.max['params'])
    return optimizer.max

def run(filename, boundsVOL, boundsVOH, idealValues):
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
        
        boundsVOL = {"R1": (1, 10), "R2": (1, 10)}
        
        boundsVOH = {"R3": (1, 10), "R4": (1, 10)}
        
        idealValues = {"VOL": 0.1, "VOH": 0.9}

        run(filename, boundsVOL, boundsVOH, idealValues)
    """
    res = []

    for i in range(3):
        print("Calibrating... Iteration " + str(i+1) + "/3", end="\r", flush=True)
        vol = optimizeVOL(filename, boundsVOL, idealValues["VOL"])
        voh = optimizeVOH(filename, boundsVOH, idealValues["VOH"])
        curr = {'target': voh['target'] + vol['target'], 'params': {**voh['params'], **vol['params']}}
        res.append(curr)
    
    # return element with target closest to 0
    res.sort(key=lambda x: x['target'], reverse=True)
    editCMLNetlist(filename, **res[0]['params'])

    print("\nParameters optimized. Running cmd...\n")
    print(runCmd())


if __name__ == "__main__":

    boundsVOL = {"R1": (100, 1000),
                "R2": (100, 1000)}
    
    boundsVOH = {"R3": (100, 1000),
                "R4": (100, 1000)}
    
    boundsMisc = {"BF": (1,1000),
                  "RC": (1e-3, 50),
                  "RE": (1e-3, 50),
                  "RB": (1e-3, 50)}
    
    idealValues = {"VOH": 3.5,
                    "VOL": 2.7}
    
    run("1822-6817.inc", boundsVOL, boundsVOH, idealValues)
