import os
from bayes_opt import BayesianOptimization, UtilityFunction
from bayes_opt.event import Events
from bayes_opt.logger import JSONLogger
from bayes_opt.util import load_logs

from util import extractLVDS, editLVDSNetlist, editJson, change


def runLVDS(filename, MPD1_W=None, MND1_W=None, KP=None, RD=None, RS=None):
    editLVDSNetlist(filename, MPD1_W, MND1_W, KP, RD, RS)
    if os.name == 'nt':
        data = os.popen("C:/KD/cygwin-roq/bin/bash.exe -i -c \"/cygdrive/c/espy/roq/bin/hpspice.exe -s -f -c '. core.cmd'\"").read()
    else:
        data = os.popen("/mnt/c/KD/cygwin-roq/bin/bash.exe -i -c \"/cygdrive/c/espy/roq/bin/hpspice.exe -s -f -c '. core.cmd'\" 2>/dev/null").read()
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


    for i in range(20):
        print("Calibrating VOH... Iteration " + str(i+1) + "/20", end="\r", flush=True)
        next_point = optimizer.suggest(utility)
        lvdsDict = runLVDS(filename, **next_point)
        # always negated because we want to maximize
        targetVOH = -abs(change(lvdsDict["Output DOUTP"], VOH)) 
        targetVOH += -abs(change(lvdsDict["Output delta"], delta)) * 2
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

    # scale vars
    scaleJson = 5

    # scale target values and load previous logs
    editJson("logs.json", scaleJson)
    load_logs(optimizer, logs=["./logs.json"])
    os.remove("logs.json")  # delete after loading logs

    utility = UtilityFunction(kind="ucb", kappa=5)

    for i in range(15):
        print("Calibrating VOL... Iteration " + str(i+1) + "/15 ", end="\r", flush=True)
        next_point = optimizer.suggest(utility)
        lvdsDict = runLVDS(filename, **next_point)
        target = -abs(change(lvdsDict["Output DOUTN"], VOL))
        target += -abs(change(lvdsDict["Output DOUTP"], VOH))
        target += -abs(change(lvdsDict["Output delta"], delta))
        optimizer.register(params=next_point, target=target)

        # print("Output DOUTN:", lvdsDict["Output DOUTN"])
        # print("Target DOUTN:", target)
        # print("Next point:", next_point)
    editLVDSNetlist(filename, **optimizer.max['params'])


# call this function to optimize LVDS
def optimize(filename, bounds, idealValues):
    optimizeVOH(filename, bounds, idealValues["VOH"], idealValues["delta"])
    optimizeVOL(filename, bounds, idealValues["VOH"], idealValues["VOL"], idealValues["delta"])
    print("\nParameters optimized. Running cmd...\n")
    if os.name == 'nt':
        data = os.popen("C:/KD/cygwin-roq/bin/bash.exe -i -c \"/cygdrive/c/espy/roq/bin/hpspice.exe -s -f -c '. core.cmd'\"").read()
    else:
        data = os.popen("/mnt/c/KD/cygwin-roq/bin/bash.exe -i -c \"/cygdrive/c/espy/roq/bin/hpspice.exe -s -f -c '. core.cmd'\" 2>/dev/null").read()
    print(data)

if __name__ == "__main__":
    
    bounds = {'MPD1_W': (1e-6,1e-3),
            'MND1_W': (1e-6,1e-3),
            'KP': (1e-6,1e-3),
            'RD': (1,300),
            'RS': (1,300)}
    
    idealValues = {"VOH": 1.6, 
                   "VOL": 1.15, 
                   "delta": 0.45}

    optimize("1813-3032.inc", bounds, idealValues)
