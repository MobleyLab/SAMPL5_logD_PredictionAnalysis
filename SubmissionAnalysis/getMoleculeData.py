# Written by Caitlin C Bannan
# Mobley Group, UC Irvine
"""
Organizes data by molecule and saves to a new dictionary. Also creates QQ and comparison plots.
"""
import pickle 
import imp
tools = imp.load_source('tools','../DataFiles/tools.py')
import numpy as np

bootits = 1000 # Number of bootstraps

# Load experimental and predicted data and ID numbers by batch
expData = pickle.load(open('../DataFiles/experimental.p','rb'))
batches = pickle.load(open('../DataFiles/batches.p','rb'))
calcData = pickle.load(open('../DataFiles/predictions.p','rb'))

# create dictionary to store data by molecule
molData = {}
best = [16, 2, 73, 44, 27, 60, 40, 54, 14, 28, 32, 36, 39, 34, 53, 56, 47, 35, 15, 43, 19, 48, 21, 61, 8, 7, 10, 49, 41, 20, 28]
for b, batch in enumerate(batches):
    bat = 'batch%i' % b
    print bat
    # Submission IDs that submitted this batch
    # SIDs = [k for k in calcData.keys() if calcData[k].has_key(bat)]
    SIDs = [k for k in calcData.keys() if k in best]

    # for each molecule ID save experimental and predicted data and compute error analysis
    for k in batch:
        molData[k] = {'MW': expData[k]['MW'], 'Smiles': expData[k]['Smiles'], 'iupac': expData[k]['iupac'], 'tautomers': expData[k]['tautomers']}
        # Store lists of experimental and calculated values for each molecule
        molData[k]['exp'] = [expData[k]['data'][0] for i in range(len(SIDs))]
        molData[k]['dexp'] = [expData[k]['data'][1] for i in range(len(SIDs))]
        molData[k]['dcalc_stat'] = [calcData[SID]['data'][k][1] for SID in SIDs]
        molData[k]['dcalc_mod'] = [calcData[SID]['data'][k][2] for SID in SIDs]
        molData[k]['calc'] = [calcData[SID]['data'][k][0] for SID in SIDs]
        molData[k]['batch'] = b
        # Error analysis for this molecule 
        AveErr, RMS, AUE, tau, R, maxErr, percent, _ = tools.stats_array(molData[k]['calc'], molData[k]['exp'], molData[k]['dexp'], bootits, sid = k)

        # Store error analysis in dictionary
        molData[k]['AveErr'] = AveErr
        molData[k]['RMS'] = RMS
        molData[k]['AUE'] = AUE
        molData[k]['tau'] = tau
        molData[k]['R'] = R 
        molData[k]['maxErr'] = maxErr
        molData[k]['percent'] = percent 

        # QQ plot for this molecule
        X, Y, slope, dslope = tools.getQQdata(molData[k]['calc'], molData[k]['exp'], molData[k]['dcalc_mod'], molData[k]['dexp'], bootits) 
        molData[k]['error slope'] = [slope, dslope]
        molData[k]['QQdata'] = [X,Y]
        title = "QQ Plot for %s" % k
        tools.makeQQplot(X, Y, slope, title, fileName = "../QQPlots/%s_topHalf_QQ.pdf" % k)

pickle.dump(molData, open('../DataFiles/moleculeData_topHalf.p','wb'))
