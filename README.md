# Data mining project1
## Association analysis

### Dataset
After generate file from IBM Quest Data Generator , preprocessing the transcation data file to the preprocessed file , each line will be a transcation itemset.

Files in the report are under datas/ folder

There are two types of command:
#### preprocessing
`python main.py preprocessing <IBM data file path> <target file path>`
before test , please preprocessing file first.
#### test
`python main.py test brute|fpg  <transaction file path> <rule output file path> <min support> <min confidence>`
Generated rules will write to <rule output file path>