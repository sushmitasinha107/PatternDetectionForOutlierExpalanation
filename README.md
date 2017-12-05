# PatternDetectionForOutlierExpalanation

##Prerequistes
* python 3.5
* sqlalchemy
* pandas
* sklearn
* numpy
* matplotlib
* seaborn
* psycopg2

##Usage

###PatternFinder
PatternFinder is the main module which is used to detect patterns

The following methods do the task of verifying the constraints:

*findRegressions()
*findConstants()

findPatterns() tries to enumerate all possible combinations of fixed and variable attributes
(still need to refine it to support multiple variable and fixed attributes)

Example of how the PatternFinder module is used is given in test.py

