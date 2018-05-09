



#LINK_TO_DOWNLOAD_EXCEL_FILE = http://www.fasb.org/jsp/FASB/Page/SectionPage&cid=1176168807223
systemid_stmt = {
    'stm-soi-pre': 'IS',
    'stm-sfp-cls-pre': 'BS',
    'stm-scf-indir-pre': 'CF',
    'stm-soc-pre': 'CI',
    'stm-sheci-pre':'EQ' } #wrong
stmt_cutoff = {
    'IS': 25,
    'BS': 25,
    'CF': 15,
    'CI': 10,
    'EQ': 10,
    'CP': 10
}

def create_stmt_templates ():
    '''creates general templates for financial statements 
    using most popular tags from sec pre file and ordered by fasb.org taxonomy excel file.'''
    # read taxonomy, select only desired one (from stmt_systemid), drop duplicates, add stmt column, a line (order) column for each stmt
    taxonomy = pd.read_excel(TAXONOMY_EXCEL, sheet_name=1)
    taxonomy = {stmt:taxonomy[taxonomy['systemid'].str.contains(systemid, na=False)].drop_duplicates('name').reset_index(drop=True) for systemid, stmt in systemid_stmt.items()}
    taxonomy = pd.concat(taxonomy, names=['stmt', 'line']).reset_index().rename(columns={'name': 'tag'})
    # read sec num file, make count for each tag, choose most frequent one
    sec = pd.read_csv(SEC_FILE, sep='\t')
    sec = sec['tag'].value_counts().nlargest(100).rename('adsh')
    # merge two dataframe and sort by line, and save
    sec = taxonomy.join(sec, on='tag', how='right').sort_values(['stmt', 'line'])
    sec = sec.groupby('stmt').apply(lambda x: x.nlargest(stmt_cutoff.get(x.name,0), 'adsh')) # cut off for each stmt by stmt_cutoff
    sec = sec.sort_values(['stmt', 'line']).reset_index(drop=True)
    os.rename(STMT_TEMPLATE, ARCHIVE_STMT_TEMPLATE) # move old to archive
    pre.to_csv (STMT_TEMPLATE, index=False) # save new template
    #print('DONE! input taxonomy file: ', TAXONOMY_EXCEL, ' and sec pre.txt file: ', SEC_FILE, 'was used and output file saved in ', STMT_TEMPLATE, ' and old file archived in ', ARCHIVE_STMT_TEMPLATE)
    return
