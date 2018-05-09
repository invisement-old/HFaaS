
import importlib
importlib.reload(gate)
importlib.reload(sx)
importlib.reload(update)

import app.update as update
update.secs_from_zips()

import app.extract_sec as x

a = x.update()

a = pd.read_csv("~/Downloads/companylist.csv")

import app.load
app.load.load_sec()

import app.company
company = app.company.update_company_file()


### Test for sec_xml
url = 'https://www.sec.gov/Archives/edgar/data/1089598/000101489718000017/0001014897-18-000017-index.html'
url = 'https://www.sec.gov/Archives/edgar/data/1657642/000119312518117072/0001193125-18-117072-index.html'
url = 'https://www.sec.gov/Archives/edgar/data/98338/000121390018004379/0001213900-18-004379-index.html'
url = 'https://www.sec.gov/Archives/edgar/data/51143/000104746916010329/0001047469-16-010329-index.html'
url = 'https://www.sec.gov/Archives/edgar/data/789019/000156459017014900/0001564590-17-014900-index.html'
url = 'https://www.sec.gov/Archives/edgar/data/1208261/000114420418018699/0001144204-18-018699-index.html'

import app.sec_xml as sx
importlib.reload(sx)
a = sx.extract(url)

import app.extract_sec as xt
importlib.reload(xt)
xt.update_sec_from_zips()
xt.update_sec_from_xml()

########
g = sx.extract(url)
import app.stmt_templates as tmpl
tmpl.create_stmt_templates()

import app.update as update


