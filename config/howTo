# How-To

## Update ops machine
- ~/PROJECTS/Finmint/config/update-ops.sh

## Update deploy machine
- ~/PROJECTS/Finmint/config/update-deploy.sh

## Create or Update finset from sec files
    cik_file=$"data/123.csv"
    python -c 'import app.update as up; up.update_finset("$cik_file")'


## update blog posts
    cd ~/PROJECTS/inVisement
    hugo --config hugo-themes/inVisement/config.toml
    gsutil -m rsync -d -r .invisement.com gs://invisement.com
    
## copy exclude to git
    cp config/exclude.txt .git/info/exclude.txt



