"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch
"""
import sys
sys.path.append('..')
import datetime as dt
import pandas as pd
import util as ut
import random
import RTLearner as rt
import BestPossibleStrategy as bps
import indicators as ind
import marketsimcode as mktsim
class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = False, impact=0.0):
        self.verbose = verbose
        self.impact = impact
        self.learner = rt.RTLearner(leaf_size=5)
        self.lb = 14 #lookback
    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000):

        # add your code to do learning here

        # example usage of the old backward compatible util function
        syms=[symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        if self.verbose: print prices
        # example use with new colname
        volume_all = ut.get_data(syms, dates, colname = "Volume")  # automatically adds SPY
        volume = volume_all[syms]  # only portfolio symbols
        volume_SPY = volume_all['SPY']  # only SPY, for comparison later
        if self.verbose: print volume


        #random tree
        self.bps = bps.testPolicy(symbol ,sd, ed, sv)

        df = pd.concat([self.dataset_addind(sd,ed,symbol,self.lb),self.bps],axis = 1)
        # print df.ix[:,0:-1]
        self.learner.addEvidence(df.ix[:,0:-1],df.ix[:,-1])

    def dataset_addind(self,sd,ed,symbol,lookback):
        sma = ind.sma(sd , ed ,syms = [symbol],lookback = self.lb, ratio = False)
        bb = ind.bb(sd , ed ,syms = [symbol],lookback = self.lb)
        rsi = ind.rsi(sd , ed ,syms = [symbol],lookback = self.lb)
        df = pd.concat([sma,bb,rsi],axis = 1)
        return df

    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):
        # here we build a fake set of trades
        # your code should return the same sort of data
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        trades = prices_all[[symbol,]]  # only portfolio symbols
        indicators = self.dataset_addind(sd,ed,symbol,self.lb)

        # get holding, LONG, SHORT, CASH
        holding = self.learner.query(indicators)

        #get trade
        trades = holding.copy()
        trades.values[1:] = holding.values[1:] - holding.values[:-1]
        trades.values[0] = holding.values[0]
        trades.columns = [symbol+(' trade')]
        # print mktsim.compute_portvals(trade, start_val = 100000, commission=0, impact=0)
        #
        # trades_SPY = prices_all['SPY']  # only SPY, for comparison later
        # trades.values[:,:] = 0 # set them all to nothing
        # trades.values[0,:] = 1000 # add a BUY at the start
        # trades.values[40,:] = -1000 # add a SELL
        # trades.values[41,:] = 1000 # add a BUY
        # trades.values[60,:] = -2000 # go short from long
        # trades.values[61,:] = 2000 # go long from short
        # trades.values[-1,:] = -1000 #exit on the last day
        # print trades
        if self.verbose: print type(trades) # it better be a DataFrame!
        if self.verbose: print trades
        if self.verbose: print prices_all
        return trades

if __name__=="__main__":

    a = StrategyLearner()
    a.addEvidence()
    a.testPolicy()
    print "One does not simply think up a strategy"
