'''
extracts data from sec submission in xml format and converts to dataframe, then cleans, denormalize and saves as csv files.
- extract: downloads the file, calls other functions, denormalize data, and saves. 
- extract_flat_dicts_from_sec_xml: for extracting data from xml page in dataframe format
- xml_to_dict: converts xml tags and attributes into collection of key-value pairs
- refs_to_df: reshapes and reforms reference data that are like dimesion/reference tables.
- facts_to_df: reshapes and cleans fact-table-like dataframes.
'''

from lxml import etree
from typing import List, Dict
import pandas as pd
import numpy as np
import requests
import time

URL = str
PRIMES = (str, int, float, bool)
PAIRS = Dict[str, str]
DICTS = List[PAIRS]
DICDIC = Dict[str, PAIRS]
XMLNS_SEP = '_'
PASS_NAMES = False
STRIP = True
PASS_NAMES_SEP = '.'
COLS = ['cik', 'period', 'item', 'value', 'unit', 'decimals', 'date', 'qtrs']
FACT_GROUPS = ['gaap', 'dei']
REF_GROUPS = ['context']
SEC_FOLDER = '~/Documents/'

def extract (url: URL) -> None:
    ''' download xml page, convert xml to dicts format, convert them to dataframe, denormalize and clean, and save as csv files'''
    try: # download xml page containing SEC submission data
        table = pd.read_html(url, header=0)[1] # read table of contents
        xml_name = table['Document'][table['Description'].str.contains('instance|.ins', case=False)].iloc[0] # select file name for xbrl instance
        xml_url = url[0:url.rfind('/')+1] + xml_name # add name to url base
        response = requests.get(xml_url) # get the xml page text
        response.raise_for_status() # raise if error
        xml_page = response.content
    except Exception as e:
        print('Error! could not fetch xbrl instance xml from', url)
        print(e)
        return
    groups = extract_flat_dicts_from_sec_xml (xml_page) # extract key-value pairs from xml
    for g in ['gaap']: # converts values to numeric and clean NAs
        groups[g]['value'] = pd.to_numeric(groups[g]['value'], errors='coerce', downcast='float')
        groups[g] = groups[g].dropna(subset=['value'])
    for ref in REF_GROUPS: # denormalize fact dataframes using refs
        for fact in FACT_GROUPS:
            groups[fact] = groups[fact].join(groups[ref], on=ref).filter(COLS)
    for g in FACT_GROUPS: # save as csv
        groups[g].to_csv (SEC_FOLDER + xml_name.replace('_html.xml', '').replace('.xml', '')+'_'+g+'.csv', index=False)
    print('Everything went successfully. All csv files for gaap and dei and context were saved in', SEC_FOLDER, 'for', xml_name)
    return

def extract_flat_dicts_from_sec_xml (xml: bytes) -> DICDIC:
    ''' converts sec xml submission file to list of dictionary that has all components. a.b means namespance a and name b. '''
    xml = xml.replace(b'xmlns', b'xns').replace(b':', bytes(XMLNS_SEP, 'utf-8')) # hack for annoying xml namespace problem
    #parser = etree.XMLParser(ns_clean=True, remove_blank_text=True, collect_ids=False)
    nodes = etree.fromstring(xml)
    groups = {group:[xml_to_dict(node, {}) for node in nodes if group in node.tag.lower()] for group in FACT_GROUPS+REF_GROUPS}
    for g in REF_GROUPS: # convert to dataframe and clean using refs_to_df
        groups[g] = refs_to_df (groups[g])
    for g in FACT_GROUPS: # convert to dataframe and clean using facts_to_df function
        groups[g] = facts_to_df (groups[g])
    return groups

def facts_to_df (facts: DICTS) -> pd.DataFrame:
    ''' converts DICTS facts to dataframe'''
    for dic in facts:
        for key in list(dic.keys()):
            s = key.split(XMLNS_SEP) # columns with XMLNS_SEP are variables
            if len(s)==2: # a hack to create long dataframe instead of pushing all fields to columns
                dic['item'] = s[1]
                dic['value'] = dic[key]
                del (dic[key])
    return pd.DataFrame(facts).rename(columns=str.lower).rename(columns={'unitref': 'unit', 'contextref': 'context'})

def xml_to_dict (xml: et, dic: PAIRS) -> PAIRS:
    ''' Recursively finds the most inner key:value pairs and collects them in a dictionary '''
    element_dict = dict(xml.attrib, **{xml.tag:xml.text}) # make a dictionary out of et attributes and tag
    if STRIP==True: # clean and strip dicts
        element_dict = {k:v.strip() for k,v in element_dict.items() if v and v.strip()!=''}
    dic.update(element_dict)
    for child in xml: # recursive for childs
        if PASS_NAMES:
            child.tag = child.tag + PASS_NAMES_SEP + xml.tag
        dic = xml_to_dict (child, dic)
    return dic

def refs_to_df (refs: DICTS) -> pd.DataFrame:
    ''' from ref DICTS, extract context dataframe with columns: cik identifier, date and period, and number of quarters.'''
    context = pd.DataFrame(refs) # convert dicts to dataframe
    ref_cols = ['id', 'identifier', 'instant', 'startdate', 'enddate'] # targeted columns
    col_match = {next((i for i in context.columns if i.lower().endswith(col)), None):col for col in ref_cols} # match context column names with ref_cols
    context = context.rename(columns = col_match).filter(ref_cols).set_index('id').rename(columns={'identifier': 'cik'}) # select ref_cols and clean
    for col in ['startdate', 'enddate']: # to_datetime
        context[col] = pd.to_datetime(context[col])
    context['qtrs'] = (context['enddate']-context['startdate'])/np.timedelta64(3, 'M') # calculate durations (in quarter) 
    context['qtrs'] = context['qtrs'].round() # round it up
    context['date'] = pd.to_datetime(context['enddate'].fillna(context['instant'])) # col date is either enddate or instant, used to_datetime to hack NAs
    context['period'] = context['date'].dt.to_period('Q') # convert to quarters
    return context[['cik', 'period', 'date', 'qtrs']]

