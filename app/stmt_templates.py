import os
import pandas as pd
from app import *

tmpl = pd.read_csv (STMT_TEMPLATE).set_index('tag').filter(['stmt', 'tag', 'item', 'line'])

#LINK_TO_DOWNLOAD_EXCEL_FILE = http://www.fasb.org/jsp/FASB/Page/SectionPage&cid=1176168807223
systemid_stmt = {
    'stm-soi-pre': 'IS',
    'stm-sfp-cls-pre': 'BS',
    'stm-scf-indir-pre': 'CF',
    'stm-soc-pre': 'CI',
    'stm-sheci-pre':'EQ' } #wrong
stmt_cutoff = {
    'IS': 25,
    'BS': 25,
    'CF': 15,
    'CI': 10,
    'EQ': 10,
    'CP': 10
}

def create_stmt_templates ():
    '''creates general templates for financial statements 
    using most popular tags from sec pre file and ordered by fasb.org taxonomy excel file.'''
    # read taxonomy, select only desired one (from stmt_systemid), drop duplicates, add stmt column, a line (order) column for each stmt
    taxonomy = pd.read_excel(TAXONOMY_EXCEL, sheet_name=1)
    taxonomy = {stmt:taxonomy[taxonomy['systemid'].str.contains(systemid, na=False)].drop_duplicates('name').reset_index(drop=True) for systemid, stmt in systemid_stmt.items()}
    taxonomy = pd.concat(taxonomy, names=['stmt', 'line']).reset_index().rename(columns={'name': 'tag'})
    # read sec num file, make count for each tag, choose most frequent one
    sec = pd.read_csv(SEC_FILE, sep='\t')
    sec = sec['tag'].value_counts().nlargest(100).rename('adsh')
    # merge two dataframe and sort by line, and save
    sec = taxonomy.join(sec, on='tag', how='right').sort_values(['stmt', 'line'])
    sec = sec.groupby('stmt').apply(lambda x: x.nlargest(stmt_cutoff.get(x.name,0), 'adsh')) # cut off for each stmt by stmt_cutoff
    sec = sec.sort_values(['stmt', 'line']).reset_index(drop=True)
    os.rename(STMT_TEMPLATE, ARCHIVE_STMT_TEMPLATE) # move old to archive
    pre.to_csv (STMT_TEMPLATE, index=False) # save new template
    #print('DONE! input taxonomy file: ', TAXONOMY_EXCEL, ' and sec pre.txt file: ', SEC_FILE, 'was used and output file saved in ', STMT_TEMPLATE, ' and old file archived in ', ARCHIVE_STMT_TEMPLATE)
    return

def make_stmts (finset, tmpl)
    stmts = finset.join(tmpl, on='tag', how='inner').dropna(subset=['item'])
    stmts = stmts.drop_duplicates(['period', 'item'], keep='last')
    stmts = stmts.set_index(['stmt', 'line', 'item', 'period'])['value']
    stmts = stmts.unstack('period')
    stmts.to_csv(STMT_FOLDER+finset)
    return stmts


def make_quarterly_yearly_finset (sec, TAG='tag'):
    sec['period'] = pd.to_datetime(sec['date'].astype(str), errors='coerce').dt.to_period('Q')
    sec = sec.sort_values([TAG, 'date'], ascending=False)
    sec = sec.drop_duplicates([TAG, 'period', 'qtrs', 'unit'])
    sec = sec.set_index ('period')
    sec['qtrs']= sec['qtrs'].fillna(0)
    Q_zero = sec.query('qtrs == 0').reset_index().drop_duplicates([TAG, 'period'])
    Y_zero = Q_zero.query('period.dt.quarter == 4')
    Q_one = sec.groupby([TAG, 'unit'], group_keys=False).apply(all_quarters)
    Y_one = Q_one.groupby([TAG, 'unit']).apply(lambda q: q.resample('Y').agg({'date':'last', 'qtrs':lambda x: pd.Series.sum(x,min_count=4), 'value':lambda x: pd.Series.sum(x,min_count=4)})).reset_index()
    Q_one = Q_one.reset_index()
    Q = pd.concat([Q_zero, Q_one])
    Y = pd.concat([Y_zero, Y_one])
    return Q, Y

def all_quarters (group):
    #print(group.shape)
    #print(group)
    quarterly = group.query('qtrs==1')
    quarterly = quarterly.resample('Q').asfreq()
    yearly = group.query('qtrs>1').sort_index()
    missings = quarterly[quarterly['value'].isna()]
    #indices = yearly.index.values.searchsorted(missings.index.values)
    #missings = missings.assign(date = yearly.iloc[indices]['date'])
    for period, row in missings.iterrows():
        try:
            total = yearly.iloc[yearly.index.searchsorted(period)]
            previous_qtrs = [idx for idx in quarterly.index if idx != period and (total.name-total.qtrs) < idx <= total.name]
            previous_values = quarterly.loc[previous_qtrs, 'value'].sum(skipna = False)
            row.value = total.value - previous_values
            row.unit = total.unit
            row.qtrs = 1
            row.date = yearly['date'].get(period)
            row[TAG] = total[TAG]
            quarterly.loc[period] = row
        except Exception:
            pass
    return quarterly


