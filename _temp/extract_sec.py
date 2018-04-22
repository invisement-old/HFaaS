'''
extract dataframe sec from SEC zip files
    - extract(sec_unzip_path): extract sec dataframe from unzip path
    - update(): extracts all new sec zip files and update sec file
    - to_fiscal(): converts date to fiscal quarter of company
usage: update()
'''

def update ():   
    ''' find new sec zip files, extract them, update old sec with new secs, archive old sec and new zip files '''
    sec = read_old_sec_and_archive_it() 
    new_urls = find_new_secs()
    for url in sorted(new_urls):
        try: # extract new sec and update sec
            print ("Extracting", url, "and updating sec.")
            req = requests.get (url) # get zip file from url 
            zipfile.ZipFile(io.BytesIO(req.content)).extractall(TEMP) # unzip content to TEMP
            new_sec = extract (sec_unzip_path = TEMP) # extract new sec
            sec = pd.concat([sec, new_sec], axis=0, join='outer') # append to sec
            sec = sec.drop_duplicates(subset=SEC_KEY, keep='last') # drop duplicates
            sec.to_csv(SEC_FILE, index=False)
            open(ARCHIVE_PATH + os.path.basename(url), 'wb').write(req.content) # write zip file to archive 
        except Exception as e:
            print("ERROR: extraction or update was not possible for", url, "error message:", e)

import requests, zipfile, io, pandas as pd, numpy as np, lxml.html as html, os, typing, shutil

SEC_DATA_SETS_INDEX = "https://www.sec.gov/dera/data/financial-statement-data-sets.html"
ARCHIVE_PATH = ".archive/"
TEMP = "./.temp/"
URL = str
PATH = str
SEC_KEY = ['cik', 'stmt', 'item', 'date', 'qtrs', 'uom']
SEC_COLS = SEC_KEY + ['value', 'fiscal', 'report', 'line']
CIK2TICKER_FILE = "./data/cik2ticker.csv"
SEC_FILE = "data/sec.csv"
ENCODING = 'latin'

def read_old_sec_and_archive_it():
    try:
        old_sec = pd.read_csv(SEC_FILE)
        print ("old sec was found")
        shutil.move(SEC_FILE, ARCHIVE_PATH+os.path.basename(SEC_FILE))
        print ("old sec file was archived in sec_archive")
    except Exception as e:
        print ("old sec file was not found so we assumed it does not exist.", e)
        old_sec = None
    return old_sec

def find_new_secs() -> typing.List[URL]:
    ''' scrapes all sec zip files from url of sec data sets 
        and excludes the files that are in sec archive '''
    zip_urls = html.fromstring(requests.get(SEC_DATA_SETS_INDEX).content).xpath('//tr/td/a//@href') # read sec page and find urls in table
    zip_urls = ["https://www.sec.gov"+url for url in zip_urls]
    archives = os.listdir(ARCHIVE_PATH) # get all sec files in archive
    new_zip_files = [url for url in zip_urls if os.path.basename(url) not in archives] # exclude archives from urls
    return new_zip_files

def extract (sec_unzip_path: PATH = TEMP, encoding=ENCODING) -> pd.DataFrame:
    ''' sec zip file is unzipped to folder, extract it to SEC dataframe format with desired columns '''
    ##### read num, pre, sub, cik2ticker; 
    num = (
        pd.read_table(TEMP+"num.txt", encoding=encoding) 
        .query('value.notnull() & value != 0')
        #.query('coreg.notnull()') # filter submitted as a coregistrant
        #num[num['ddate']<=int(dt.now().strftime('%Y%m%d'))] # filter values for future date
    )
    pre = (
        pd.read_table(TEMP+"pre.txt", encoding=encoding)
        .query('plabel.notnull()')
        #.query('stmt==["BS", "IS", "CF", "EQ", "CI"]')
    )
    #tag = pd.read_table (secPath+"tag.txt", encoding=encode)
    sub = (
        pd.read_table(TEMP+"sub.txt", encoding=encoding)
        #.query('form==["10-K", "10-Q", "10-K/A", "10-Q/A"]')
    )
    ##### merge all to df; create stamp and fiscal; filter desired columns; 
    new_sec = num.merge(pre, on=["adsh", "tag", "version"], how="inner"
        ).merge(sub, on="adsh", how="inner"
        ).rename(columns={'plabel':'item', 'ddate':'date'}
        ).assign(fiscal = lambda x: to_fiscal(x.date, x.fye)
        ).filter(SEC_COLS)
    return new_sec

def to_fiscal (dates: int, fYearEnd: int) -> int:
    ''' Calculates the fiscal quarter for each date given the endyear'''
    month = dates // 100 % 100
    fmonth = fYearEnd // 100
    fquarter = (11 + month - fmonth) // 3 % 4 + 1
    return fquarter
