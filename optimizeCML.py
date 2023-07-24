import os
from bayes_opt import BayesianOptimization, UtilityFunction
from bayes_opt.event import Events
from bayes_opt.logger import JSONLogger
from bayes_opt.util import load_logs

from util import extractCML, editCMLNetlist, editJson

def runCML(filename, R1=None, R2=None, R3=None, R4=None, BF=None, RC=None, RE=None, RB=None, MCA_W=None):
    editCMLNetlist(filename, R1, R2, R3, R4, BF, RC, RE, RB, MCA_W)
    data = os.popen("C:/KD/cygwin-roq/bin/bash.exe -i -c \"/cygdrive/c/espy/roq/bin/hpspice.exe -s -c '. core.cmd'\"").read()
    data = data.splitlines()[1:]
    return extractCML(data)

def optimizeV(filename, bounds, VOH, VOL, delta):
    optimizer = BayesianOptimization(
        f=None,
        pbounds=bounds,
        verbose=2,
        random_state=42,
        allow_duplicate_points=True
    )

    # logger object initialization
    logger = JSONLogger(path="./logs.json")
    optimizer.subscribe(Events.OPTIMIZATION_STEP, logger)

    # define acquisition function
    utility = UtilityFunction(kind="ucb", kappa=5)

    print("Calibrating VOH and VOL...")

    for _ in range(20):
        next_point = optimizer.suggest(utility)
        cmlDict = runCML(filename, **next_point)
        target = -abs(cmlDict["Output VOH"] - VOH)
        target += -abs(cmlDict["Output VOL"] - VOL) * 1.5
        target += -abs(cmlDict["Output Delta"] - delta)
        optimizer.register(next_point, target)

        # print("Output VOH:", cmlDict["Output VOH"])
        # print("Target VOH:", target)
        # print("Next point:", next_point)
    editCMLNetlist(filename, **optimizer.max['params'])


def optimizeCurrent(filename, bounds, VOH, VOL, delta, IVCC):
    optimizer = BayesianOptimization(
        f=None,
        pbounds=bounds,
        verbose=2,
        random_state=42,
        allow_duplicate_points=True
    )

    # scale target values and load previous logs
    editJson("logs.json", 5)
    load_logs(optimizer, logs=["./logs.json"])
    os.remove("logs.json")  # delete after loading logs

    utility = UtilityFunction(kind="ucb", kappa=5)

    print("Calibrating IVCC...")

    for _ in range(10):
        next_point = optimizer.suggest(utility)
        cmlDict = runCML(filename, **next_point)
        target = -abs(cmlDict["IVCC"] - IVCC)
        target += -abs((cmlDict["Output VOH"] - VOH) + (cmlDict["Output Delta"] - delta)) * 5
        target += -abs(cmlDict["Output VOL"] - VOL) * 5
        optimizer.register(params=next_point, target=target)

    editCMLNetlist(filename, **optimizer.max['params'])



def optimize(filename, bounds, idealValues):
    optimizeV(filename, bounds, idealValues["VOH"], idealValues["VOL"], idealValues["Delta"])
    optimizeCurrent(filename, bounds, idealValues["VOH"], idealValues["VOL"], idealValues["Delta"], idealValues["IVCC"])
    print("Parameters optimized. Running cmd...")
    print(os.popen("C:/KD/cygwin-roq/bin/bash.exe -i -c \"/cygdrive/c/espy/roq/bin/hpspice.exe -s -c '. core.cmd'\"", ).read())

if __name__ == "__main__":
    os.chdir("1822-6817")

    bounds = {"R1": (100, 1000),
                "R2": (100, 1000),
                "R3": (100, 1000),
                "R4": (100, 1000),
                "BF": (1,1000),
                "RC": (1, 1000),
                "RE": (1, 1000),
                "RB": (1, 1000),
                "MCA_W": (1e-6, 1e-4)}
    
    idealValues = {"VOH": 3.5,
                    "VOL": 2.7,
                    "Delta": 0.8,
                    "IVCC": 0.13}
    
    optimize("1822-6817.inc", bounds, idealValues)