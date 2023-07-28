import os
from bayes_opt import BayesianOptimization, UtilityFunction
from bayes_opt.event import Events
from bayes_opt.logger import JSONLogger
from bayes_opt.util import load_logs

from util import extractMOSCmd, extractMosText, genMosCmd, editMOSNetlist, editJson

def runMOS(filename, VTO=None, KP=None, LAMBDA=None, RS=None, RD=None):
    editMOSNetlist(filename, VTO, KP, LAMBDA, RS, RD)
    data = os.popen("C:/KD/cygwin-roq/bin/bash.exe -i -c \"/cygdrive/c/espy/roq/bin/hpspice.exe -s -f -c '. core.cmd'\"").read()
    data = data.splitlines()[1:]
    return extractMOSCmd(data)


def optimizeT(filename, bounds):
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

    
    print("Calibrating T...")

    for _ in range(20):
        next_point = optimizer.suggest(utility)
        mosDict = runMOS(filename, **next_point)
        try:
            target = -abs(sum(softexp(i[1], 0.5) for i in mosDict["T"]))
        except OverflowError:
            target = -abs(sum(i[1] for i in mosDict["T"]))
        optimizer.register(next_point, target)
    print(optimizer.max)
    editMOSNetlist(filename, **optimizer.max['params'])


def optimizeS(filename, bounds):
    optimizer = BayesianOptimization(
        f=None,
        pbounds=bounds,
        verbose=2,
        random_state=42,
        allow_duplicate_points=True
    )

    editJson("logs.json", 5)
    load_logs(optimizer, logs=["./logs.json"])
    # os.remove("logs.json")

    utility = UtilityFunction(kind="ucb", kappa=5)

    print("Calibrating S...")
    for _ in range(20):
        next_point = optimizer.suggest(utility)
        mosDict = runMOS(filename, **next_point)
        target = sum(-abs(ood(i[2])) for i in mosDict["S"])
        target += sum(-abs(ood(i[2])) for i in mosDict["L"])
        T_delta = -abs(sum(softexp(i[1], 1) for i in mosDict["T"]))
        target += T_delta
        optimizer.register(next_point, target)

        # print("Target S:", target)
    print(optimizer.max)
    editMOSNetlist(filename, **optimizer.max['params'])

# soft exponential activation function
def softexp(x, threshold):
    if x <= threshold: return x
    elif x > 5: return 100
    else: return 2**(x-0.2)

def ood(x):
    # values towards 1 exponentially get lower, hence better
    if x <= 1: return (1/x)-1
    else: return softexp(x, 1)

def optimize(filename, bounds):
    optimizeT(filename, bounds)
    optimizeS(filename, bounds)
    print("Parameters optimized. Running cmd...")
    print(os.popen("C:/KD/cygwin-roq/bin/bash.exe -i -c \"/cygdrive/c/espy/roq/bin/hpspice.exe -s -c '. core.cmd'\"", ).read())


if __name__ == "__main__":
    os.chdir("1855-3098")

    bounds = {"VTO": (0.1, 3.95),
                "KP": (0.1, 100),
                "LAMBDA": (1e-2, 100),
                "RS": (1e-6, 1e-2),
                "RD": (1e-6, 1e-2)}

    # genMosCmd("core.cmd", extractMosText("mos_data.txt"), True)
    optimize("1855-3098.inc", bounds)