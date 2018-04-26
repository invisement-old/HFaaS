

### Thses are default global variables (setting) for python apps in this package
SEC_DATA_SETS_INDEX = "https://www.sec.gov/dera/data/financial-statement-data-sets.html"
TEMP = ".temp/"
SEC_FOLDER = 'data/sec/'
ARCHIVE_DATA = 'archive-data/'
SEC_KEY = ['tag', 'date', 'qtrs', 'unit']
SEC_ENCODING = 'latin1'
NEW_SUBMISSIONS = 'https://www.sec.gov/Archives/edgar/full-index/form.idx'
OLD_SUBMISSIONS = 'archive-data/form_idx.csv'
DATA_SETTING = 'data/data-setting.json'
SEC_ZIP_ARCHIVES = 'sec_zip_archives'

XMLNS_SEP = '_'
PASS_NAMES = False
STRIP = True
PASS_NAMES_SEP = '.'
SEC_KEY = ['tag', 'unit', 'date', 'qtrs']
FACT_GROUPS = ['gaap', 'dei']
REF_GROUPS = ['context']


### User can change the global variables (setting) in config/app_config.py file
import sys
sys.path.append('config/')
from app_config import *
