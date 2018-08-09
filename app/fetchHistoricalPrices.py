
import requests
import pandas as pd
import fix_yahoo_finance as yf

companyListPathes = ["~/Temp/companylistNASDAQ.csv", "~/Temp/companylistNYSE.csv", "~/Temp/companylistAMEX.csv"]

links = {
    'investopedia': "https://www.investopedia.com/markets/api/partial/historical/?Symbol={}&Type=Historical+Prices&Timeframe=Daily&StartDate=Nov+28%2C+1990&EndDate=Dec+05%2C+2018",
    'alphavantage': "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey=0AP847PM2NU4EJDH&datatype=csv&outputsize=full",
    'financialContent': "http://markets.financialcontent.com/stocks/action/gethistoricaldata?Month=12&Symbol={}&Range=300&Year=2019",
    'yahooDownload': "https://query1.finance.yahoo.com/v7/finance/download/{}?period1=1&period2=2532231439&events=history&crumb=UrdIgSD1ObY&interval=1d",
    'quantprice': "https://quantprice.herokuapp.com/api/v1.1/scoop/period?tickers={}&begin=1960-01-03",
    'yahooDividends': "https://finance.yahoo.com/quote/{}/history?period1=1&period2=2532156400&interval=div%7Csplit&filter=div&frequency=1d",
    'yahoo': "https://finance.yahoo.com/quote/{}/history?period1=0&period2=2532242800&interval=1d&filter=history&frequency=1d"
}


# read company list, get symbols, strip whitespace, and exclude bad names
def cleanSymbols (companyListPath):
    companyList = pd.read_csv(companyListPath)
    symbols = companyList["Symbol"]
    symbols = symbols.str.strip()
    legitNames = symbols.str.contains("^[a-zA-Z0-9]+$")
    symbols = symbols[legitNames]
    return symbols.tolist()
##############################################

def download (symbols, source):
    link = links[source]
    folder = "/home/invisement/Temp/{}/".format(source)
    while len(symbols) > 0:
        symbol = symbols.pop()
        res = requests.get(url)
        if res.status_code != 200:
            print("Error! we sopped downloading at symbol: ", symbol)
            continue
        if len(res.content) < 1000: # if response is not empty or a message
            print("This seems empty, symbol: ", symbol)
            continue
        with open(folder + symbol + ".csv", 'wb+') as file:
            file.write(res.content)
###############################

def downloadHTML (symbols, source):
    link = links[source]
    folder = "/home/invisement/Temp/{}/".format(source)
    while len(symbols) > 0:
        symbol = symbols.pop()
        url = link.format(symbol)
        try:
            dfList = pd.read_html(url, attrs={'data-test': "historical-prices"})
        except Exception as e:
            print ("Error, no table found for symbol: ", symbol)
            continue 
        #out = dfList[0].dropna(subset=["Dividends"])
        if len(out)>0:
            out.to_csv(folder + symbol + ".csv", index=False)
        else:
            print("it seems empty dividends for symbol: ", symbol) 

def downloadYF (symbols, source):
    folder = "/home/invisement/Temp/{}/".format(source)
    while len(symbols) > 0:
        symbol = symbols.pop()
        try:
            out = yf.download(symbol)
        except Exception as e:
            print ("Error, could not fetch price data for symbol: ", symbol)
            continue 
        if len(out)>0:
            out.to_csv(folder + symbol + ".csv")
        else:
            print("it seems empty price data for symbol: ", symbol) 

##################################

symbols = []
for companyListPath in companyListPathes:
    symbols = symbols + cleanSymbols(companyListPath)
symbols = list(set(symbols)) #make unique

source = "yahoo"
downloadYF(symbols, source)

