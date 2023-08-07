import os
from bayes_opt import BayesianOptimization, UtilityFunction
from bayes_opt.event import Events
from bayes_opt.logger import JSONLogger
from bayes_opt.util import load_logs, NotUniqueError

from util import extractMOSCmd, extractMosText, genMosCmd, editMOSNetlist, editJson

def runMOS(filename, VTO=None, KP=None, LAMBDA=None, RS=None, RD=None):
    editMOSNetlist(filename, VTO, KP, LAMBDA, RS, RD)
    if os.name == 'nt':
        data = os.popen("C:/KD/cygwin-roq/bin/bash.exe -i -c \"/cygdrive/c/espy/roq/bin/hpspice.exe -s -f -c '. core.cmd'\"").read()
    else:
        data = os.popen("/mnt/c/KD/cygwin-roq/bin/bash.exe -i -c \"/cygdrive/c/espy/roq/bin/hpspice.exe -s -f -c '. core.cmd'\" 2>/dev/null").read()
    data = data.splitlines()[1:]
    return extractMOSCmd(data)


def optimizeS(filename, bounds):
    optimizer = BayesianOptimization(
        f=None,
        pbounds=bounds,
        verbose=1,
        allow_duplicate_points=True
    )

    # logger object initialization
    logger = JSONLogger(path="./logs.json")
    optimizer.subscribe(Events.OPTIMIZATION_STEP, logger)

    utility = UtilityFunction(kind="ucb", kappa=3)

    for i in range(20):
        print("Calibrating S... Iteration: " + str(i+1) + "/20", end="\r", flush=True)
        next_point = optimizer.suggest(utility)
        mosDict = runMOS(filename, **next_point)
        target = sum(-abs(ood(i[2])) for i in mosDict["S"])
        optimizer.register(next_point, target)

    print(optimizer.max)
    editMOSNetlist(filename, **optimizer.max['params'])

def optimizeT(filename, bounds):
    optimizer = BayesianOptimization(
        f=None,
        pbounds=bounds,
        verbose=1,
        allow_duplicate_points=True
    )

    editJson("logs.json", 1)
    load_logs(optimizer, logs=["./logs.json"])
    os.remove("logs.json")

    # define acquisition function
    utility = UtilityFunction(kind="ucb", kappa=5)

    for i in range(15):
        print("Calibrating T... Iteration: " + str(i+1) + "/15", end="\r", flush=True)
        next_point = optimizer.suggest(utility)
        mosDict = runMOS(filename, **next_point)
        target = -abs(sum(i[1] for i in mosDict["T"]))
        target += sum(-abs(ood(i[2])) for i in mosDict["S"])
        optimizer.register(next_point, target)
    print(optimizer.max)
    editMOSNetlist(filename, **optimizer.max['params'])

    return optimizer.max


def optimizeL(filename, KP, RS, RD, max_dict):
    optimizer = BayesianOptimization(
        f=None,
        pbounds={"KP": KP,
                "RS": RS,
                "RD": RD},
        verbose=0,
        allow_duplicate_points=False
    )

    utility = UtilityFunction(kind="ucb", kappa=2)
    dup_counter = 0
    mosDict = runMOS(filename)
    currBest = sum(-abs(ood(i[2])) for i in mosDict["S"])

    for i in range(10):
        print("Calibrating L... Iteration: " + str(i+1) + "/10", end="\r", flush=True)
        next_point = optimizer.suggest(utility)
        mosDict = runMOS(filename, **next_point)
        target = sum(-abs(ood(i[2])) for i in mosDict["S"])
        target += sum(-abs(ood(i[2])) for i in mosDict["L"])
        try:
            optimizer.register(next_point, target)
        except NotUniqueError:
            dup_counter += 1
            if dup_counter > 2: break
            continue
    
    mosDict = runMOS(filename)
    newBest = sum(-abs(ood(i[2])) for i in mosDict["S"])
    if newBest > currBest:
        print(optimizer.max)
        editMOSNetlist(filename, **optimizer.max['params'])
    else:
        editMOSNetlist(filename, **max_dict['params'])


# soft exponential activation function
def softexp(x, threshold):
    if x <= threshold: return x
    elif x > 2: return 8*x
    else: return 2**(x*2)-1

def ood(x):
    # values towards 1 exponentially get lower, hence better
    if x <= 1e-4: return 1e4
    elif x <= 1: return 3*((1/x)-1)
    elif x <= 2-1e-4: return 3*((1/(2-x))-1)
    else: return 1e4+x

def optimize(filename, bounds):
    optimizeS(filename, bounds)
    res = optimizeT(filename, bounds)
    optimizeL(filename, bounds["KP"], bounds["RS"], bounds["RD"], res)
    print("\nParameters optimized. Running cmd...\n")
    if os.name == 'nt':
        data = os.popen("C:/KD/cygwin-roq/bin/bash.exe -i -c \"/cygdrive/c/espy/roq/bin/hpspice.exe -s -f -c '. core.cmd'\"").read()
    else:
        data = os.popen("/mnt/c/KD/cygwin-roq/bin/bash.exe -i -c \"/cygdrive/c/espy/roq/bin/hpspice.exe -s -f -c '. core.cmd'\" 2>/dev/null").read()
    print(data)


if __name__ == "__main__":
    os.chdir("1855-3098")

    bounds = {"VTO": (3, 3.9),
                "KP": (0.1, 10),
                "LAMBDA": (1e-2, 10),
                "RS": (1e-6, 1e-2),
                "RD": (1e-6, 1e-4)}

    # genMosCmd("core.cmd", extractMosText("mos_data.txt"), True)
    optimize("1855-3098.inc", bounds)