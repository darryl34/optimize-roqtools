import os
from bayes_opt import BayesianOptimization, UtilityFunction
from bayes_opt.event import Events
from bayes_opt.logger import JSONLogger
from bayes_opt.util import load_logs

from util import extractLVDS, editLVDSNetlist, editJson


def runLVDS(filename, MPD1_W=None, MND1_W=None, KP=None, RD=None, RS=None):
    editLVDSNetlist(filename, MPD1_W, MND1_W, KP, RD, RS)
    data = os.popen("C:/KD/cygwin-roq/bin/bash.exe -i -c \"/cygdrive/c/espy/roq/bin/hpspice.exe -s -c '. core.cmd'\"").read()
    data = data.splitlines()[1:]
    return extractLVDS(data)


def optimizeVOH(filename, bounds, VOH, delta):
    # optimizer object initialization
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

    print("Calibrating VOH...")

    for _ in range(20):
        next_point = optimizer.suggest(utility)
        lvdsDict = runLVDS(filename, **next_point)
        targetVOH = -abs(lvdsDict["Output DOUTP"] - VOH) # always negated because we want to maximize
        targetVOH += -abs(lvdsDict["Output delta"] - delta) * 4
        optimizer.register(params=next_point, target=targetVOH)

        # print("Output DOUTP:", lvdsDict["Output DOUTP"])
        # print("Target VOH:", targetVOH)
        # print("Next point:", next_point)
    editLVDSNetlist(filename, **optimizer.max['params'])


def optimizeVOL(filename, bounds, VOH, VOL, delta):
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

    print("Calibrating VOL...")

    for _ in range(15):
        next_point = optimizer.suggest(utility)
        lvdsDict = runLVDS(filename, **next_point)
        target = -abs(lvdsDict["Output DOUTN"] - VOL) # always negated because we want to maximize
        target += -abs(lvdsDict["Output DOUTP"] - VOH) * 2
        target += -abs(lvdsDict["Output delta"] - delta) * 4
        optimizer.register(params=next_point, target=target)

        # print("Output DOUTN:", lvdsDict["Output DOUTN"])
        # print("Target DOUTN:", target)
        # print("Next point:", next_point)
        # print()
    editLVDSNetlist(filename, **optimizer.max['params'])
    # print(optimizer.max)
    # print(optimizer.max['params'])


# call this function to optimize LVDS
def optimize(filename, bounds, idealValues):
    optimizeVOH(filename, bounds, idealValues["VOH"], idealValues["delta"])
    optimizeVOL(filename, bounds, idealValues["VOH"], idealValues["VOL"], idealValues["delta"])
    print("Parameters optimized. Running cmd...\n")
    print(os.popen("C:/KD/cygwin-roq/bin/bash.exe -i -c \"/cygdrive/c/espy/roq/bin/hpspice.exe -s -c '. core.cmd'\"", ).read())


if __name__ == "__main__":
    testDir = "1822-2408"
    os.chdir(testDir)

    bounds = {'MPD1_W': (1e-6,1e-3),
            'MND1_W': (1e-6,1e-3),
            'KP': (1e-5,1e-3),
            'RD': (1,300),
            'RS': (1,300)}
    
    idealValues = {"VOH": 1.41, "VOL": 1.05, "delta": 0.36}

    optimize("1822-2408.inc", bounds, idealValues)
