''' update company info dataframe from web sources'''

import re, requests, pandas as pd, numpy as np

COMPANY_FILE = 'data/sec/company.csv.gz'
#COMPANY_URL = "https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange={}&render=download"
COMPANY_LISTING = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqtraded.txt"
SEC_CIK_URL = 'http://www.sec.gov/cgi-bin/browse-edgar?CIK={}&Find=Search&owner=exclude&action=getcompany'
CIK_RE = re.compile(r'.*CIK=(\d{10}).*')    
COMPANY_COLS = ['CIK', 'Symbol', 'Name', 'Exchange', 'SIC', 'IRS', 'Sector', 'industry', 'State']

def update_company_file ():
    ''' update company info file '''
    # read old compnay file, append to company list, prepare old ticker2cik
    try:
        old_company = pd.read_csv(COMPANY_FILE)
        ticker2cik = old_company.set_index('Symbol')['CIK']
    except Exception as e:
        ticker2cik = pd.DataFrame()
        print(e)
    # read new compnay lists from COMPANY URL, append them together
    try:
        #company_list = [pd.read_csv(COMPANY_URL.format(ex)).assign(Exchange=ex).filter(regex='^[^Unnamed]') for ex in ['NYSE', 'NASDAQ', 'AMEX']]
        #company = pd.concat(company_list)
        company = pd.read_csv(COMPANY_LISTING, sep='|').filter(['Symbol', 'Security Name', 'Listing Exchange', 'ETF'])
        company.columns = ['Symbol', 'Name', 'Exchange', 'ETF']
    except Exception as e:
        print ('Error! Counld not download new company info from nasdaq.com, make sure connection works! \n', e)
        return
    # find CIKs from old ticker2cik file
    company = company.join(ticker2cik, on='Symbol', how='left') # find CIK from old file
    # for missing or invalid CIK, scrape them from SEC
    cond = (company['CIK'].isnull()) | (company['CIK']<=0) # invalid or missing CIKs
    cond = cond & (company['ETF']=='N') # exclude ETF symbols
    cond = cond & ~(company['Symbol'].str.contains('[^a-zA-Z]', na=True)) # exclude non characters
    company.loc[cond, 'CIK'] = company.loc[cond, 'Symbol'].apply(lambda x: scrape_CIK_from_SEC(x))
    # concat old and new company files together, filter desired columns, cast CIK col to int type
    company = pd.concat ([company, old_company], join='outer')
    company = company.filter(COMPANY_COLS)
    company['CIK'] = company['CIK'].fillna(0).astype(int) # missing values makes int
    # remove duplicates by getting the first valid vallue for each group, save copmany file
    company = first_valids(company, index=['Symbol'])
    company.to_csv(COMPANY_FILE, index=False, compression="gzip") # Write
    return company

def first_valids(df, index):
    ''' update new dataframe missings from old one '''
    groups = df.groupby(index)
    for _, group in groups:
        group = group.bfill()
    return groups.first().reset_index()

def scrape_CIK_from_SEC (ticker):
    ''' get ticker by scraping SEC website '''
    print("lets scrape CIK for", ticker, "from SEC website")
    resp = requests.get(SEC_CIK_URL.format(ticker), stream = True)
    results = CIK_RE.findall(resp.text)
    if len(results) > 0: 
        cik = int(re.sub('\.[0]*', '.', results[0]))
        return cik

def test():
    print(COMPANY_FILE)

