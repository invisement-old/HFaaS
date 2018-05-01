''' The module is responsible mostly for updating content on server by calling other underlying 
modules. It is the interface between module functionality and outside world (data sources and data storages)
'''

import app.stmt as st
from app import *
import pandas as pd
import os

cik2ticker = pd.read_csv(CIK2TICKER, dtype=str).set_index('CIK')['Symbol']
tmpl = pd.read_csv (STMT_TEMPLATE).set_index('tag').filter(['stmt', 'tag', 'item', 'line'])


def update_finset(cik_file):
    ''' from sec file in cik_file creates quartely and yealry finsets and saves to FINSET_FOLDER'''
    sec = pd.read_csv(cik_file)
    q, y = st.make_quarterly_yearly_finset (sec)
    cik = os.path.basename(cik_file).split('.')[0]
    ticker = cik2ticker[cik]
    q_name = str(ticker)+"-"+"Q.csv"
    replace_old(q_name, q.drop('qtrs', axis=1), folder=FINSET_FOLDER, key=['period', 'tag', 'unit'])
    y_name = str(ticker)+"-"+"Y.csv"
    replace_old(y_name, y.drop('qtrs', axis=1), folder=FINSET_FOLDER, key=['period', 'tag', 'unit'])

def replace_old (old_name, new, folder, key, keep='first'):
    ''' finds old dataframe (if not creates and empty old), updates it with new dataframe, gets rid of duplicates and saves back.'''
    try:
        old = pd.read_csv(folder+old_name)
    except Exception:
        old = None
        print("could not file old file, created a new file for ", old_name)
    new = pd.concat([new, old]).drop_duplicates(key, keep=keep)
    new.to_csv (folder+old_name, index=False)
    print ("Success! file ", old_name, " updated successfully!")





