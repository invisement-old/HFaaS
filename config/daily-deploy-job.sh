#!/bin/bash
## Push this bash code to ops machine everytime it is changed or updated
echo start deploy machine from ops, run daily job to update sec files, copy them to gs://sec.invisement.com
cd ~/PROJECTS/inVisement
gcloud compute instances start deploy
gcloud compute ssh ali@deploy --quiet \
    &>> .log/daily-deploy-job.log \
    << daily-deploy-job
echo "Daily deploy job for sec update started!"
date
## set up env
cd ~/PROJECTS/inVisement
source .env/bin/activate
touch .temp/stop.watch # record start time by creating a temp file
# python -c "import company; company.test();"
## extract all new files from sec
python -c "import app.update; app.update.secs_from_zips();" # update sec data from zips
python -c "import app.update; app.update.secs_from_xmls()" # update sec data from xml
## convert newly updated sec files to periodical (y, q) dataset
# find data/q/* -newer .temp/stop.watch -exec python -c "import sys; import app.transform as tr; tr.to_periodic(sys.argv[1])" {} \;
## transform periodic files to stmts
# find data/y/* -newer .temp/stop.watch -exec python -c "import sys; import app.transform as tr; tr.to_stmt(sys.argv[1])" {} \;
deactivate
## push to gstorage all files in sec and finset that newly updated
find data/sec/* -newer .temp/stop.watch | gsutil -m cp -r -c -Z -I gs://data.invisement.com/sec
find data/q/* -newer .temp/stop.watch | gsutil -m cp -r -c -Z -I gs://data.invisement.com/q
find data/y/* -newer .temp/stop.watch | gsutil -m cp -r -c -Z -I gs://data.invisement.com/y
find data/q-stmt/* -newer .temp/stop.watch | gsutil -m cp -r -c -Z -I gs://data.invisement.com/q-stmt
find data/y-stmt/* -newer .temp/stop.watch | gsutil -m cp -r -c -Z -I gs://data.invisement.com/y-stmt
date
echo "Daily Script Finished."
daily-deploy-job
gcloud compute instances stop deploy
echo "Daily jobs are done and deploy machine is stopped. Check log file ops:~/PROEJCTS/inVisement/.log/daily-deploy-job.log"

