import os
import pandas as pd
from app import *

def make_quarterly_yearly_sec (sec, TAG='tag'):
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
    Y = pd.concat([Y_zero, Y_one], sort=False)
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


