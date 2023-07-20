import os
from bayes_opt import BayesianOptimization, UtilityFunction

from extract import extractLVDS, editLVDSNetlist


def runLVDS(filename, MPD1_W=None, MND1_W=None, KP=None, RD=None, RS=None):
    editLVDSNetlist(filename, MPD1_W, MND1_W, KP, RD, RS)
    data = os.popen("C:/KD/cygwin-roq/bin/bash.exe -i -c \"/cygdrive/c/espy/roq/bin/hpspice.exe -s -c '. core.cmd'\"").read()
    data = data.splitlines()[1:]
    return extractLVDS(data)


def optimize(filename, boundsDelta, boundsCom):
    optimizeDelta(filename, boundsDelta)
    optimizeCom(filename, boundsCom)

def optimizeDelta(filename, bounds):
    optimizer = BayesianOptimization(
        f=None,
        pbounds=bounds,
        verbose=2,
        random_state=42,
        allow_duplicate_points=True
    )

    utility = UtilityFunction(kind="ucb", kappa=15, kappa_decay=0.95)

    for _ in range(30):
        next_point = optimizer.suggest(utility)
        lvdsDict = runLVDS(filename, **next_point)
        targetVOD = -abs(lvdsDict["Output delta"] - 0.36) # always negated because we want to maximize
        optimizer.register(params=next_point, target=targetVOD)

        print("Output Delta:", lvdsDict["Output delta"])
        print("Target VOD:", targetVOD)
        print("Next point:", next_point)
        print()

    print(optimizer.max)
    # print(optimizer.max['params'])
    editLVDSNetlist(filename, **optimizer.max['params'])


def optimizeCom(filename, bounds):
    optimizer = BayesianOptimization(
        f=None,
        pbounds=bounds,
        verbose=2,
        random_state=42,
        allow_duplicate_points=True
    )

    utility = UtilityFunction(kind="ucb", kappa=3)

    for _ in range(15):
        next_point = optimizer.suggest(utility)
        lvdsDict = runLVDS(filename, **next_point)
        target = -abs(lvdsDict["Output com"] - 1.23) # always negated because we want to maximize
        optimizer.register(params=next_point, target=target)

        print("Output Com:", lvdsDict["Output com"])
        print("Target Com:", target)
        print("Next point:", next_point)
        print()

    print(optimizer.max)
    # print(optimizer.max['params'])
    editLVDSNetlist(filename, **optimizer.max['params'])


if __name__ == "__main__":
    optimize("1822-2408.inc", {'MPD1_W': (1e-6,1e-3),
                                'MND1_W': (1e-6,1e-3)},
                                {'KP': (1e-5,1e-3),
                                 'RD': (1,300),
                                 'RS': (1,300)})