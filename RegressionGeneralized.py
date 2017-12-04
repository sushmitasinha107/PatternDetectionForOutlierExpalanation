#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 16:05:11 2017

@author: deeptichavan
"""

import matplotlib.pyplot as plt
import numpy as np
from Pattern import Pattern
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from matplotlib.backends.backend_pdf import PdfPages
from PatternStore import addPattern
import PatternFinder as pf

def formQuery(fixed, variable, aggFunc, value, tableName):
    
    query = "SELECT " + fixed + ", " + variable + ", avg(" + value + ") FROM " + tableName  +\
            " GROUP BY " + fixed + ", " + variable + " ORDER BY " + variable
    
    #print('Query::', query)

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
    #plt.show()
    
    pf.pdf.savefig(fig)
    
    return

def formDictionary(curs, dictFixed):
    
    for row in curs:
        fixed = row[0]
        variable = row[1]
        agg = row[2]
        
        if fixed not in dictFixed:
            dictFixed[fixed] = {}
       
        dictFixed[fixed][variable] = float(agg)


def fitRegressionModel(dictFixed, fixed, variable, aggFunc, value):
    
    validPatterns = 0
    for fixedVar, plotData in dictFixed.items():
    
        x = []
        y = []
        for key in plotData:
            x.append(key)
            y.append(plotData[key])
                        
        
        x = np.transpose(np.reshape(x,[1,len(x)]))
        y = np.transpose(np.reshape(y,[1,len(y)]))
        r = x.size
        
        slopeLR, rmseLR, yPltLR, scoreLR = performLinearRegression(x, y, r)
        
        if(slopeLR > 0 and scoreLR > 0.7):
            validPatterns = validPatterns + 1
            addPattern(fixed, fixedVar, variable, aggFunc, value, 'increasing', scoreLR)
            #plotLinearRegression(x, y, yPltLR, scoreLR, fixed)
            
        elif(slopeLR < 0 and scoreLR > 0.7):
            validPatterns = validPatterns + 1
            addPattern(fixed, fixedVar, variable, aggFunc, value, 'decreasing', scoreLR)
            #plotLinearRegression(x, y, yPltLR, scoreLR, fixed)
                  
        
    
    addPattern(fixed, "none", variable, aggFunc, value, "none", (validPatterns * 100 / len(dictFixed)))
        
