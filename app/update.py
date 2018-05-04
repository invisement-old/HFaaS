''' The module is responsible mostly for updating content on server by calling other underlying 
modules. It is the interface between module functionality and outside world (data sources and data storages)
'''

import app.stmt as st
from app import *
import pandas as pd
import os

cik2ticker = pd.read_csv(CIK2TICKER, dtype=str).drop_duplicates('CIK').set_index('CIK')['Symbol']
tmpl = pd.read_csv (STMT_TEMPLATE).set_index('tag').filter(['tag', 'item', 'loc'])

def update_sec(cik_file, since=20100101):
    ''' from sec file in cik_file creates quartely and yealry secs and save'''
    sec = pd.read_csv(cik_file).query('date > @since')
    q, y = st.make_quarterly_yearly_sec (sec)
    cik = os.path.basename(cik_file).split('.')[0]
    ticker = cik2ticker.get(cik, cik)
    q_name = str(ticker)+".csv"
    replace_old(q_name, q.drop('qtrs', axis=1), folder=QUARTERLY_FOLDER, key=['period', 'tag', 'unit'])
    y_name = str(ticker)+".csv"
    replace_old(y_name, y.drop('qtrs', axis=1), folder=YEARLY_FOLDER, key=['period', 'tag', 'unit'])

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


def make_stmt (fin_path, tmpl): ## fins comes from q or y
    stmts = pd.read_csv(fin_path).join(tmpl, on='tag', how='inner')
    stmts = stmts.dropna(subset=['item']).drop_duplicates(['period', 'item'], keep='last')
    stmts = stmts.set_index(['loc', 'item', 'period'])['value']
    stmts = stmts.unstack('period')
    path, name = os.path.split(fins)
    stmts.to_csv(path+'-stmt/'+name)
    return



