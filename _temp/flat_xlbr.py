''' 
flat-xlbr extracts sec xlbr submission files and converts them to useful flat dictionary formats and serialize them to json and saves them. 
    - extract_dicts_from_xml extracts dicts from xml, then, segregate_facts_refs segregates reference dicdic from facts (or facts) dicdic
    - extract_flat_tags extracts flat dictionary (dicdic) from MetaLinks.json of the sec submission, dicdic_to_df converts it to pandas.DataFrame
    - xml_to_dict converts an xml to doctionary. if PASS_NAMES = True, it will pass names
    - find_tag finds branch of dict (inner dict) of a nested dict for given tag
    - collect_leaf extracts the most inner key values of a nested dict as a new dict
    - create_context converts refs DICDIC to context dataframe
'''

from xml.etree import ElementTree as et
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
ID_VAR = 'id'
COLS = ['cik', 'period', 'item', 'value', 'unit', 'decimals', 'date', 'qtrs']
FACT_GROUPS = ['gaap', 'dei']
REF_GROUPS = ['context']

########## SECOND PART
def find_tag (tag: str, dic: Dict) -> Dict:
    out = dic.get(tag)
    if out is None:
        for inner in dic.values():
            if isinstance(inner, dict):
                out = find_tag (tag, inner)
                if out is not None:
                    return out
    return out

def collect_leaf (dic: Dict, out, branch='') -> PAIRS:
    ''' flats any dictionary by extracting the inner key values, recursively'''
    for k,v in dic.items():
        if PASS_NAMES and branch != '':
            k = k + PASS_NAMES_SEP + branch
        if isinstance(v, PRIMES):
            out[k] = v
        elif v in (None, [], {}):
            continue
        elif isinstance(v, list):
            v = {k+str(i):e for i,e in enumerate(v)}
            collect_leaf(v, out, '')
        elif isinstance(v, dict):
            collect_leaf(v, out, k)
        else:
            print ("Warning! this is weird: ", v, type(v))
    return out

def tags_to_df (tags):
    tags =pd.DataFrame.from_dict(tags, orient='index')
    cols = ['label', 'parentTag', 'order',  'weight'] # extras: 'crdr', 'terseLabel', 'totalLabel', 'root'
    presentations = [col for col in pre.columns if 'presentation' in col]
    for p in presentations:
        tags2[p] = tags2[p].str.split('_', expand=True).iloc[:, 1]
        tags2[p] =  tags2[p].str.replace('Disclosure.*', 'Disclosure')
    reports = [tags2[cols].assign(report=tags2[p]).dropna(subset=['report']) for p in presentations] # create a list of reports containing not missing records
    tags_df = pd.concat(reports)
    tags_df.index.name = 'item' 
    return tags



SEC_FOLDER = '~/Documents/'
items.to_csv (SEC_FOLDER + xml_name.replace('_html.xml', '_items.csv').replace('.xml', '_items.csv'))
    try:
        JSON_URL = url[0:url.rfind('/')+1] + "MetaLinks.json"
        response = requests.get(JSON_URL)
        response.raise_for_status()
        json = response.json() 
    except Exception as e:
        print('Error! could not fetch MetaLinks.json from', url)
        print(e)
    ''' Extracts meta data from metaLink file of SEC submissions. But it is flat dicts and easy to work '''
    tags = find_tag (tag, json) 
    tags_dict = {k:collect_leaf(v, {}) for k,v in tags.items()}
    tags_df = tags_to_df (tags)
    tags_df.to_csv (SEC_FOLDER + xml_name.replace('_html.xml', '_tags.csv').replace('.xml', '_tags.csv'))
    print('everything went well and data and tags csv files saved in', SEC_FOLDER)
    return


