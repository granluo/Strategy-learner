 # implements your indicators as functions that operate on dataframes. The "main" code in indicators.py should generate the charts that illustrate your indicators in the report.
import sys
sys.path.append('..')
import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data
from indicators import bb,sma,so
# Bollinger Bands
# simple moving average rate
# Stochastic Oscillator

def testPolicy(symbol = "AAPL",sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000,impact = None):
    bb_index = bb(sd,ed,[symbol])
    sma_index = sma(sd,ed,[symbol],ratio = True)
    so_index = so(sd,ed,[symbol])
    decisions = pd.DataFrame(index = bb_index.index)
    decisions['bb'] = [-1 if x>1 else 1 if x <0 else 0 for x in bb_index[symbol]]
    decisions['sma'] = [-1 if x>1.05 else 1 if x <0.95 else 0 for x in sma_index[symbol]]
    decisions['so'] = [-1 if x>80 else 1 if x <20 else 0 for x in so_index[symbol]]
    decisions['holding'] = [0 if x == 0 else 1000 if x >0 else -1000 for x in decisions.sum(axis = 1)]
    decisions[symbol] = 0

    decisions[symbol].values[1:] = decisions['holding'].values[1:]-decisions['holding'].values[:-1]
    # print decisions['trade']

    decisions= decisions[[symbol]]
    return decisions
    # print sma_index
    # print so_index

if __name__ == "__main__":
    df_trades = testPolicy()
    print df_trades
