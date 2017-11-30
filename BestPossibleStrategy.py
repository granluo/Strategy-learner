 # implements your indicators as functions that operate on dataframes. The "main" code in indicators.py should generate the charts that illustrate your indicators in the report.
import sys
sys.path.append('..')
import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def testPolicy(symbol = "AAPL",sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000) :
    symbol = [symbol]
    dates = pd.date_range(sd, ed)
    prices = get_data(symbol, dates)  # automatically adds SPY
    prices = prices[symbol]
    daily_rets=prices.copy()
    daily_rets.values[1:,:]= prices.values[1:,:]-prices.values[:-1,:]
    daily_rets.values[0,:] = np.nan
    #benchmark
    # bm = prices.copy()
    # bm.values[:,:] = prices.values[:,:]/prices.values[0,:]
    # bmholding= prices.copy()
    # bmholding.values[:-1,]= 1000
    # bmholding.values[-1,]=0
    # bmtrade=bmholding.copy()
    # bmtrade.values[0,] = 1000
    # bmtrade.values[1:,:] = bmholding.values[1:,:] - bmholding.values[:-1,:]
    holding = prices.copy()
    holding.values[:-1,0] =[1000 if x>0  else -1000 for x in daily_rets[symbol].values[1:,]]
    holding.values[-1,:] = 0
    holding.columns = [symbol[0]+(' holding')]

    return holding
    # trade = holding.copy()
    # trade.values[1:,:] = holding.values[1:,:] - holding.values[:-1,:]
    # trade.values[0,:] = holding.values[0,:]
    # trade.columns = [symbol[0]+(' trade')]
    # print trade
    # print sv- (bmtrade.values*prices.values).sum()
    # print sv -1000*prices.values[0,0]+ 1000*prices.values[-1,0]
    # return trade
    # print daily_rets


if __name__ == "__main__":
    df_trades = testPolicy(symbol = "JPM", sd=dt.datetime(2008,1,2), ed=dt.datetime(2009,12,31), sv = 100000)
    print df_trades
