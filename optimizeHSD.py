#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# *****************************************************************************
# Name:     optimizeHSD.py
# Purpose:  Optimize LVDS, ECL, CML model parameters
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
# * 1. Experiment with tuning LVDS parameters with the same values
# * 2. Refine bounds if needed
#

from bayes_opt import BayesianOptimization, SequentialDomainReductionTransformer, UtilityFunction
from util import *


# Class for LVDS optimizations
# and necessary functions
class optimizeLVDS():
    def __init__(self, filename, boundsDelta, boundsV, idealValues):
        self.filename = filename
        self.boundsDelta = boundsDelta
        self.boundsV = boundsV
        self.idealValues = idealValues

    def runLVDS(self, params):
        editLVDSNetlist(self.filename, **params)
        data = runCmd().splitlines()[1:]
        return extractLVDS(data)
    
    def optimizeDelta(self):
        optimizer = BayesianOptimization(
            f=None,
            pbounds=self.boundsDelta,
            allow_duplicate_points=True,
            bounds_transformer=SequentialDomainReductionTransformer()
        )

        # define acquisition function
        utility = UtilityFunction(kind="ucb", kappa=5)

        # number of iterations
        deltaIters = 25
        # controls penalty for delta
        # higher = more optimization for delta
        penalty = -20

        for _ in range(deltaIters):
            next_point = optimizer.suggest(utility)
            lvdsDict = self.runLVDS(next_point)
            
            # calculate output errors
            # Force both W to be almost equal to each other
            # Cant be exactly equal because many decimal places are used
            if abs(next_point["MPD1_W"] - next_point["MND1_W"]) > 1e-2:
                # print(next_point["MPD1_W"] - next_point["MND1_W"])
                target = -50
            else:
                target = penaltyFunc(lvdsDict["Output delta"], self.idealValues["VOH"]-self.idealValues["VOL"], penalty)
            optimizer.register(next_point, target)

        print(optimizer.max)
        editLVDSNetlist(self.filename, **optimizer.max['params'])
        return optimizer.max
    
    def optimizeV(self):
        optimizer = BayesianOptimization(
            f=None,
            pbounds=self.boundsV,
            allow_duplicate_points=True,
            bounds_transformer=SequentialDomainReductionTransformer()
        )

        # define acquisition function
        utility = UtilityFunction(kind="ucb", kappa=5)

        # PARAMETERS
        vIters = 25
        penalty = -20

        for _ in range(vIters):
            next_point = optimizer.suggest(utility)
            lvdsDict = self.runLVDS(next_point)
            
            # calculate output errors

            # Commented out because it doesnt produce good results
            # Increasing threshold might help but might as well not have a threshold
            # if abs(next_point["P_RD"] - next_point["P_RS"]) > 3 or abs(next_point["N_RD"] - next_point["N_RS"]) > 3:
            #     target = -50
            # else:
            target = penaltyFunc(lvdsDict["Output DOUTP"], self.idealValues["VOH"], penalty)\
                    + penaltyFunc(lvdsDict["Output DOUTN"], self.idealValues["VOL"], penalty)
            optimizer.register(next_point, target)

        print(optimizer.max)
        editLVDSNetlist(self.filename, **optimizer.max['params'])
        return optimizer.max
    
    def run(self):
        res = []
        errorThreshold = -0.1  # must be < 0 as error is negative

        iters = 3

        for i in range(iters):
            print("Calibrating... Iteration " + str(i+1) + "/" + str(iters), end="\r", flush=True)
            delta = self.optimizeDelta()
            v = self.optimizeV()
            curr = {'params': {**delta['params'], **v['params']}, 'target': delta['target'] + v['target']}
            res.append(curr)
            if curr['target'] > errorThreshold: break

        # select best result
        res.sort(key=lambda x: x['target'], reverse=True)
        editLVDSNetlist(self.filename, **res[0]['params'], rounded=True)

        print("Optimization complete. Running cmd...\n")
        print(runCmd())


# ECL OPTIMIZATION
class optimizeECL():
    def __init__(self, filename, boundsVOH, boundsVOL, idealValues):
        self.filename = filename
        self.boundsVOH = boundsVOH
        self.boundsVOL = boundsVOL
        self.idealValues = idealValues

    def runECL(self, RB1=None, RB2=None):
        editECLNetlist(self.filename, RB1, RB2)
        data = runCmd().splitlines()[1:]
        return extractECL(data)
    
    def optimizeVOH(self):
        optimizer = BayesianOptimization(
            f=None,
            pbounds=self.boundsVOH,
            allow_duplicate_points=True,
            bounds_transformer=SequentialDomainReductionTransformer()
        )

        # define acquisition function
        utility = UtilityFunction(kind="ucb", kappa=5)

        # PARAMETERS
        vohIters = 25
        penalty = -30

        for _ in range(vohIters):
            next_point = optimizer.suggest(utility)
            eclDict = self.runECL(**next_point)
            target = penaltyFunc(eclDict["Output VOH"], self.idealValues["VOH"], penalty)
            optimizer.register(next_point, target)
        
        print(optimizer.max)
        editECLNetlist(self.filename, **optimizer.max['params'])
        return optimizer.max
    
    def optimizeVOL(self):
        optimizer = BayesianOptimization(
            f=None,
            pbounds=self.boundsVOL,
            allow_duplicate_points=True,
            bounds_transformer=SequentialDomainReductionTransformer()
        )

        # define acquisition function
        utility = UtilityFunction(kind="ucb", kappa=5)

        # PARAMETERS
        volIters = 25
        penalty = -30

        for _ in range(volIters):
            next_point = optimizer.suggest(utility)
            eclDict = self.runECL(**next_point)
            target = penaltyFunc(eclDict["Output VOL"], self.idealValues["VOL"], penalty)
            optimizer.register(next_point, target)
        
        print(optimizer.max)
        editECLNetlist(self.filename, **optimizer.max['params'])
        return optimizer.max
    
    def run(self):
        res = []
        errorThreshold = -1e-4

        iters = 2

        for i in range(iters):
            print("Calibrating... Iteration " + str(i+1) + "/" + str(iters), end="\r", flush=True)
            voh = self.optimizeVOH()
            vol = self.optimizeVOL()
            curr = {'params': {**voh['params'], **vol['params']}, 'target': voh['target'] + vol['target']}
            res.append(curr)
            if curr['target'] > errorThreshold: break

        # select best result
        res.sort(key=lambda x: x['target'], reverse=True)
        editECLNetlist(self.filename, **res[0]['params'], rounded=True)

        print("Optimization complete. Running cmd...\n")
        print(runCmd())


# CML OPTIMIZATION
class optimizeCML():
    def __init__(self, filename, boundsVOL, boundsVOH, idealValues):
        self.filename = filename
        self.boundsVOL = boundsVOL
        self.boundsVOH = boundsVOH
        self.idealValues = idealValues

    def runCML(self, R1=None, R2=None, R3=None, R4=None):
        editCMLNetlist(self.filename, R1, R2, R3, R4)
        data = runCmd().splitlines()[1:]
        return extractCML(data)
    
    def optimizeVOL(self):
        optimizer = BayesianOptimization(
            f=None,
            pbounds=self.boundsVOL,
            allow_duplicate_points=True,
            bounds_transformer=SequentialDomainReductionTransformer()
        )

        # define acquisition function
        utility = UtilityFunction(kind="ucb", kappa=5)

        # PARAMETERS
        volIters = 25
        penalty = -10

        for _ in range(volIters):
            next_point = optimizer.suggest(utility)
            cmlDict = self.runCML(**next_point)
            target = penaltyFunc(cmlDict["Output VOL"], self.idealValues["VOL"], penalty)
            optimizer.register(next_point, target)
        
        print(optimizer.max)
        editCMLNetlist(self.filename, **optimizer.max['params'])
        return optimizer.max
    
    def optimizeVOH(self):
        optimizer = BayesianOptimization(
            f=None,
            pbounds=self.boundsVOH,
            allow_duplicate_points=True,
            bounds_transformer=SequentialDomainReductionTransformer()
        )

        # define acquisition function
        utility = UtilityFunction(kind="ucb", kappa=5, kappa_decay=0.95, kappa_decay_delay=10)

        # PARAMETERS
        vohIters = 25
        penalty = -10

        for _ in range(vohIters):
            next_point = optimizer.suggest(utility)
            cmlDict = self.runCML(**next_point)
            target = penaltyFunc(cmlDict["Output VOH"], self.idealValues["VOH"], penalty)
            optimizer.register(next_point, target)
        
        print(optimizer.max)
        editCMLNetlist(self.filename, **optimizer.max['params'])
        return optimizer.max
    
    def run(self):
        res = []
        errorThreshold = -1e-4

        iters = 2

        for i in range(iters):
            print("Calibrating... Iteration " + str(i+1) + "/" + str(iters), end="\r", flush=True)
            vol = self.optimizeVOL()
            voh = self.optimizeVOH()
            curr = {'params': {**vol['params'], **voh['params']}, 'target': vol['target'] + voh['target']}
            res.append(curr)
            if curr['target'] > errorThreshold: break

        # select best result
        res.sort(key=lambda x: x['target'], reverse=True)
        editCMLNetlist(self.filename, **res[0]['params'], rounded=True)

        print("Optimization complete. Running cmd...\n")
        print(runCmd())


# example usage
if __name__ == "__main__":
    boundsVOH = {"RB1": (1, 1000)}
    boundsVOL = {"RB2": (1, 1000)}
    
    idealValues = {"VOH": 3.21,
                    "VOL": 4.105}
    
    filename = "1821-0424.inc"
    optimizeECL(filename, boundsVOH, boundsVOL, idealValues).run()
