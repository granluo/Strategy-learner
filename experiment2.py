import sys
sys.path.append('..')
import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data
import BestPossibleStrategy as bp
import ManualStrategy as ms
import StrategyLearner as sl
import matplotlib.pyplot as plt
import marketsimcode as mktsim


def test():

    # mktsim.plotgraph('BestPossibleStrategy','Best Strategy',policy = bp.testPolicy,sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31))
    # mktsim.plotgraph('In Sample ManualStrategy','Manual Strategy',sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31))
    slearner = sl.StrategyLearner()
    slearner.addEvidence(symbol='JPM',sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31),sv = 10000)
    mktsim.plotgraph('In Sample StrategyLearner','RDT Strategy',policy = slearner.testPolicy, sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), impact=[0.001,0.002,0.003,0.005])

if __name__ == '__main__':
    test()
