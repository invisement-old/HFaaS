''' utilities and functions to read, write, scrape, and upload. 
    It is the interface gate of app module to the environment system: file system or web '''

from app import *
import pandas as pd
import requests
import zipfile
import io, os
from lxml import html
import json

def read_archived_sec_zips ():
    try:
        with open(DATA_SETTING, 'r') as jfile:
            setting = json.load(jfile)
    except:
        print ("Error! it seems you do not have ", DATA_SETTING, "file. Copy one or create empty json object {}")
        raise Exception("create data setting file")
    return setting.get(SEC_ZIP_ARCHIVES, [])

def scrape_sec_zip_urls ():
    response = requests.get(SEC_DATA_SETS_INDEX)
    response.raise_for_status()
    zip_urls = html.fromstring(response.content).xpath('//tr/td/a//@href') # read sec page and find urls in table
    zip_urls = ["https://www.sec.gov"+url for url in zip_urls]
    return zip_urls

def read_zip_sec (sec_zip_url):
    response = requests.get (sec_zip_url) # get zip file from url 
    response.raise_for_status()
    zipped = io.BytesIO(response.content)
    zipfile.ZipFile(zipped).extractall(TEMP) # unzip content to TEMP
    sub = pd.read_csv (TEMP+'sub.txt', sep='\t', encoding=SEC_ENCODING, dtype=str).set_index('adsh')['cik']
    num = pd.read_csv (TEMP+'num.txt', sep='\t', encoding=SEC_ENCODING, dtype=str)
    num = num.join(sub, on='adsh', how='inner').rename(columns={'ddate': 'date', 'uom': 'unit'})
    num = num.set_index('cik').filter(SEC_COLS)
    return num

def update_df (new, old_file, key, keep='first'):
    try:
        old = pd.read_csv(old_file, dtype=DATATYPE)
    except Exception:
        old = None
        print("could not find old file, created a new file for ", old_file)
    new = pd.concat([new, old]).drop_duplicates(key, keep=keep)
    new.to_csv(old_file, index=False, date_format=DATE_FORMAT)
    print ("Success! file ", old_file, " updated successfully!")

def archive_sec_zip (new_sec_zip_basenames):
    with open(DATA_SETTING, 'r+') as jfile:
        setting = json.load(jfile)
        setting[SEC_ZIP_ARCHIVES] = setting.get(SEC_ZIP_ARCHIVES, []) + new_sec_zip_basenames
        jfile.seek(0)
        json.dump(setting, jfile)
        jfile.truncate()

def scrape_xml_submissions_page (path):
    try:
        submissions = pd.read_csv(path, sep='|', skiprows=[0,1,2,3,4,5,6,7, 9], dtype=DATATYPE)
        submissions = submissions.rename(columns = {'Filename': 'file', 'Form Type': 'form', 'CIK': 'cik'})
        submissions = submissions.query('form in ["10-K", "10-Q", "10-K/A", "10-Q/A"]')
        urls = 'https://www.sec.gov/Archives/'+ submissions['file']
        urls = urls.str.replace('-|.txt', '')+'/index.json'
        submissions = submissions.assign(file = urls)
    except Exception:
        print('did not find submissions at ', path)
        submissions = pd.DataFrame(columns = ['file', 'form', 'cik'])
    return submissions

