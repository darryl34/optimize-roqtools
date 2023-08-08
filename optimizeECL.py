import os
from bayes_opt import BayesianOptimization, UtilityFunction

from util import extractECL, editECLNetlist, penaltyFunc, runCmd


def runECL(filename, RB1=None, RB2=None, MB1_W=None, MB2_W=None):
    editECLNetlist(filename, RB1, RB2, MB1_W, MB2_W)
    data = runCmd().splitlines()[1:]
    return extractECL(data)


def optimizeCurrent(filename, bounds, VOH, VOL, IAVDD):
    optimizer = BayesianOptimization(
        f=None,
        pbounds=bounds,
        verbose=2,
        allow_duplicate_points=True
    )

    # scale target values and load previous logs
    # editJson("logs.json", 1)
    # load_logs(optimizer, logs=["./logs.json"])
    # os.remove("logs.json")  # delete after loading logs

    utility = UtilityFunction(kind="ucb", kappa=5)


    for i in range(10):
        next_point = optimizer.suggest(utility)
        eclDict = runECL(filename, **next_point)
        target = penaltyFunc(eclDict["Output VOH"], VOH, -20)
        target += penaltyFunc(eclDict["Output VOL"], VOL, -20)
        target += penaltyFunc(eclDict["Analog Supply Current IAVDD"], IAVDD, -5)
        optimizer.register(next_point, target)
    
    print(optimizer.max)
    # editECLNetlist(filename, **optimizer.max['params'])
    return optimizer.max


def optimize(filename, bounds, idealValues):
    res = []
    errorThreshold = -0.1  # must be < 0

    for i in range(5):
        print("Calibrating... Iteration " + str(i+1) + "/5", end="\r", flush=True)
        curr = optimizeCurrent(filename, bounds, **idealValues)
        res.append(curr)
        if curr['target'] > errorThreshold:
            break

    # return element with target closest to 0
    res.sort(key=lambda x: x['target'], reverse=True)
    editECLNetlist(filename, **res[0]['params'])

    print("\nParameters optimized. Running cmd...\n")
    print(runCmd())

if __name__ == "__main__":

    bounds = {"RB1": (100, 1000),
            "RB2": (100, 1000),
            "MB1_W": (1e-6,1e-4),
            "MB2_W": (1e-6,1e-4)}
    
    idealValues = {"VOH": 2.32,
                    "VOL": 1.5,
                    "IAVDD": 0.17}
    
    optimize("1822-2408.inc", bounds, idealValues)
