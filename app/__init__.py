

### Thses are default global variables (setting) for python apps in this package
## For extract_sec module
SEC_DATA_SETS_INDEX = "https://www.sec.gov/dera/data/financial-statement-data-sets.html"
TEMP = ".temp/"
SEC_FOLDER = 'data/sec/'
ARCHIVE_DATA = 'archive-data/'
SEC_KEY = ['tag', 'date', 'qtrs', 'unit']
SEC_ENCODING = 'latin1'
NEW_SUBMISSIONS = 'https://www.sec.gov/Archives/edgar/full-index/form.idx'
OLD_SUBMISSIONS = 'data/basic/form_idx.csv'
DATA_SETTING = 'data/basic/data-setting.json'
SEC_ZIP_ARCHIVES = 'sec_zip_archives'

## For sec_xml module
XMLNS_SEP = '_'
PASS_NAMES = False
STRIP = True
PASS_NAMES_SEP = '.'
SEC_KEY = ['tag', 'unit', 'date', 'qtrs']
FACT_GROUPS = ['gaap', 'dei']
REF_GROUPS = ['context']

## For stmt_template module
TAXONOMY_EXCEL = 'data/Taxonomy_2017Amended.xlsx'
SEC_FILE = '.temp/num.txt'
STMT_TEMPLATE = 'data/basic/stmt_template.csv'
ARCHIVE_STMT_TEMPLATE = 'data/basic/stmt_template_archive.csv'
STMT_FOLDER = 'data/stmt/'

## For update module

FINSET_FOLDER = "data/finset/"
CIK2TICKER = "data/basic/company.csv"




### User can change the global variables (setting) in config/app_config.py file
import sys
sys.path.append('config/')
from app_config import *
