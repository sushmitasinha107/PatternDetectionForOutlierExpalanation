#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 16:31:31 2017

@author: sushmitasinha
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np
import seaborn as sns
import scipy.stats as stats

from scipy.stats import chi2
from scipy.stats import chisquare

import matplotlib.pyplot as plt
##import re

import sklearn as sk
import sklearn.tree as tree
from sklearn.cluster import KMeans

from IPython.display import Image  
##import pydotplus

from sklearn.tree import DecisionTreeRegressor



def findCatCorrelation3(fixed,value,category, categoryvalues):
    
    CategotyResult = False
    Cat_trueCount = 0;
    Cat_falseCount = 0;
    #  fixed/value/categorical
    df_cluster = df[[fixed, value , category]]
    
    for categoryvalue in categoryvalues:
        df_clustermean = df_cluster.where(df[category] == categoryvalue).groupby([fixed,category]).mean()
        #df_clustermean.plot.line(style=['o','rx'])
        df_clusterstd = df_cluster.where(df[category] == categoryvalue).groupby([fixed,category]).std()
        #df_clusterstd.plot.line(style=['o','rx'])
        trueCount = 0;
        falseCount = 0;
        for row1 in df_clustermean.iterrows():
            for row in df_clusterstd.iterrows():
                if(row1[0][0] == row[0][0]):
                    mean = row1[1]
                    std = row[1]
                    if( std[value] == 0 or mean[value]/std[value] < 15):
                        trueCount = trueCount +1
                    else:
                        falseCount= falseCount+1
                
            
        if(trueCount>falseCount):
            Cat_trueCount = Cat_trueCount+1
        else:
            Cat_falseCount = Cat_falseCount+1
    if(Cat_trueCount>Cat_falseCount):
        CategotyResult = True
    return CategotyResult


def findCatCorrelation2(value,category, categoryvalues):
    
    CategotyResult = False
    #  fixed/value/categorical
    df_cluster = df[[ value , category]]
    
    for categoryvalue in categoryvalues:
        df_clustermean = df_cluster.where(df[category] == categoryvalue).groupby([category]).mean()
        #df_clustermean.plot.line(style=['o','rx'])
        df_clusterstd = df_cluster.where(df[category] == categoryvalue).groupby([category]).std()
        #df_clusterstd.plot.line(style=['o','rx'])
        trueCount = 0;
        falseCount = 0;
        for row1 in df_clustermean.iterrows():
            for row in df_clusterstd.iterrows():
                if(row1[0][0] == row[0][0]):
                    mean = row1[1]
                    std = row[1]
                    if( std[value] == 0 or mean[value]/std[value] < 15):
                        trueCount = trueCount +1
                    else:
                        falseCount= falseCount+1            
        if(trueCount>falseCount):
            CategotyResult = True

    return CategotyResult
        

    

def correlation(dataset, thresholdpos, thresholdneg ):
    col_corr = set() # Set of all the names of columns

    corr_matrix = dataset.corr()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            
            if (corr_matrix.iloc[i, j] >= thresholdpos or corr_matrix.iloc[i, j] <= thresholdneg):
                colname = corr_matrix.columns[i] # getting the name of column
                colname2 = corr_matrix.columns[j] # getting the name of column
               
                #statistic , pvalue = stats.chisquare( df[colname], df[colname2])
                #if(pvalue < 0.2):
                col_corr.add(colname)
                col_corr.add(colname2)

    return col_corr
    
    
def correlationHeat(dataset, thresholdpos, thresholdneg ):
    col_corrHeat = set() # Set of all the names of columns

    corr_matrix = dataset.corr()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            
            if (corr_matrix.iloc[i, j] >= thresholdpos or corr_matrix.iloc[i, j] <= thresholdneg):
                colname = corr_matrix.columns[i] # getting the name of column
                colname2 = corr_matrix.columns[j] # getting the name of column
              
                col_corrHeat.add(colname)
                col_corrHeat.add(colname2)

    return col_corrHeat



col = ['ticker', 'date', 'month', 'day', 'year','open', 'high', 'low', 'close', 'volume', 'ex-dividend', 'split_ratio', 'adj_open','adj_high', 'adj_low', 'adj_close', 'adj_volume']
df  = pd.read_csv('/Users/sushmitasinha/Downloads/data5.csv', names=col) 

#df = df[['open', 'high', 'low', 'close', 'volume', 'ex-dividend', 'split_ratio', 'adj_open','adj_high', 'adj_low', 'adj_close', 'adj_volume']]

df.select_dtypes(include=[np.number]).isnull().sum()

df.replace ('n/a', np.nan, inplace = True)
df.fillna(0.0,inplace=True)
df.fillna(0,inplace=True)

df[df.isnull() == True].count()


value_col = ['open', 'high', 'low', 'close', 'volume', 'adj_open','adj_high', 'adj_low', 'adj_close', 'adj_volume']
cat_col = ['ticker', 'date']
dimention_col = ['month','year']

list_corr = value_col + dimention_col
df_cluster = df[list_corr]
#sns.heatmap (df_cluster.corr())
cluster=KMeans(n_clusters=5)
cluster.fit(df_cluster)
df_cluster['clusters']=cluster.labels_
df_cluster.groupby('clusters').mean()
df_cluster_corr = df_cluster.corr()
df_heatmap = df_cluster.corr();
df_cluster_hm = correlationHeat(df_heatmap, 0.5 , -0.5 )
print(df_cluster_hm)
'''
#  fixed/value/categoricals
fixed = 'grade'
value = 'int_rate'
category =  'addr_state'
categoryvalues = list(set(df.addr_state))

        
#CategotyResult = findCatCorrelation3(fixed,value,category, categoryvalues)

fixed = 'grade'
value = 'int_rate'
category =  'addr_state'
categoryvalues = list(set(df.addr_state))

        
CategotyResult = findCatCorrelation2(value,category, categoryvalues)
    
            

  '''                  
    


















