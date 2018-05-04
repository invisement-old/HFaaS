#!/bin/bash
### update deploy-machine through git
gcloud compute instances start deploy
gcloud compute scp ~/PROJECTS/Finmint/config/exclude ali@deploy:~/PROJECTS/Finmint/.git/info/exclude
gcloud compute ssh ali@deploy << update-deploy
cd ~/PROJECTS/Finmint/
git fetch
git reset --hard origin/master
git merge master/origin
git diff --name-only
source .env/bin/activate
cat config/python-requirements.txt | xargs -n 1 pip install
deactivate
update-deploy
## turn off the deploy machine
gcloud compute instances stop deploy
echo deploy-machine code files are updated through git


