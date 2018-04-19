#!/bin/bash
echo "Monthly Script Started!"
export PYTHONPATH=~/PROJECTS/Finmint/app
source ~/PROJECTS/Finmint/.env/bin/activate
python -c "import company; company.test();"

