
import importlib
importlib.reload(xt)

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
mport app.stmt_templates as tmpl
tmpl.create_stmt_templates()


#########
import wget
import time
import os
import requests

url = "http://sec.finmint.us/1000180.csv.gz"
url = "https://www.google.com"
url = 'http://www.futurecrew.com/skaven/song_files/mp3/razorback.mp3'

import urllib.request


t0 = time.time()
os.system("wget "+url)
t1 = time.time()
res = requests.get(url)
with open("test.csv", 'wb') as out_file:
    out_file.write(res.content)

t0 = time.time()
os.system("gsutil cp -Z test.csv gs://sec.finmint.us")
t1 = time.time()
open("test.csv", "wb").write(requests.get(url).content)
t2 = time.time()
print(t1-t0, t2-t1)
import pandas as pd

############
import asyncio
import time
import requests
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

urls = ['http://www.google.com', "http://www.nytimes.com",  "http://www.microsoft.com", "http://www.cnn.com", 'http://www.yandex.ru', 'http://www.python.org']

async def call_url(url):
    print('Starting {}'.format(url))
    #response = requests.get(url)
    response = await loop.run_in_executor(None, requests.get, url)
    #data = yield from response.text
    #print('{}: {} bytes: {}'.format(url, len(data), data))
    return response.text

t0 = time.time()
futures = [call_url(url) for url in urls]
res, _ = loop.run_until_complete(asyncio.wait(futures))
a = [x.result() for x in res]
t1 = time.time()
t1-t0

###
