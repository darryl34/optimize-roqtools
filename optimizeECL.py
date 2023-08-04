import os
from bayes_opt import BayesianOptimization, UtilityFunction
from bayes_opt.event import Events
from bayes_opt.logger import JSONLogger
from bayes_opt.util import load_logs

from util import extractECL, editECLNetlist, editJson, change


def runECL(filename, RB1=None, RB2=None, MB1_W=None, MB2_W=None):
    editECLNetlist(filename, RB1, RB2, MB1_W, MB2_W)
    if os.name == 'nt':
        data = os.popen("C:/KD/cygwin-roq/bin/bash.exe -i -c \"/cygdrive/c/espy/roq/bin/hpspice.exe -s -f -c '. core.cmd'\"").read()
    else:
        data = os.popen("/mnt/c/KD/cygwin-roq/bin/bash.exe -i -c \"/cygdrive/c/espy/roq/bin/hpspice.exe -s -f -c '. core.cmd'\" 2>/dev/null").read()
    data = data.splitlines()[1:]
    return extractECL(data)


def optimizeV(filename, bounds, VOH, VOL): 
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

    
    for i in range(15):
        print("Calibrating VOH and VOL... Iteration: " + str(i+1) + "/15", end="\r", flush=True)
        next_point = optimizer.suggest(utility)
        eclDict = runECL(filename, **next_point)
        target = -abs(change(eclDict["Output VOH"], VOH))
        target += -abs(change(eclDict["Output VOL"], VOL))
        optimizer.register(next_point, target)
    # print(optimizer.max)
    editECLNetlist(filename, **optimizer.max['params'])


def optimizeCurrent(filename, bounds, VOH, VOL, IAVDD):
    optimizer = BayesianOptimization(
        f=None,
        pbounds=bounds,
        verbose=2,
        random_state=42,
        allow_duplicate_points=True
    )

    # scale target values and load previous logs
    editJson("logs.json", 1)
    load_logs(optimizer, logs=["./logs.json"])
    os.remove("logs.json")  # delete after loading logs

    utility = UtilityFunction(kind="ucb", kappa=5)


    for i in range(10):
        print("Calibrating IAVDD... Iteration: " + str(i+1) + "/10 ", end="\r", flush=True)
        next_point = optimizer.suggest(utility)
        eclDict = runECL(filename, **next_point)
        target = -abs(change(eclDict["Analog Supply Current IAVDD"], IAVDD))
        target += -abs(change(eclDict["Output VOH"], VOH))
        target += -abs(change(eclDict["Output VOL"], VOL))
        optimizer.register(next_point, target)
        # print("Target IAVDD:", target)
    # print(optimizer.max)
    editECLNetlist(filename, **optimizer.max['params'])


def optimize(filename, bounds, idealValues):
    optimizeV(filename, bounds, idealValues["VOH"], idealValues["VOL"])
    optimizeCurrent(filename, bounds, **idealValues)
    print("\nParameters optimized. Running cmd...\n")
    if os.name == 'nt':
        data = os.popen("C:/KD/cygwin-roq/bin/bash.exe -i -c \"/cygdrive/c/espy/roq/bin/hpspice.exe -s -f -c '. core.cmd'\"").read()
    else:
        data = os.popen("/mnt/c/KD/cygwin-roq/bin/bash.exe -i -c \"/cygdrive/c/espy/roq/bin/hpspice.exe -s -f -c '. core.cmd'\" 2>/dev/null").read()
    print(data)

if __name__ == "__main__":

    bounds = {"RB1": (100, 1000),
            "RB2": (100, 1000),
            "MB1_W": (1e-6,1e-4),
            "MB2_W": (1e-6,1e-4)}
    
    idealValues = {"VOH": 3.21,
                    "VOL": 4.105,
                    "IAVDD": 0.07}

    optimize("1821-0424.inc", bounds, idealValues)