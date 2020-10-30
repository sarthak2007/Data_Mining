## Programming Languages Required:
- python 3.6.9

## Packages Required:
* json
* datetime
* requests
* os
* math

## How to run the entire assignment in one-go:
```
chmod 700 *.sh
bash assign1.sh
```

## How to run questions individually:
First run:
```
chmod 700 *.sh
rm -f *.csv states.json neighbor-districts-modified.json
```

1. Question1(**NOTE**: Running this script is necessary before other questions if you want to run the questions individually)
```
bash neighbor-districts-modified.sh
```

2. Question2
```
bash case-generator.sh
```

3. Question3
```
bash edge-generator.sh
```

4. Question4
```
bash neighbor-generator.sh
```

5. Question5
```
bash state-generator.sh
```

6. Question6
```
bash zscore-generator.sh
```

7. Question7
```
bash method-spot-generator.sh
```

8. Question8
```
bash top-generator.sh
```

## Description of bash script for Question1:
The bash script calls 2 python files data.py and modified_neighbors.py.
data.py:
* downloads the raw data and process to make data.json which contains all relevant information.
* **NOTE**: If data.json is already present in the directory then it does not fetch the raw data again. So, if you want the data to be fetched again then delete data.json.
* then it also creates states.json (which contains states and their districts) from using fetched data

modified_neighbors.py:
* it uses neighbor-districts.json and states.json to create neighbor-districts-modified.json

So, then in Question2 data is not fetched again from the website as we have already did that in Question1. So, data.json is used in further questions which is created in Question1.
Hence, it is necessary to run script for Question1 before proceeding further.
