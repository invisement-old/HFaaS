'''
extracts data from sec submission in xml format and converts to dataframe, then cleans, denormalize and saves as csv files.
- extract: downloads the file, calls other functions, denormalize data, and saves. 
- extract_flat_dicts_from_sec_xml: for extracting data from xml page in dataframe format
- xml_to_dict: converts xml tags and attributes into collection of key-value pairs
- refs_to_df: reshapes and reforms reference data that are like dimesion/reference tables.
- facts_to_df: reshapes and cleans fact-table-like dataframes.
'''

import xml.etree.ElementTree as etree
from typing import List, Dict
import pandas as pd
import numpy as np
import requests
import time

from app import * # import global variables

URL = str
PRIMES = (str, int, float, bool)
PAIRS = Dict[str, str]
DICTS = List[PAIRS]
DICDIC = Dict[str, PAIRS]

def extract (sec_xml_page):
    ''' convert xml_page (in byte) to dicts format, convert them to dataframe, denormalize and clean'''
    groups = extract_flat_dicts_from_sec_xml (sec_xml_page) # extract key-value pairs from xml
    facts = [df for g, df in groups.items() if g in FACT_GROUPS]
    refs = [df for g, df in groups.items() if g in REF_GROUPS]
    fact = pd.concat(facts)
    ref = pd.concat(refs)
    fact = fact.join (ref , on='context').filter(SEC_COLS)
    return fact

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
                dic['tag'] = s[1]
                dic['value'] = dic[key]
                del (dic[key])
    df = pd.DataFrame(facts).rename(columns=str.lower).rename(columns={'unitref': 'unit', 'contextref': 'context'})
    if 'unit' in df.columns:
        df['unit'] = df['unit'].str.replace('.*[0-9_ ]+', '')
    return df

def xml_to_dict (xml, dic: PAIRS) -> PAIRS:
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
    ''' from ref DICTS, extract context dataframe with columns: cik identifier, date, and number of quarters.'''
    context = pd.DataFrame(refs) # convert dicts to dataframe
    ref_cols = ['id', 'identifier', 'instant', 'startdate', 'enddate'] # targeted columns
    col_match = {next((i for i in context.columns if i.lower().endswith(col)), None):col for col in ref_cols} # match context column names with ref_cols
    context = context.rename(columns = col_match).filter(ref_cols).set_index('id').rename(columns={'identifier': 'cik'}) # select ref_cols and clean
    for col in ['startdate', 'enddate']: # to_datetime
        context[col] = pd.to_datetime(context[col], errors='coerce')
    context['qtrs'] = (context['enddate']-context['startdate'])/np.timedelta64(3, 'M') # calculate durations (in quarter) 
    context['qtrs'] = context['qtrs'].round() # round it up
    context['date'] = pd.to_datetime(context['enddate'].fillna(context['instant']), errors='coerce').dt.strftime("%Y%m%d") # col date is either enddate or instant, used to_datetime to hack NAs
    return context[['cik', 'date', 'qtrs']]

