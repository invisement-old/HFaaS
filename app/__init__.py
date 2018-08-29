
import pandas as pd
import os

### Thses are default global variables (setting) for python apps in this package
## For extract_sec module
SEC_DATA_SETS_INDEX = "https://www.sec.gov/dera/data/financial-statement-data-sets.html"
TEMP = ".temp/"
SEC_FOLDER = 'data/sec/'
ARCHIVE_DATA = 'archive-data/'
SEC_KEY = ['tag', 'date', 'qtrs']
SEC_COLS = ['tag','date', 'qtrs', 'unit', 'value']
SEC_ENCODING = 'latin1'
NEW_SUBMISSIONS = 'https://www.sec.gov/Archives/edgar/full-index/xbrl.idx'
OLD_SUBMISSIONS = 'data/basic/xbrl.idx'
DATA_SETTING = 'data/basic/data-setting.json'
SEC_ZIP_ARCHIVES = 'sec_zip_archives'
DATE_FORMAT = "%Y%m%d"
DATATYPE = str

## For sec_xml module
XMLNS_SEP = '_'
PASS_NAMES = False
STRIP = True
PASS_NAMES_SEP = '.'
FACT_GROUPS = ['gaap', 'dei']
REF_GROUPS = ['context']

## For stmt_template module
TAXONOMY_EXCEL = 'data/Taxonomy_2017Amended.xlsx'
SEC_FILE = '.temp/num.txt'
STMT_TEMPLATE = 'data/basic/stmt_template.csv'
ARCHIVE_STMT_TEMPLATE = 'data/basic/stmt_template_archive.csv'
STMT_FOLDER = 'data/stmt/'

## For update module

#FINSET_FOLDER = "data/finset/"
QUARTERLY_FOLDER = "data/q/"
YEARLY_FOLDER = "data/y/"
CIK2TICKER = "data/basic/company.csv"
FILL_MISSING_SINCE = "19590101"

