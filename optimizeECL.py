import os
from bayes_opt import BayesianOptimization, UtilityFunction
from bayes_opt.event import Events
from bayes_opt.logger import JSONLogger
from bayes_opt.util import load_logs

from util import extractECL, editECLNetlist, editJson

def runECL(filename, RB1=None, RB2=None, MB1_w=None, MB2_W=None):
    editECLNetlist(filename, RB1, RB2, MB1_w, MB2_W)
    data = os.popen("C:/KD/cygwin-roq/bin/bash.exe -i -c \"/cygdrive/c/espy/roq/bin/hpspice.exe -s -c '. core.cmd'\"").read()
    data = data.splitlines()[1:]
    return extractECL(data)

if __name__ == "__main__":
    os.chdir("1822-2408")
    runECL("1822-2408.inc", 1, 1, 0.5, 0.5)