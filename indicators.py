
 # implements your indicators as functions that operate on dataframes. The "main" code in indicators.py should generate the charts that illustrate your indicators in the report.
import sys
sys.path.append('..')
import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data



def sma(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,12,31), \
    syms = ['JPM'],lookback = 10, ratio = False):
    price =  get_data(syms, pd.date_range(sd, ed))
    price = price[syms]
    sma = price.rolling(window = lookback,min_periods=lookback).mean()
    # sma.values[lookback:,:]=(sma.values[lookback:,:] - sma.values[:-lookback,:])/lookback
    # sma.ix[:lookback,:] = np.nan
    ps = price/sma
    if (ratio):
        price.columns += '.price'
        sma.columns += '.sma'
        return pd.concat([ps, price, sma],axis = 1)
    else:
        return sma

# Bollinger Bands
def bb(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,12,31), \
    syms = ['JPM'],lookback = 10):
    price =  get_data(syms, pd.date_range(sd, ed))
    price = price[syms]
    bb_sma = sma(sd,ed,syms)
    rolling_std = price.rolling(window = lookback,min_periods=lookback).std()
    top_band = bb_sma+2*rolling_std
    bot_band = bb_sma-2*rolling_std
    bbp = (price - bot_band)/(top_band - bot_band)
    price.columns += '.price'
    top_band.columns += '.top_band'
    bot_band.columns += '.bot_band'
    return pd.concat([bbp,top_band,bot_band],axis = 1)

# Relative Strength
def rsi(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,12,31), \
    syms = ['JPM'],lookback = 10):
    price =  get_data(syms, pd.date_range(sd, ed))
    price = price[syms]
    daily_rets = price.copy()
    daily_rets.values[1:,:]= price.values[1:,:]-price.values[:-1,:]
    daily_rets.values[0,:] = np.nan

    up_rets = daily_rets[daily_rets >= 0].fillna(0).cumsum()
    down_rets = -1 * daily_rets[daily_rets < 0].fillna(0).cumsum()

    up_gain = price.copy()
    up_gain.ix[:,:] = 0
    up_gain.values[lookback:,:] = up_rets.values[lookback:,:]- up_rets.values[:-lookback,:]

    down_loss = price.copy()
    down_loss.ix[:,:] = 0
    down_loss.values[lookback:,:] = down_rets.values[lookback:,:]- down_rets.values[:-lookback,:]

    rs = (up_gain / lookback)/(down_loss/lookback)
    # rsi = price.copy()
    rsi = 100-(100/(1+rs))
    rsi.fillna(100,inplace = True)
    price.columns += '.price'
    up_gain.columns += '.up_gain'
    down_loss.columns += '.down_loss'
    return pd.concat([rsi,up_gain,down_loss],axis = 1)

#Stochastic Oscillator
#Overbought if Stochastic above 80, time to sell
#Oversold if Stochastic below 20, time to buy
#reference: http://www.investopedia.com/terms/s/stochasticoscillator.asp
def so(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,12,31), \
    syms = ['JPM'],lookback = 14):
    price =  get_data(syms, pd.date_range(sd, ed))
    price = price[syms]
    rolling_max = price.rolling(window = lookback,min_periods=lookback).max()
    rolling_min = price.rolling(window = lookback,min_periods=lookback).min()
    daily_range = rolling_max - rolling_min
    # daily_range.values[1:,:]= price.values[1:,:]-price.values[:-1,:]
    # daily_range.values[0,:] = np.nan
    so = 100*((price - rolling_min)/daily_range)
    price.columns += '.price'
    rolling_max.columns += '.rolling_max'
    rolling_min.columns += '.rolling_min'
    return pd.concat([so,rolling_max,rolling_min],axis = 1)

def test_code():
    prices_all =  get_data(['AAPL'], pd.date_range(dt.datetime(2010,01,01), dt.datetime(2010,12,31)))
    prices_all.fillna(method = 'ffill',inplace = True)
    prices_all.fillna(method = 'bfill',inplace = True)
    print prices_all

if __name__ == "__main__":

    print so()
