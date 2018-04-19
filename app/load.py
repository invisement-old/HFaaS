
import pickle, pandas as pd

EXTRACTED_SEC = "data/sec.csv"
COMPANY_FILE= "data/company.csv"
SEC_KEY = ['ticker', 'stmt', 'item', 'date', 'qtrs', 'fiscal', 'uom']
SEC_API_FILE = "data/sec.torshi"

def load_sec():
    '''to transform and load sec dataframe as a dictionary with ticker keys to use in api web server'''
    sec = pd.read_csv(EXTRACTED_SEC)
    sec = add_ticker(sec)
    sec = sec.sort_values(['ticker', 'stmt', 'line']
        ).dropna(subset=['ticker', 'value']
        ).drop_duplicates(subset=SEC_KEY)
    sec = {ticker:df for ticker, df in sec.groupby('ticker')}
    with open(SEC_API_FILE, 'wb') as f:
        pickle.dump(sec, f)
    print("sec file is cleaned and pickled in", SEC_API_FILE)

def add_ticker(sec):
    cik2ticker = pd.read_csv(COMPANY_FILE).set_index('CIK')['Symbol'].rename('ticker')
    sec = sec.join(cik2ticker, on="cik", how='left')
    return sec

