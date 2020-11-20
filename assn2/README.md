## Programming Language Required
- python 3.6.9

## Packages Required
* collections
* sys
* csv

## Directory Structure
```
.
├── assign2_1.pdf
├── data
│   ├── output
│   │   └── *.csv
│   └── wikispeedia_paths-and-graph
├── README.txt
├── report
│   ├── report.tex
│   └── report.pdf
└── src
    ├── *.py
    └── *.sh
```

## Description:
- Avg. time taken to run the whole assignment: 2 mins 25 seconds on a 2.30GHz, 64-bit, 8GB RAM machine.
- All the output csv files are generated inside the ./data/output directory.
- All the python and bash scripts are present in the ./src directory.
- A module helper.py is created which contains many general functions that are being used in many questions. 
- Questions 8 and 9 have different csv files but their corresponding bash script is same i.e. category-paths.sh.
- Except for question9, if a csv file is x.csv then its corresponding implementation/generation files are x.py and x.sh. 
- The default line separator is '\r\n' in csv.writer. If you're getting difference in the output files even though they look same, then you can try chaning the line separator by modifying output() function in helper.py. You have to just comment the line 9 and uncomment line 10.

## How to run the entire assignment in one-go
```
cd src
chmod 700 *.sh
bash assign2.sh
```

## How to run questions individually
First run:
```
cd src
chmod 700 *.sh
```

1. Question1
```
bash article-ids.sh
```

2. Question2
```
bash category-ids.sh
```

3. Question3
```
bash article-categories.sh
```

4. Question4
```
bash edges.sh
```

5. Question5
```
bash graph-components.sh
```

6. Question6
```
bash finished-paths.sh
```

7. Question7
```
bash percentage-paths.sh
```

8. Question8 and Question 9
```
bash category-paths.sh
```

9. Question10
```
bash category-pairs.sh
```

10. Question11
```
bash category-ratios.sh
```
