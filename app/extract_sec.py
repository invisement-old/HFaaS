
import pandas as pd
import requests
import zipfile
import io, os
from lxml import html
import app.sec_xml as sx
import json

SEC_DATA_SETS_INDEX = "https://www.sec.gov/dera/data/financial-statement-data-sets.html"
TEMP = ".temp/"
SEC_FOLDER = 'data/sec/'
ARCHIVE_DATA = 'archive-data/'
SEC_KEY = ['tag', 'date', 'qtrs', 'unit']
ENCODING = 'latin'
NEW_SUBMISSIONS = 'https://www.sec.gov/Archives/edgar/full-index/form.idx'
OLD_SUBMISSIONS = 'archive-data/form_idx.csv'
DATA_SETTING = 'data/data-setting.json'
SEC_ZIP_ARCHIVES = 'sec_zip_archives'

def update_sec_from_zips ():
    ''' find new sec zip files, extract them, update old sec with new secs, archive old sec and new zip files '''
    try:
        with open(DATA_SETTING, 'r') as jfile:
            setting = json.load(jfile)
    except:
        print ("Error! it seems you do noy have ", DATA_SETTING, "file. Copy one or create empty json object {}")
        raise Exception("create data setting file")
    archives = setting.get(SEC_ZIP_ARCHIVES, [])
    new_urls = find_new_zip_secs(archives)
    for url in sorted(new_urls):
        try: # extract new sec and update sec
            print ("Extracting", url, "and updating sec.")
            req = requests.get (url) # get zip file from url 
            zipfile.ZipFile(io.BytesIO(req.content)).extractall(TEMP) # unzip content to TEMP
            num = pd.read_csv (TEMP+'num.txt', sep='\t', encoding=ENCODING).rename(columns={'ddate': 'date', 'uom': 'unit'})
            sub = pd.read_csv (TEMP+'sub.txt', sep='\t', encoding=ENCODING).set_index('adsh')['cik'].astype(str)
            num = num.join(sub, on='adsh', how='inner')
            print ("dispaching to files started")
            for cik, new in num.groupby('cik'):
                update_and_replace(new, cik)
            print("archiving the zip file.")
            archives = archives + [os.path.basename(url)]
            setting[SEC_ZIP_ARCHIVES] = archives
            with open(DATA_SETTING, 'w+') as jfile:
                json.dump(setting, jfile)
            # f = open(ARCHIVE_DATA + os.path.basename(url), 'wb')
            # f.write(req.content) # write zip file to archive 
            # f.close()
        except Exception as e:
            print("ERROR: extraction or update was not possible for", url, "error message:", e)
    return

def find_new_zip_secs(archives):
    ''' scrapes all sec zip files from url of sec data sets 
        and excludes the files that are in sec archive '''
    zip_urls = html.fromstring(requests.get(SEC_DATA_SETS_INDEX).content).xpath('//tr/td/a//@href') # read sec page and find urls in table
    zip_urls = ["https://www.sec.gov"+url for url in zip_urls]
    # archives = os.listdir(ARCHIVE_DATA) # get all sec files in archive
    new_zip_urls = [url for url in zip_urls if os.path.basename(url) not in archives] # exclude archives from urls
    return new_zip_urls

'''
def dispatch_new_zip_sec ():
    num = pd.read_csv (TEMP+'num.txt', sep='\t', encoding=ENCODING).rename(columns={'ddate': 'date'})
    sub = pd.read_csv (TEMP+'sub.txt', sep='\t', encoding=ENCODING).set_index('adsh')['cik']
    num = num.join(sub, on='adsh', how='inner')
    for cik, new in num.groupby('cik'):
        file_name = SEC_FOLDER+cik+'.csv.gz'
        new = new.sort_values(SEC_KEY+['coreg'], na_position='first')
        new = new.filter(SEC_KEY+['value'])
        try:
            old = pd.read_csv(file_name, compression='gzip')
        except Exception:
            old = None
            print('Warning, we could not find file ', file_name, ' so we created a new file.')
        new = pd.concat([new, old]).drop_duplicates(SEC_KEY)
        new.to_csv(file_name, index=False, compression='gzip')
    return
'''

############# PART TWO: UPDATE XMLS FILES
def update_sec_from_xml ():
    submissions = pd.read_fwf(NEW_SUBMISSIONS, skiprows=[0,1,2,3,4,5,6,7, 9]).rename(columns = {'File Name': 'File', 'Form Type': 'Form'})
    files = find_new_xml_submissions (submissions)
    path = files.apply(os.path.dirname)
    name = files.apply(os.path.basename)
    #cik = name.str.split('-|_', expand=True)[0]
    adsh = name.str.replace('-|\..*', '') # replace 123-1234-234.txt with 1231234234
    urls = 'https://www.sec.gov/Archives/' + path +'/' + adsh + '/'+ name.str.replace('\..*', '-index.html')
    #urls.index = urls.index.astype(str).str.zfill(10)
    for cik, url in urls.iteritems():
        try:
            #print("extracting: ", url)
            new = sx.extract (url)
            new['value'] = pd.to_numeric(new['value'], errors='coerce', downcast='float')
            new = new.dropna(subset=['value'])
            new = new.filter(SEC_KEY+['value']).drop_duplicates(SEC_KEY)
            update_and_replace (new, cik)
        except Exception:
            print("ERROR! Could not update ", cik, "from url ", url)
    submissions.to_csv (OLD_SUBMISSIONS, index=False)
    return

def find_new_xml_submissions (submissions):
    #submissions = pd.read_fwf(NEW_SUBMISSIONS, skiprows=[0,1,2,3,4,5,6,7, 9]).rename(columns = {'File Name': 'File', 'Form Type': 'Form'})
    try:
        old = pd.read_csv (OLD_SUBMISSIONS)
        #old = pd.read_fwf(OLD_SUBMISSIONS, skiprows=[0,1,2,3,4,5,6,7, 9]).rename(columns = {'File Name': 'File', 'Form Type': 'Form'})
        used = submissions['File'].isin(old['File'])
        submissions = submissions[~used]
    except Exception:
        print ('WARNING! could not find old submission file ', OLD_SUBMISSIONS)
    submissions['CIK'] = submissions['CIK'].astype(str)
    submissions = submissions.query('Form in ["10-K", "10-Q"]').set_index('CIK')['File']
    return submissions

def update_and_replace (new, cik):
    file_name = SEC_FOLDER+cik+'.csv.gz'
    new = new.filter(SEC_KEY+['value'])
    try:
        old = pd.read_csv(file_name, compression='gzip')
    except Exception:
        old = None
        print('Warning, we could not find file ', file_name, ' so we created a new file.')
    new = pd.concat([new, old]).drop_duplicates(SEC_KEY)
    new.to_csv(file_name, index=False, compression='gzip')
    return

