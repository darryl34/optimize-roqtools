import os
from bayes_opt import BayesianOptimization, UtilityFunction

from util import extractCML, editCMLNetlist, penaltyFunc, runCmd

def runCML(filename, R1=None, R2=None, R3=None, R4=None, BF=None, RC=None, RE=None, RB=None, MCA_W=None):
    editCMLNetlist(filename, R1, R2, R3, R4, BF, RC, RE, RB, MCA_W)
    data = runCmd().splitlines()[1:]
    return extractCML(data)

def optimizeV(filename, bounds, VOH, VOL, IVCC):
    optimizer = BayesianOptimization(
        f=None,
        pbounds=bounds,
        allow_duplicate_points=True
    )

    # define acquisition function
    utility = UtilityFunction(kind="ucb", kappa=5)


    for _ in range(10):
        next_point = optimizer.suggest(utility)
        cmlDict = runCML(filename, **next_point)
        target = penaltyFunc(cmlDict["Output VOH"], VOH, -20)
        target += penaltyFunc(cmlDict["Output VOL"], VOL, -10)
        target += penaltyFunc(cmlDict["Output Delta"], VOH-VOL, -10)
        target += penaltyFunc(cmlDict["IVCC"], IVCC, -5)
        optimizer.register(next_point, target)

    print(optimizer.max)
    return optimizer.max


def optimize(filename, bounds, idealValues):
    res = []
    errorThreshold = -0.1  # must be < 0

    for i in range(5):
        print("Calibrating... Iteration " + str(i+1) + "/5", end="\r", flush=True)
        curr = optimizeV(filename, bounds, **idealValues)
        res.append(curr)
        if curr['target'] > errorThreshold:
            break
    
    # return element with target closest to 0
    res.sort(key=lambda x: x['target'], reverse=True)
    editCMLNetlist(filename, **res[0]['params'])

    print("\nParameters optimized. Running cmd...\n")
    print(runCmd())

if __name__ == "__main__":

    bounds = {"R1": (100, 1000),
                "R2": (100, 1000),
                "R3": (100, 1000),
                "R4": (100, 1000),
                "BF": (1,1000),
                "RC": (1e-3, 500),
                "RE": (1e-3, 500),
                "RB": (1e-3, 500),
                "MCA_W": (1e-6, 1e-4)}
    
    idealValues = {"VOH": 3.5,
                    "VOL": 2.7,
                    "IVCC": 0.13}

    optimize("1822-6817.inc", bounds, idealValues)
