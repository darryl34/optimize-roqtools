#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# *****************************************************************************
# Name:     optimize_mosfet.py
# Purpose:  Optimize MOSFET model parameters
# Script version: 1.0
# Python version: Python 3.8.10
# Compatible OS: Windows 10
# Requirements: Hpspice, bayesian-optimization
# Developer (v1.0): Darryl Ng
# Notes: Bayesian Optimization GitHub repo:
#       https://github.com/bayesian-optimization/BayesianOptimization
#       The example notebooks provide a good overview of the model functions
#       and how to use the library.
# ***************************************************************************
# Usage:
# 1. Edit cmd file and place initials T, S and L at the start of each data line
#    Example: print "DS VG..." -> print "T DS VG..."
# 2. Ensure that params in the inc file are in the correct order
#    Example:
#       1st row: .model MN2675 UCBMOS NMOS VTO KP LAMBDA
#       2nd row: + RS, RD ...
# 3. Check that VTO bounds are correct
# 4. Run script
#
# Version History:
# - v1.0 (2023-09-05) - First version
# *****************************************************************************
#
# Future Improvements:
# * 1. Auto generate cmd file based on harness and mos_data.txt
#


from bayes_opt import BayesianOptimization, SequentialDomainReductionTransformer, UtilityFunction
from bayes_opt.util import NotUniqueError
from util import editMOSNetlist, extractMOSCmd, runCmd, penaltyFunc

# Running Hpspice cmd
def runMOS(filename, VTO=None, KP=None, LAMBDA=None, RS=None, RD=None):
    editMOSNetlist(filename, VTO, KP, LAMBDA, RS, RD)
    data = runCmd().splitlines()[1:]
    return extractMOSCmd(data)


# optimize Transfer and Saturation together
def optimizeTS(filename, bounds):
    optimizer = BayesianOptimization(
        f=None,
        pbounds=bounds,
        verbose=1,
        allow_duplicate_points=True,
        bounds_transformer=SequentialDomainReductionTransformer()
    )

    # define acquisition function
    utility = UtilityFunction(kind="ucb", kappa=5, kappa_decay=0.95, kappa_decay_delay=15)
    
    iters = 10      # change this to increase number of iterations
    sPenalty = -30  # penalty for S, decrease this to increase penalty
    
    # run iterations
    for _ in range(iters):
        next_point = optimizer.suggest(utility)
        mosDict = runMOS(filename, **next_point)
        
        # calculate error value
        target = -abs(sum(i[1] for i in mosDict["T"]))
        target += sum(penaltyFunc(i[2], 1, sPenalty) for i in mosDict["S"])
        optimizer.register(next_point, target)
    
    print(optimizer.max)
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

    # get current best params
    mosDict = runMOS(filename)
    currBest = sum(penaltyFunc(i[2], 1, -20) for i in mosDict["S"])

    iters = 15      # change this to increase number of iterations
    sPenalty = -20  # penalty for S, decrease this to increase penalty
    lPenalty = -10  # penalty for L

    for i in range(iters):
        print("Calibrating L... Iteration: " + str(i+1) + "/" + str(iters), end="\r", flush=True)
        next_point = optimizer.suggest(utility)
        mosDict = runMOS(filename, **next_point)
        target = sum(penaltyFunc(i[2], 1, sPenalty) for i in mosDict["S"])
        target += sum(penaltyFunc(i[2], 1, lPenalty) for i in mosDict["L"])
        try:
            optimizer.register(next_point, target)
        except NotUniqueError:
            # break if duplicate point is repeatedly found 
            dup_counter += 1
            if dup_counter > 2: break
            continue
    
    # calculate new best with tuned Linear
    mosDict = runMOS(filename)
    newBest = sum(penaltyFunc(i[2], 1, -20) for i in mosDict["S"])
    print("\nCurrent Best: " + str(currBest))
    print("New Best: " + str(newBest))
    
    # update only if newly found best is better than existing best
    if newBest > currBest:
        print(optimizer.max)
        editMOSNetlist(filename, **optimizer.max['params'], rounded=True)
    else:
        editMOSNetlist(filename, **max_dict['params'], rounded=True)


def run(filename, bounds):
    res = []

    iters = 10    # change this to increase number of iterations

    for i in range(iters):
        print("Calibrating T and S... Iteration: " + str(i+1) + "/" + str(iters), end="\r", flush=True)
        res.append(optimizeTS(filename, bounds))
    
    # sort by target value
    res.sort(key=lambda x: x["target"], reverse=True)
    editMOSNetlist(filename, **res[0]['params'], rounded=True)

    optimizeL(filename, bounds["KP"], bounds["RS"], bounds["RD"], res[0])
    print("\nParameters optimized. Running cmd...\n")
    print(runCmd())


if __name__ == "__main__":

    # Set bounds for optimization
    bounds = {"VTO": (0.7, 1),
                "KP": (0.1, 10),
                "LAMBDA": (1e-2, 10),
                "RS": (1e-6, 1e-2),
                "RD": (1e-6, 1e-4)}

    filename = "1855-2187.inc"

    run(filename, bounds)