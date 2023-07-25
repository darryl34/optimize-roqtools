import os
from bayes_opt import BayesianOptimization, UtilityFunction
from bayes_opt.event import Events
from bayes_opt.logger import JSONLogger
from bayes_opt.util import load_logs

# from util import extractMOSFET, editMOSFETNetlist, editJson


def optimize():
    print("Parameters optimized. Running cmd...")
    print(os.popen("C:/KD/cygwin-roq/bin/bash.exe -i -c \"/cygdrive/c/espy/roq/bin/hpspice.exe -s -c '. core.cmd'\"", ).read())


if __name__ == "__main__":
    os.chdir("1855-3098")
    optimize()