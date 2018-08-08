#!/bin/bash
### update deploy-machine through git
gcloud compute instances start deploy
gcloud compute scp ~/PROJECTS/inVisement/config/exclude ali@deploy:~/PROJECTS/inVisement/.git/info/exclude
gcloud compute ssh ali@deploy << update-deploy
cd ~/PROJECTS/inVisement/
git fetch origin
git reset --hard origin/master
source .env/bin/activate
cat config/pythonRequirements.txt | xargs -n 1 pip install
deactivate
update-deploy
## turn off the deploy machine
gcloud compute instances stop deploy
echo deploy-machine code files are updated through git


