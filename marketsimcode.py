 # implements your indicators as functions that operate on dataframes. The "main" code in indicators.py should generate the charts that illustrate your indicators in the report.
# Zongran Luo
# zluo76
"""MC2-P1: Market simulator."""
import sys
sys.path.append('..')
import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data
import BestPossibleStrategy as bp
import ManualStrategy as ms
import matplotlib.pyplot as plt

def compute_portvals(orders, start_val = 100000, commission=0, impact=0):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here
    orders.sort_index(inplace = True)
    orders = orders[(orders.T != 0).any()]
    symbol = orders.columns[0]
    df = pd.DataFrame()
    df['Date']= orders.index
    df['Symbol'] = 'JPM'
    df['Order'] = ["BUY" if x >0 else "SELL" for x in orders.values]
    df['Shares'] = abs(orders.values)
    orders = df
    orders.set_index('Date',inplace = True)
    cash = start_val
    # Get discrete value from column Symbol so as to get symbols
    symbols = orders['Symbol'].apply(pd.Series).stack().drop_duplicates().tolist()

    start_date = orders.index[0]#dt.datetime(orders['Date'][0])
    end_date = orders.index[-1]#dt.datetime(2008,6,1)
    # for i, tra in orders.iterrows():
    #     print tra
    portvals = get_data(symbols, pd.date_range(start_date, end_date))
    # portvals = portvals.reindex(pd.date_range(start_date, end_date), fill_value=np.nan)
    portvals.fillna(method = 'ffill',inplace = True)
    portvals.fillna(method = 'bfill',inplace = True)
    portvals = portvals[symbols]  # remove BM
    # print portvals

    shares_hold = {}
    Daily_value = pd.DataFrame(columns = ['Value'])
    Daily_value.loc[start_date] = 0
    # print Daily_value
    for i in symbols:
        shares_hold[i] = 0
    date_current = start_date
    for i,tra in orders.iterrows():
        if not isinstance(portvals.loc[i][tra['Symbol']],float):
            continue
        while True:
            try:

                Daily_value.loc[date_current] = sum([shares_hold[x]*portvals.loc[date_current][x] for x in shares_hold])+cash

            except KeyError:
                pass
            except UnboundLocalError:
                pass

            if date_current >= tra.name:
                break
            date_current +=  dt.timedelta(days=1)
        if tra['Order'] == 'BUY':
            shares_hold[tra['Symbol']]+=tra['Shares']
            # print shares_hold
            # print "value of shares", tra['Shares']*portvals.loc[i][tra['Symbol']]
            cash -= tra['Shares']*(portvals.loc[i][tra['Symbol']]*(1+impact))
            cash -= commission
        if tra['Order'] == 'SELL':
            shares_hold[tra['Symbol']]-=tra['Shares']

            cash += tra['Shares']*(portvals.loc[i][tra['Symbol']]*(1-impact))
            cash -= commission
        # Update last row of transations
        Daily_value.loc[date_current] = sum([shares_hold[x]*portvals.loc[date_current][x] for x in shares_hold])+cash

    return Daily_value

def plotgraph(title,label,policy = ms.testPolicy, symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000,impact = None):
    mstrade =policy(symbol , sd, ed, sv,impact = impact)
    portvals =compute_portvals(mstrade)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"

    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    bm = pd.DataFrame()
    bm['Date']= [mstrade.index.values[0], mstrade.index.values[-1]]
    bm[symbol] = [1000,-1000]

    bm.set_index('Date',inplace=True)
    bmportvals =  compute_portvals(bm)
    if isinstance(bmportvals, pd.DataFrame):
        bmportvals = bmportvals[bmportvals.columns[0]]
    bmdaily_return = bmportvals.copy()
    bmdaily_return[1:]=(bmportvals.ix[1:]/bmportvals.ix[:-1].values)-1
    bmdaily_return.ix[0] = 0.

    fig, ax = plt.subplots()
    for d in mstrade.index[mstrade[symbol]<0]:
        ax.axvline(x = d , color = 'red')
    for d in mstrade.index[mstrade[symbol]>0]:
        ax.axvline(x = d, color ='green')

    ax.plot(portvals.index,portvals.values/portvals.values[0],color = 'black',label=label)
    ax.plot(bmportvals.index,bmportvals.values/bmportvals.values[0],color = 'blue',label='Benchmark')
    if type(impact) is list:
        color=plt.cm.rainbow(np.linspace(0,1,len(impact)))
        c = 0
        for i in impact:
            po = compute_portvals(mstrade,impact = i)
            ax.plot(portvals.index,po.values/po.values[0],color = color[c],label=label+' impact '+str(i))
            c+= 1
            
    plt.title(title)
    ax.legend(loc='best', shadow=True)
    fig.autofmt_xdate()
    plt.show()


def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters
    plotgraph('BestPossibleStrategy','Best Strategy',policy = bp.testPolicy,sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31))
    plotgraph('In Sample ManualStrategy','Manual Strategy',sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31))
    plotgraph('Out of Sample ManualStrategy','Manual Strategy',sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31))
    mstrade =ms.testPolicy(symbol = "JPM", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000)

    portvals =compute_portvals(mstrade)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]]
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = portvals.index[0]
    end_date = portvals.index[-1]
    daily_return = portvals.copy()
    daily_return[1:]=(portvals.ix[1:]/portvals.ix[:-1].values)-1
    daily_return.ix[0] = 0.
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [ portvals.ix[-1]/portvals.ix[0]-1,
                                                            daily_return[1:].mean(),
                                                            daily_return[1:].std(),
                                                            252**0.5*((daily_return[1:]-0).mean())/daily_return[1:].std()]
    bm = pd.DataFrame()
    bm['Date']= [dt.datetime(2010,1,4), dt.datetime(2011,12,30)]
    bm['JPM'] = [1000,-1000]

    bm.set_index('Date',inplace=True)
    bmportvals =  compute_portvals(bm)
    if isinstance(bmportvals, pd.DataFrame):
        bmportvals = bmportvals[bmportvals.columns[0]]
    bmdaily_return = bmportvals.copy()
    bmdaily_return[1:]=(bmportvals.ix[1:]/bmportvals.ix[:-1].values)-1
    bmdaily_return.ix[0] = 0.
    cum_ret_bm, avg_daily_ret_bm, std_daily_ret_bm, sharpe_ratio_bm = [ bmportvals.ix[-1]/bmportvals.ix[0]-1,
                                                            bmdaily_return[1:].mean(),
                                                            bmdaily_return[1:].std(),
                                                            252**0.5*((bmdaily_return[1:]-0).mean())/bmdaily_return[1:].std()]




    #
    # bptesttrade =bp.testPolicy(symbol = "JPM", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000)
    #
    # portvals =compute_portvals(bptesttrade)
    # bm.set_index ([[dt.datetime(2010,1,1), dt.datetime(2011,12,31)]],inplace=True)
    #
    # bmportvals =  compute_portvals(bm)
    # bmportvals = bmportvals[bmportvals.columns[0]]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of BM : {}".format(sharpe_ratio_bm)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of BM : {}".format(cum_ret_bm)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of BM : {}".format(std_daily_ret_bm)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of BM : {}".format(avg_daily_ret_bm)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])
    print "Final Benchmark Portfolio Value: {}".format(bmportvals[-1])
def author():
    return 'zluo76' # replace tb34 with your Georgia Tech username.
if __name__ == "__main__":
    test_code()
