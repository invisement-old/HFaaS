#!/bin/bash
echo "Daily Script Started!" >> log/output-log.txt
date >> log/output-log.txt
cd ~/PROJECTS/Finmint
source _env/bin/activate
# python -c "import company; company.test();"
python -c "import app.extract_sec as xt; xt.update_sec_from_xml(); xt.update_sec_from_zips()" >> log/output-log.txt
deactivate
echo "Daily Script Finished, hopefully, successfully!" >> log/output-log.txt
date >> log/output-log.txt

