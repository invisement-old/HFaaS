#!/bin/bash
echo "Daily Script Started!"
date
cd ~/PROJECTS/Finmint
source .env/bin/activate
# python -c "import company; company.test();"
python -c "import app.extract_sec as xt; xt.update_sec_from_xml(); xt.update_sec_from_zips()"
deactivate
echo "Daily Script Finished, hopefully, successfully!"
date

