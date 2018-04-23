#!/bin/bash
# execude without sudo please to avoid $HOME change
echo "Sync and upgrading finmint source files and services are started!"
date
#gcloud compute ssh ali@sec
cd ~/PROJECTS/Finmint/
git fetch
git merge master/origin
#cp config/exclude .git/info/exclude # copy customized exclude file to git
sudo cp config/nginx.conf /etc/nginx/nginx.conf # copy costomized nginx.config
sudo nginx -s reload
crontab -r # remove crontab: scheduled jobs
#crontab -l | grep -v 'config/daily-tasks2.sh' | crontab - # remove from crontabl scheduler
crontab -l | { cat; echo "0 22 * * * bash config/daily-tasks.sh &>> .temp/daily-tasks.log"; } | crontab - #add a new scheduled job use UTC time zone
crontab -l | { cat; echo "11 19 * * * bash config/daily-tasks.sh &>> .temp/daily-tasks.log"; } | crontab - #add a new scheduled job
crontab -l | { cat; echo "11 23 * * * bash config/daily-tasks.sh &>> .temp/daily-tasks.log"; } | crontab - #add a new scheduled job
date
echo "Sync Done"

