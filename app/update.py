''' manages updates of all extracts and transformations by calling gate and all other modules '''

from app import *
import app.gate as gate
import os
import pandas as pd
import requests
import app.sec_xml as sx

def secs_from_zips ():
    archived_sec_zips = gate.read_archived_sec_zips()
    all_sec_zip_urls = gate.scrape_sec_zip_urls()
    new_sec_zip_urls = [url for url in all_sec_zip_urls if os.path.basename(url) not in archived_sec_zips]
    print("New sec zip files are ", new_sec_zip_urls)
    for sec_zip_url in sorted(new_sec_zip_urls):
        secs = gate.read_zip_sec (sec_zip_url)
        for cik, sec in secs.groupby('cik'):
            gate.update_df (sec, SEC_FOLDER+str(cik)+'.csv', key=SEC_KEY, keep='last')
        new_sec_zip_basenames = [os.path.basename(sec_zip_url)]
        gate.archive_sec_zip(new_sec_zip_basenames)
    return

def secs_from_xmls ():
    response = requests.get(NEW_SUBMISSIONS)
    response.raise_for_status()
    new_file = response.content
    submissions = gate.scrape_xml_submissions_page (response.url) # scrape it
    old_submissions = gate.scrape_xml_submissions_page (OLD_SUBMISSIONS)
    new_submissions = submissions[~submissions['file'].isin(old_submissions['file'])]
    new_submissions = new_submissions.set_index('cik')['file'] # set index
    for cik, url in new_submissions.iteritems(): # find xml file from index.json file from url, 
        try:
            response = requests.get(url)
            response.raise_for_status()
            dic = response.json()['directory']['item']
            names = pd.DataFrame(dic)['name'] # file names in submission directory
            xml_file = names[names.str.contains('[0-9]{4}(_htm)*(l)*\.xml')].iloc[0] ## regex to find xml file from names
            xml_url = os.path.dirname(url) +'/' + xml_file 
            response = requests.get(xml_url)
            response.raise_for_status()
            xml_page = response.content
            sec = sx.extract(xml_page)
            sec['value'] = pd.to_numeric(sec['value'], errors='coerce', downcast='float')
            sec = sec.dropna(subset=['value'])
            sec['qtrs'].fillna(0, inplace=True)
            gate.update_df (sec, SEC_FOLDER+str(cik)+'.csv', key=SEC_KEY, keep='last')
        except Exception as e:
            print ('ERROR! could not extract xml from ', url, e)
    with open(OLD_SUBMISSIONS, 'wb') as f: # wrtite NEW_SUBMISSIONS as the OLD_Submissions since it is used.
        f.write(new_file)

