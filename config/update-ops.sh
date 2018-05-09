#!/bin/bash
# execute without sudo to avoid $HOME change
echo "Sync and upgrade control-machine. It includes scheduler, nginx, etc."
date
### copy deploy-job and nginx to control
#gcloud compute scp ~/PROJECTS/Finmint/config/nginx.conf ali@sec:~/PROJECTS/Finmint/config
gcloud compute scp ~/PROJECTS/Finmint/config/daily-deploy-job.sh ali@ops:~/PROJECTS/Finmint/config

gcloud compute ssh ali@ops <<update-ops
#sudo cp config/nginx.conf /etc/nginx/nginx.conf # copy costomized nginx.config
#sudo nginx -s reload

crontab -r # remove crontab: scheduled jobs
#crontab -l | grep -v 'config/daily-tasks.sh' | crontab - # remove from crontabl scheduler
crontab -l | { cat; echo "35 3,23 * * * bash ~/PROJECTS/Finmint/config/daily-deploy-job.sh"; } | crontab - #add a new scheduled job
crontab -l | { cat; echo "35 4 * * 2 mv ~/PROJECTS/Finmint/.log/*.log ~/PROJECTS/Finmint/.log/archive"; } | crontab - #add a new scheduled job
crontab -l
update-ops
date
echo Sync and upgrading control-machine is done.

