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

    for _ in range(20):
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

    for _ in range(20):
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

    for i in range(3):
        print("Calibrating... Iteration " + str(i+1) + "/3", end="\r", flush=True)
        voh = optimizeVOH(filename, boundsVOH, idealValues["VOH"])
        vol = optimizeVOL(filename, boundsVOL, idealValues["VOL"])
        curr = {'target': voh['target'] + vol['target'], 'params': {**voh['params'], **vol['params']}}
        res.append(curr)

    # return element with target closest to 0
    res.sort(key=lambda x: x['target'], reverse=True)
    editECLNetlist(filename, **res[0]['params'])

    print("\nParameters optimized. Running cmd...\n")
    print(runCmd())


if __name__ == "__main__":

    boundsVOH = {"RB1": (1, 1000)}
    boundsVOL = {"RB2": (1, 1000)}
    
    idealValues = {"VOH": 2.32,
                    "VOL": 1.5}
    
    os.chdir("1822-2408")
    run("1822-2408.inc", boundsVOH, boundsVOL, idealValues)
