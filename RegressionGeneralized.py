#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 16:05:11 2017

@author: deeptichavan
"""

import sys
import psycopg2
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from matplotlib.backends.backend_pdf import PdfPages



ATTRIBUTES_FILE = 'attributes.txt'
AGGREGATE = 'avg'
TABLENAME = 'author'
conn = None
try:
    conn = psycopg2.connect(dbname='deeptichavan', user='postgres', host='localhost', password='postgres')
except psycopg2.DatabaseError as ex:
    print (ex)
    sys.exit(1)

curs = conn.cursor()
pdf = PdfPages('Authors.pdf')


def load_attributes(filePath):
    
    '''
        load the dimension, fixed and value columns
    '''
    with open(filePath) as f:
        lines = f.readlines()

    '''
    variableAttributes = lines[0].strip(' \r\n').split(',')
    fixedAttributes = lines[1].strip(' \r\n').split(',')
    valueAttributes = lines[2].strip(' \r\n').split(',')
    '''
    #return fixedAttributes, variableAttributes, valueAttributes
    return lines[0], lines[1], lines[2]


def formQuery(fixed, variable, value, tableName):
    
    query = "SELECT " + fixed + ", " + variable + ", avg(" + value + ") FROM " + tableName + " where ticker in ('AAPL', 'MSFT', 'A') GROUP BY " + fixed + ", " + variable
    
    print('Query::', query)
    #query = "SELECT name, year, COUNT(DISTINCT pubid) FROM dblp_combined where name in ('Jiawei Han', 'Samuel Madden', 'Joseph M. Hellerstein', 'Jeffrey Xu Yu')   group by name, year"
    return query


def performLinearRegression(x ,y, r):
    
    lr = LinearRegression(normalize=True)
    lr.fit(x,y)
    
    slope = lr.coef_
    
    ytest = lr.predict(x)
    
    x = x.astype(float)
    y = y.astype(float)
    scoreLR = lr.score(x, y)
        
    mse = mean_squared_error(y, ytest)
    rmse = np.sqrt(mse)
        
    return float(slope), rmse, ytest, scoreLR

def plotLinearRegression(x, y, yPltLR, scoreLR, fixed):
    
    lw = 2
    fig = plt.figure()
    fig.set_size_inches(10.5, 6.5)
    #plt.xlabel('months')
    #plt.ylabel(label)
    plt.suptitle("State:: " + fixed +  "  Score :: " + str(scoreLR)) 
      
    plt.scatter(x,y)
    plt.plot(x, yPltLR, color='navy', linewidth=lw, label='Linear Regressor')
    
    plt.legend(loc='lower right')
    plt.show()
    pdf.savefig(fig)
    
    return

def formDictionary(curs, dictFixed):
    
    for row in curs:
        fixed = row[0]
        variable = row[1]
        agg = row[2]
        
        if fixed not in dictFixed:
            dictFixed[fixed] = {}
       
        dictFixed[fixed][variable] = float(agg)


def fitRegressionModel(dictFixed):
    
    for fixed, plotData in dictFixed.items():
    
        x = []
        y = []
        for key in plotData:
            x.append(key)
            y.append(plotData[key])
                        
        
        x = np.transpose(np.reshape(x,[1,len(x)]))
        y = np.transpose(np.reshape(y,[1,len(y)]))
        r = x.size
        
        slopeLR, rmseLR, yPltLR, scoreLR = performLinearRegression(x, y, r)
        plotLinearRegression(x, y, yPltLR, scoreLR, fixed)
     


'''
fixedAttributes, variableAttributes, valueAttributes = load_attributes(ATTRIBUTES_FILE)

query = formQuery(fixedAttributes, variableAttributes, valueAttributes)
print (query)
curs.execute(query)

print(curs.rowcount)

dictFixed = {}
formDictionary(curs)

fitRegressionModel(dictFixed)


pdf.close()
'''
