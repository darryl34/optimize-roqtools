import os
from bayes_opt import BayesianOptimization, UtilityFunction
from bayes_opt.event import Events
from bayes_opt.logger import JSONLogger
from bayes_opt.util import load_logs

from util import extractCML, editCMLNetlist, editJson, change

def runCML(filename, R1=None, R2=None, R3=None, R4=None, BF=None, RC=None, RE=None, RB=None, MCA_W=None):
    editCMLNetlist(filename, R1, R2, R3, R4, BF, RC, RE, RB, MCA_W)
    if os.name == 'nt':
        data = os.popen("C:/KD/cygwin-roq/bin/bash.exe -i -c \"/cygdrive/c/espy/roq/bin/hpspice.exe -s -f -c '. core.cmd'\"").read()
    else:
        data = os.popen("/mnt/c/KD/cygwin-roq/bin/bash.exe -i -c \"/cygdrive/c/espy/roq/bin/hpspice.exe -s -f -c '. core.cmd'\" 2>/dev/null").read()
    data = data.splitlines()[1:]
    return extractCML(data)

def optimizeV(filename, bounds, VOH, VOL, delta):
    optimizer = BayesianOptimization(
        f=None,
        pbounds=bounds,
        verbose=2,
        allow_duplicate_points=True
    )

    # logger object initialization
    logger = JSONLogger(path="./logs.json")
    optimizer.subscribe(Events.OPTIMIZATION_STEP, logger)

    # define acquisition function
    utility = UtilityFunction(kind="ucb", kappa=5)


    for i in range(20):
        print("Calibrating VOH and VOL... Iteration " + str(i+1) + "/20", end="\r", flush=True)
        next_point = optimizer.suggest(utility)
        cmlDict = runCML(filename, **next_point)
        target = -abs(change(cmlDict["Output VOH"], VOH))
        target += -abs(change(cmlDict["Output VOL"], VOL))
        target += -abs(change(cmlDict["Output Delta"], delta)) * 2
        optimizer.register(next_point, target)

        # print("Output VOH:", cmlDict["Output VOH"])
        # print("Target VOH:", target)
        # print("Next point:", next_point)
    # print(optimizer.max)
    editCMLNetlist(filename, **optimizer.max['params'])


def optimizeCurrent(filename, bounds, VOH, VOL, Delta, IVCC):
    optimizer = BayesianOptimization(
        f=None,
        pbounds=bounds,
        verbose=2,
        allow_duplicate_points=True
    )

    # scale target values and load previous logs
    editJson("logs.json", 5)
    load_logs(optimizer, logs=["./logs.json"])
    os.remove("logs.json")  # delete after loading logs

    utility = UtilityFunction(kind="ucb", kappa=5)


    for i in range(10):
        print("Calibrating IVCC... Iteration " + str(i+1) + "/10        ", end="\r", flush=True)
        next_point = optimizer.suggest(utility)
        cmlDict = runCML(filename, **next_point)
        target = -abs(change(cmlDict["IVCC"], IVCC))
        target += -abs(change(cmlDict["Output VOH"], VOH) + change(cmlDict["Output Delta"], Delta) ) * 2
        target += -abs(change(cmlDict["Output VOL"], VOL))
        optimizer.register(params=next_point, target=target)

    editCMLNetlist(filename, **optimizer.max['params'])



def optimize(filename, bounds, idealValues):
    optimizeV(filename, bounds, idealValues["VOH"], idealValues["VOL"], idealValues["Delta"])
    optimizeCurrent(filename, bounds, **idealValues)
    print("\nParameters optimized. Running cmd...\n")
    if os.name == 'nt':
        data = os.popen("C:/KD/cygwin-roq/bin/bash.exe -i -c \"/cygdrive/c/espy/roq/bin/hpspice.exe -s -f -c '. core.cmd'\"").read()
    else:
        data = os.popen("/mnt/c/KD/cygwin-roq/bin/bash.exe -i -c \"/cygdrive/c/espy/roq/bin/hpspice.exe -s -f -c '. core.cmd'\" 2>/dev/null").read()
    print(data)

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
                    "Delta": 0.8,
                    "IVCC": 0.13}
    
    optimize("1822-6817.inc", bounds, idealValues)