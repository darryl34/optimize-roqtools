import os
from bayes_opt import BayesianOptimization, SequentialDomainReductionTransformer, UtilityFunction
from bayes_opt.util import NotUniqueError

from mos_util import editMOSNetlist, extractMOSCmd
from util import runCmd, penaltyFunc

def runMOS(filename, VTO=None, KP=None, LAMBDA=None, RS=None, RD=None):
    editMOSNetlist(filename, VTO, KP, LAMBDA, RS, RD)
    data = runCmd().splitlines()[1:]
    return extractMOSCmd(data)


# optimize T and S together
def optimizeT(filename, bounds):
    optimizer = BayesianOptimization(
        f=None,
        pbounds=bounds,
        verbose=1,
        allow_duplicate_points=True,
        bounds_transformer=SequentialDomainReductionTransformer()
    )

    # load_logs(optimizer, logs=["./logs.json"])
    # os.remove("logs.json")

    # define acquisition function
    utility = UtilityFunction(kind="ucb", kappa=5, kappa_decay=0.95, kappa_decay_delay=15)

    for _ in range(30):
        next_point = optimizer.suggest(utility)
        mosDict = runMOS(filename, **next_point)
        target = -abs(sum(i[1] for i in mosDict["T"])) / 2
        target = sum(penaltyFunc(i[2], 1, -20) for i in mosDict["S"])
        optimizer.register(next_point, target)
        # print(target)
    print(optimizer.max)
    # editMOSNetlist(filename, **optimizer.max['params'])
    return optimizer.max

# Optimize L with KP, RS and RD params
def optimizeL(filename, KP, RS, RD, max_dict):
    optimizer = BayesianOptimization(
        f=None,
        pbounds={"KP": KP,
                "RS": RS,
                "RD": RD},
        verbose=0,
        allow_duplicate_points=False
    )

    utility = UtilityFunction(kind="ucb", kappa=3)
    dup_counter = 0
    mosDict = runMOS(filename)
    currBest = sum(penaltyFunc(i[2], 1, -20) for i in mosDict["S"])

    for i in range(10):
        print("Calibrating L... Iteration: " + str(i+1) + "/10", end="\r", flush=True)
        next_point = optimizer.suggest(utility)
        mosDict = runMOS(filename, **next_point)
        target = sum(penaltyFunc(i[2], 1, -20) for i in mosDict["S"])
        target += sum(penaltyFunc(i[2], 1, -10) for i in mosDict["L"])
        try:
            optimizer.register(next_point, target)
        # break if duplicate point is found repeatedly
        except NotUniqueError:
            dup_counter += 1
            if dup_counter > 2: break
            continue
    
    mosDict = runMOS(filename)
    newBest = sum(penaltyFunc(i[2], 1, -20) for i in mosDict["S"])
    # update only if newly found best is better than existing best
    if newBest > currBest:
        print(optimizer.max)
        editMOSNetlist(filename, **optimizer.max['params'])
    else:
        editMOSNetlist(filename, **max_dict['params'])


def run(filename, bounds):
    res = []

    for i in range(3):
        print("Calibrating T and S... Iteration: " + str(i+1) + "/3", end="\r", flush=True)
        res.append(optimizeT(filename, bounds))
    
    # sort by target value
    res.sort(key=lambda x: x["target"], reverse=True)
    editMOSNetlist(filename, **res[0]['params'])

    optimizeL(filename, bounds["KP"], bounds["RS"], bounds["RD"], res[0])
    print("\nParameters optimized. Running cmd...\n")
    print(runCmd())


if __name__ == "__main__":
    os.chdir("1855-3098")

    bounds = {"VTO": (3, 3.9),
                "KP": (0.1, 10),
                "LAMBDA": (1e-2, 10),
                "RS": (1e-6, 1e-2),
                "RD": (1e-6, 1e-4)}

    run("1855-3098.inc", bounds)