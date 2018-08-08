## option pricing applet
### for given option xyz-Expiration, calculate expected return base on hosty and best fit.
### then save all data in invisement cloud.

import pandas as pd
import numpy as np
import matplotlib.pylab as plot
import math

priceApi = {
    "financialContent": "http://markets.financialcontent.com/stocks/action/gethistoricaldata?Symbol={}&Year=2019&Month=12&Range=500"
}

mapper = {
    "price": "close"
}

def fetch_EOD_price_table (stock, provider="financialContent"):
    url = priceApi[provider].format(stock.upper())
    prices = pd.read_csv (url)
    prices.columns = prices.columns.str.lower()
    prices.index = pd.to_datetime(prices['date'])
    prices = prices.sort_index()
    return prices

def cut_tail_and_head (daily_returns, tailCut=0.001, headCut=0.999): # the default numbers exclude stock split effect and extreme moves
    ''' cut tail and head of returns given tail and head quantiles '''
    tail = daily_returns.quantile(tailCut)
    head = daily_returns.quantile(headCut)
    daily_returns = daily_returns[daily_returns > tail]
    daily_returns = daily_returns[daily_returns < head]
    return daily_returns

def predicted_returns (daily_returns, lag, cycle):
    ''' 
        calculate Squared of Mean Square Errors (mean standad error) 
        between actural returns with lag days and predicted returns using past cycle*lag data points
    ''' 
    # transform to log of returns for easier calculations multiplication ==> summation
    log_daily_returns = np.log(1+daily_returns) 
    # calc returns with given lag, which is rolling sum of returns with window=lag
    actual_returns = log_daily_returns.rolling(window=lag).sum().rename("actual_return")
    # calc predicted returns by taking rolling mean of past cycles, then align to returns through shifting lag periods
    predicted_returns = actual_returns.rolling(window=lag*cycle, min_periods=1).mean().rename("predicted_return")
    # align predicted returns to returns by shifting lag periods
    predicted_returns = predicted_returns.shift(lag)
    # make dataframe from actural_r and predicted_r and calc errors
    returns = pd.concat ([actual_returns, predicted_returns], axis=1)
    returns = returns.assign (error = lambda x: x.predicted_return - x.actual_return)
    # calc mean square returns of errors
    return returns

def optimal_cycle (stock_daily_prices, return_period, tailCut=0.01, headCut=0.99, cycle_penalty=0.001):
    ''' 
        finds optimal cycle for given stock daily prices and return period in days.
        @param tailCut, headCut: [number 0 to 1] can give tailCut and headCut (in quantile) to censor the extreme low and high daily returns.
        @param cycle_penalty: [small number] determines the penalty for having bigger cycle as in penalty*cycle
        @return cycle: [number] return the optimal cycle
    '''
    # calculate daily returns, censor them to cut extreme low and high daily returns, and modify lag
    daily_returns = prices.pct_change().dropna()
    daily_returns = cut_tail_and_head (daily_returns, tailCut, headCut)
    lag = return_period * (headCut-tailCut)
    max_cycle = round(len(daily_returns)/(lag))
    # calculate the predicted returns and mean of errors for each cycle, then transform to dataframe 
    standard_deviations_df = {
        cycle: predicted_returns(daily_returns, math.ceil(lag), cycle).abs().mean() 
        for cycle in range(1, max_cycle)
    }
    standard_deviations = pd.DataFrame.from_dict(standard_deviations_df, orient='index').rename_axis('cycle')
    #calculate errors taking into account the penalty attn: index is cycle
    errors = standard_deviations['error']*(1 + cycle_penalty*standard_deviations.index)
    return errors.idxmin() # return index of minimum error



price_table = pd.read_csv("/home/invisement/PROJECTS/Temp/spy.txt")
price_table.columns = price_table.columns.str.lower()

stock = "IBM"
price_table = fetch_EOD_price_table (stock)

prices = price_table[mapper['price']].sort_index(ascending=True)

for lag in range(1, 300, 10):
    print(optimal_cycle(prices, lag, tailCut=0.01, headCut=0.99, cycle_penalty=0.01))

prices.shape

