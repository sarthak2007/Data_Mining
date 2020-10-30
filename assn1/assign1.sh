# !/bin/bash

rm -f *.csv states.json neighbor-districts-modified.json

bash neighbor-districts-modified.sh
bash case-generator.sh
bash edge-generator.sh
bash neighbor-generator.sh
bash state-generator.sh
bash zscore-generator.sh
bash method-spot-generator.sh
bash top-generator.sh