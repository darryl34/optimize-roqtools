#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# *****************************************************************************
# Name:     optimizeLVDS.py
# Purpose:  Optimize LVDS model parameters
# Script version: 1.0
# Python version: Python 3.8.10
# Compatible OS: Windows 10
# Requirements: Hpspice, bayesian-optimization
# Developer (v1.0): Darryl Ng
# Notes: Bayesian Optimization GitHub repo:
#       https://github.com/bayesian-optimization/BayesianOptimization
#       The example notebooks provide a good overview of the model functions
#       and how to use the library.
# 
# Version History:
# - v1.0 (2023-09-05) - First version
# *****************************************************************************
#
# Future Improvements:
# * 1. Refine bounds if needed
# * 2. Remove unnecessary parameters
#


from bayes_opt import BayesianOptimization, SequentialDomainReductionTransformer, UtilityFunction
from util import extractCML, editCMLNetlist, penaltyFunc, runCmd

def runCML(filename, R1=None, R2=None, R3=None, R4=None, BF=None, RC=None, RE=None, RB=None):
    editCMLNetlist(filename, R1, R2, R3, R4, BF, RC, RE, RB)
    data = runCmd().splitlines()[1:]
    return extractCML(data)

def optimizeVOL(filename, bounds, VOL):
    optimizer = BayesianOptimization(
        f=None,
        pbounds=bounds,
        allow_duplicate_points=True,
        bounds_transformer=SequentialDomainReductionTransformer()
    )

    # define acquisition function
    utility = UtilityFunction(kind="ucb", kappa=5, kappa_decay=0.95, kappa_decay_delay=10)

    for _ in range(25):
        next_point = optimizer.suggest(utility)
        cmlDict = runCML(filename, **next_point)
        target = penaltyFunc(cmlDict["Output VOL"], VOL, -10)
        optimizer.register(next_point, target)

    print(optimizer.max)
    editCMLNetlist(filename, **optimizer.max['params'])
    return optimizer.max


def optimizeVOH(filename, bounds, VOH):
    optimizer = BayesianOptimization(
        f=None,
        pbounds=bounds,
        allow_duplicate_points=True,
        bounds_transformer=SequentialDomainReductionTransformer()
    )

    utility = UtilityFunction(kind="ucb", kappa=5, kappa_decay=0.95, kappa_decay_delay=10)

    for _ in range(25):
        next_point = optimizer.suggest(utility)
        cmlDict = runCML(filename, **next_point)
        target = penaltyFunc(cmlDict["Output VOH"], VOH, -10)
        optimizer.register(next_point, target)

    print(optimizer.max)
    editCMLNetlist(filename, **optimizer.max['params'])
    return optimizer.max

def run(filename, boundsVOL, boundsVOH, idealValues):
    """
    Optimize the parameters of a model file by running a calibration process
    on VOH and VOL outputs sequentially. The best result is then selected and
    the model file is edited to reflect the optimized parameters.

    Args:
        filename (str): The name of the model file.
        boundsVOL (dict): A dictionary specifying the bounds for the VOL parameters.
        boundsVOH (dict): A dictionary specifying the bounds for the VOH parameters.
        idealValues (dict): A dictionary specifying the ideal VOL and VOH values.

    Returns:
        None
    """
    res = []

    for i in range(2):
        print("Calibrating... Iteration " + str(i+1) + "/2")
        vol = optimizeVOL(filename, boundsVOL, idealValues["VOL"])
        voh = optimizeVOH(filename, boundsVOH, idealValues["VOH"])
        curr = {'target': voh['target'] + vol['target'], 'params': {**voh['params'], **vol['params']}}
        res.append(curr)
    
    # return element with target closest to 0
    res.sort(key=lambda x: x['target'], reverse=True)
    editCMLNetlist(filename, **res[0]['params'], rounded=True)

    print("\nParameters optimized. Running cmd...\n")
    print(runCmd())


def run_with_params(filename: str, RB1_L: int, RB1_R: int,
                    RB2_L: int, RB2_R: int,
                    RB3_L: int, RB3_R: int,
                    RB4_L: int, RB4_R: int, 
                    VOH: float, VOL: float):
    run(filename, {"R1": (RB1_L, RB1_R), "R2": (RB2_L, RB2_R)},
                {"R3": (RB3_L, RB3_R), "R4": (RB4_L, RB4_R)},
                {"VOH": VOH, "VOL": VOL})

if __name__ == "__main__":

    boundsVOL = {"R1": (100, 1000),
                "R2": (100, 1000)}
    
    boundsVOH = {"R3": (100, 1000),
                "R4": (100, 1000)}
    
    boundsMisc = {"BF": (1,1000),
                  "RC": (1e-3, 50),
                  "RE": (1e-3, 50),
                  "RB": (1e-3, 50)}
    
    idealValues = {"VOH": 3.5,
                    "VOL": 2.7}
    
    filename = "1822-6817.inc"

    run(filename, boundsVOL, boundsVOH, idealValues)
