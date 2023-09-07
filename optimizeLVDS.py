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
# * 1. Experiment with tuning parameters with the same values
# * 2. Refine bounds
#


from bayes_opt import BayesianOptimization, SequentialDomainReductionTransformer, UtilityFunction
from util import editLVDSNetlist, extractLVDS, penaltyFunc, runCmd

# Run core.cmd, returns a dictionary of extracted values
def runLVDS(filename, params):
    editLVDSNetlist(filename, **params)
    data = runCmd().splitlines()[1:]
    return extractLVDS(data)


def optimizeDelta(filename, bounds, VOH, VOL):
    optimizer = BayesianOptimization(
        f=None,
        pbounds=bounds,
        allow_duplicate_points=True,
        bounds_transformer=SequentialDomainReductionTransformer()
    )

    # define acquisition function
    utility = UtilityFunction(kind="ucb", kappa=5)

    for _ in range(25):
        next_point = optimizer.suggest(utility)
        lvdsDict = runLVDS(filename, next_point)
        
        # calculate output errors
        # Force both W to be almost equal to each other
        # Cant be exactly equal because many decimal places are used
        if abs(next_point["MPD1_W"] - next_point["MND1_W"]) > 1e-2:
            print(next_point["MPD1_W"] - next_point["MND1_W"])
            target = -50
        else:
            target = penaltyFunc(lvdsDict["Output delta"], VOH-VOL, -20)
        optimizer.register(next_point, target)

    print(optimizer.max)
    editLVDSNetlist(filename, **optimizer.max['params'])
    return optimizer.max


def optimizeV(filename, bounds, VOH, VOL):
    optimizer = BayesianOptimization(
        f=None,
        pbounds=bounds,
        allow_duplicate_points=True,
        bounds_transformer=SequentialDomainReductionTransformer()
    )

    # define acquisition function
    utility = UtilityFunction(kind="ucb", kappa=5)

    for _ in range(25):
        next_point = optimizer.suggest(utility)
        lvdsDict = runLVDS(filename, next_point)
        
        # calculate output errors

        # Commented out because it doesnt produce good results
        # Increasing threshold might help but might as well not have a threshold
        # if abs(next_point["P_RD"] - next_point["P_RS"]) > 3 or abs(next_point["N_RD"] - next_point["N_RS"]) > 3:
        #     target = -50
        # else:
        target = penaltyFunc(lvdsDict["Output DOUTP"], VOH, -20) + penaltyFunc(lvdsDict["Output DOUTN"], VOL, -20)
        optimizer.register(next_point, target)

    print(optimizer.max)
    editLVDSNetlist(filename, **optimizer.max['params'])
    return optimizer.max


def run(filename, boundsDelta, boundsV, idealValues):
    """
    Optimize the parameters of a model file by running a calibration process
    on Delta and VOH/VOL outputs sequentially. The best result is then selected and
    the model file is edited to reflect the optimized parameters.

    Args:
        filename (str): The name of the model file.
        boundsDelta (dict): A dictionary specifying the bounds for the Delta parameters.
        boundsV (dict): A dictionary specifying the bounds for the V parameters.
        idealValues (dict): A dictionary specifying the ideal VOH and VOL values.

    Returns:
        None
    """
    res = []
    errorThreshold = -0.1  # must be < 0 as error is negative

    for i in range(3):
        print("Calibrating... Iteration " + str(i+1) + "/3", end="\r", flush=True)
        delta = optimizeDelta(filename, boundsDelta, **idealValues)
        v = optimizeV(filename, boundsV, **idealValues)
        curr = {'params': {**delta['params'], **v['params']}, 'target': delta['target'] + v['target']}
        res.append(curr)
        # end optimization if target is better than threshold
        if curr['target'] > errorThreshold: break
    
    # return element with target closest to 0
    res.sort(key=lambda x: x['target'], reverse=True)
    editLVDSNetlist(filename, **res[0]['params'])

    print("\nParameters optimized. Running cmd...\n")
    print(runCmd())


# For GUI parameters use
def run_with_params(filename: str, 
                    MPD1_L: float, MPD1_H: float,
                    MND1_L: float, MND1_H: float,
                    P_KP_L: float, P_KP_H: float,
                    P_RD_L: float, P_RD_H: float,
                    P_RS_L: float, P_RS_H: float,
                    N_KP_L: float, N_KP_H: float,
                    N_RD_L: float, N_RD_H: float,
                    N_RS_L: float, N_RS_H: float,
                    VOH: float, VOL: float):
    
    boundsDelta = {'MPD1_W': (MPD1_L, MPD1_H),
                   'MND1_W': (MND1_L, MND1_H)}
    
    boundsV = {'P_KP': (P_KP_L, P_KP_H),
               'P_RD': (P_RD_L, P_RD_H),
               'P_RS': (P_RS_L, P_RS_H),
               'N_KP': (N_KP_L, N_KP_H),
               'N_RD': (N_RD_L, N_RD_H),
               'N_RS': (N_RS_L, N_RS_H)}
    
    idealValues = {"VOH": VOH, 
                   "VOL": VOL}
    
    run(filename, boundsDelta, boundsV, idealValues)


if __name__ == "__main__":

    boundsDelta = {'MPD1_W': (1e-6,1e-3),
                   'MND1_W': (1e-6,1e-3)}
    
    boundsV = {'P_KP': (1e-5,10e-3),
               'P_RD': (1,50),
               'P_RS': (1,50),
               'N_KP': (1e-5,10e-3),
               'N_RD': (1,50),
               'N_RS': (1,50)}
    
    idealValues = {"VOH": 1.6, 
                   "VOL": 1.15}
    
    filename = "1813-3032.inc"
    
    run(filename, boundsDelta, boundsV, idealValues)
