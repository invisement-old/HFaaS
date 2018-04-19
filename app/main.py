
import importlib
importlib.reload(xl)

import app.extract_sec as x

a = x.update()

a = pd.read_csv("~/Downloads/companylist.csv")

import app.load
app.load.load_sec()

import app.company
company = app.company.update_company_file()


### Test for sec_xml
url = 'https://www.sec.gov/Archives/edgar/data/1657642/000119312518117072/0001193125-18-117072-index.html'
url = 'https://www.sec.gov/Archives/edgar/data/1089598/000101489718000017/0001014897-18-000017-index.html'
url = 'https://www.sec.gov/Archives/edgar/data/98338/000121390018004379/0001213900-18-004379-index.html'
url = 'https://www.sec.gov/Archives/edgar/data/51143/000104746916010329/0001047469-16-010329-index.html'
url = 'https://www.sec.gov/Archives/edgar/data/789019/000156459017014900/0001564590-17-014900-index.html'

import app.sec_xml as sx
importlib.reload(sx)

g = sx.extract(url)




