#!/bin/bash
echo start paid machine from ops, run daily job to update sec files, copy them to gs://sec.finmint.us
cd ~/PROJECTS/Finmint
gcloud compute instances start paid
gcloud compute ssh ali@paid --quiet &>> .log/daily-paid-job.log <<daily-paid-job
echo "Daily paid job for sec update started!"
date
## set up env
cd ~/PROJECTS/Finmint
source .env/bin/activate
# python -c "import company; company.test();"
touch .temp/stopwatch # record time of start by creating a temp file
## extract all new files from sec
python -c "import app.extract_sec as xt; xt.update_sec_from_zips(); xt.update_sec_from_xml()" # update data sets
## convert newly updated sec files to finset
find data/sec/* -newer .temp/stopwatch -exec python -c "import sys; import app.update; app.update.update_finset(sys.argv[1])" {} \;
deactivate
## push to gstorage all files in sec and finset that newly updated
find data/sec/* -newer .temp/stopwatch | gsutil -m cp -r -c -Z -I gs://sec.finmint.us/
find data/finset/* -newer .temp/stopwatch | gsutil -m cp -r -c -Z -I gs://sec.finmint.us/
date
echo "Daily Script Finished, hopefully, successfully!"
daily-paid-job
gcloud compute instances stop paid
echo daily jobs are done and paid machine is stopped

