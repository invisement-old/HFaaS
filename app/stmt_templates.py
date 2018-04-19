
TAXONOMY_EXCEL = 'data/Taxonomy_2017Amended.xlsx'
SEC_PRE_FILE = 'data/pre.txt'
OUTPUT_STMT_TEMPLATE = 'data/stmt_template.csv'
#LINK_TO_DOWNLOAD_EXCEL_FILE = http://www.fasb.org/jsp/FASB/Page/SectionPage&cid=1176168807223
stmt_systemid = {
    'IS': 'stm-soi-pre',
    'BS': 'stm-sfp-cls-pre',
    'CF': 'stm-scf-indir-pre',
    'CI': 'stm-soc-pre',
    'EQ': 'stm-sheci-pre'} #wrong
stmt_size = {
    'IS': 20,
    'BS': 25,
    'CF': 20,
    'CI': 15,
    'EQ': 20,
    'CP': 15
}

def create_stmt_templates ():
    '''creates general templates for financial statements 
    using most popular tags from sec pre file and ordered by fasb.org taxonomy excel file.'''
    # read taxonomy, select only desired one (from stmt_systemid), drop duplicates, add stmt column, a line (order) column for each stmt
    taxonomy = pd.read_excel(TAXONOMY_EXCEL, sheet_name=1)
    taxonomy = {stmt:taxonomy[taxonomy['systemid'].str.contains(systemid, na=False)].drop_duplicates('name').reset_index(drop=True) for stmt, systemid in stmt_systemid.items()}
    taxonomy = pd.concat(taxonomy, names=['stmt', 'line']).reset_index().rename(columns={'name': 'tag'})
    # read sec pre file, clean it ftom abstract tags, make count for each tag, choose most frequenct one based on stmt_size cut-off
    pre = pd.read_csv(SEC_PRE_FILE, sep='\t')
    pre = pre[~ pre['plabel'].str.contains("\[", na=False)]
    pre = pre[~ pre['tag'].str.contains('Abstract', case=False, na=False, regex=False)]
    pre = pre.filter(['stmt', 'adsh', 'tag']).drop_duplicates()
    pre = pre.groupby(['stmt', 'tag']).count().reset_index()
    pre = pre.groupby('stmt').apply(lambda x: x.nlargest(stmt_size.get(x.name,0), 'adsh')).reset_index(drop=True)
    # merge two dataframe and sort by line, and save
    pre = pre.merge(taxonomy, on=['stmt', 'tag'], how='left').sort_values(['stmt', 'line'])
    pre.to_csv (OUTPUT_STMT_TEMPLATE, index=False)
    print('input taxonomy file:', TAXONOMY_EXCEL, 'and sec pre.txt file:', SEC_PRE_FILE, 'output saved in', OUTPUT_STMT_TEMPLATE)
    return
