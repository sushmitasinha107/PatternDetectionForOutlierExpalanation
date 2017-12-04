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
import psycopg2
# import seaborn as sns
# import scipy.stats as stats
#
# from scipy.stats import chi2
# from scipy.stats import chisquare
#
# import matplotlib.pyplot as plt
# ##import re

import sklearn as sk
import sklearn.tree as tree
from sklearn.cluster import KMeans

# from IPython.display import Image
# ##import pydotplus

# from sklearn.tree import DecisionTreeRegressor



def findCatCorrelation3(variable, value, fixedcategory, categoryvalues):
    CategotyResult = False
    Cat_trueCount = 0;
    Cat_falseCount = 0;
    #  fixed/value/categorical
    df_cluster = df[[variable, value, fixedcategory]]

    for categoryvalue in categoryvalues:
        df_clustermean = df_cluster.where(
            df[fixedcategory] == categoryvalue).groupby([variable, fixedcategory]).mean()
        # df_clustermean.plot.line(style=['o','rx'])
        df_clusterstd = df_cluster.where(
            df[fixedcategory] == categoryvalue).groupby([variable, fixedcategory]).std()
        # df_clusterstd.plot.line(style=['o','rx'])
        trueCount = 0;
        falseCount = 0;
        for row1 in df_clustermean.iterrows():
            for row in df_clusterstd.iterrows():
                if (row1[0][0] == row[0][0]):
                    mean = row1[1]
                    std = row[1]
                    if (std[value] == 0 or  std[value]/mean[value] < .15):
                        trueCount = trueCount + 1
                    else:
                        falseCount = falseCount + 1

        if (trueCount > falseCount):
            Cat_trueCount = Cat_trueCount + 1
        else:
            Cat_falseCount = Cat_falseCount + 1
    if (Cat_trueCount > Cat_falseCount):
        CategotyResult = True
    return CategotyResult


def findCatCorrelation2(value,category):
    
    falseCount = 0
    trueCount = 0   
    CategotyResult = False
    df_cluster = df[[ value , category]]
    
    df_clustermean = df_cluster.groupby([category]).mean()
    #df_clustermean.plot.line(style=['o','rx'])
    df_clusterstd = df_cluster.groupby([category]).std()
    #df_clusterstd.plot.line(style=['o','rx'])
    #for keymean,valuemean in df_clustermean.iteritems():
    
    for row1 in df_clustermean.iterrows():
        for row in df_clusterstd.iterrows():
            if(row1[0] == row[0]):
                mean = row1[1]
                std = row[1]
                if( std[value] == 0 or mean[value]/std[value] < 15):
                    trueCount = trueCount +1
                else:
                    falseCount= falseCount+1    
            
    if((trueCount/falseCount) >0.75):
        CategotyResult = True
        
    return CategotyResult


def correlation(dataset, thresholdpos, thresholdneg):
    col_corr = set()  # Set of all the names of columns

    corr_matrix = dataset.corr()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):

            if (corr_matrix.iloc[i, j] >= thresholdpos or corr_matrix.iloc[
                i, j] <= thresholdneg):
                colname = corr_matrix.columns[i]  # getting the name of column
                colname2 = corr_matrix.columns[j]  # getting the name of column

                # statistic , pvalue = stats.chisquare( df[colname], df[colname2])
                # if(pvalue < 0.2):
                col_corr.add(colname)
                col_corr.add(colname2)

    return col_corr

def heatMap(dimention, value):
    thresholdpos = 0.5
    thresholdneg = -0.5
    df_cluster = df[dimention + value ]
    # sns.heatmap (df_cluster.corr())
    cluster = KMeans(n_clusters=5)
    cluster.fit(df_cluster)
    df_cluster['clusters'] = cluster.labels_
    df_cluster.groupby('clusters').mean()
    df_heatmap = df_cluster.corr();

    col_corrHeat_dim = set()  # Set of all the names of columns
    col_corrHeat_val = set()  # Set of all the names of columns

    corr_matrix = df_heatmap.corr()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):

            if (corr_matrix.iloc[i, j] >= thresholdpos or corr_matrix.iloc[
                i, j] <= thresholdneg):
                colname = corr_matrix.columns[i]  # getting the name of column
                colname2 = corr_matrix.columns[j]  # getting the name of column
                if(colname in dimention):
                    col_corrHeat_dim.add(colname)
                elif (colname in value):
                    col_corrHeat_val.add(colname)
                if(colname2 in dimention):
                    col_corrHeat_dim.add(colname2)
                elif (colname2 in value):
                    col_corrHeat_val.add(colname2)

    return list(col_corrHeat_dim), list(col_corrHeat_val)


conn = psycopg2.connect(dbname='postgres', user='postgres',
                                    host='localhost', password='postgres')
#df = pd.read_sql_query('select * from stock', con=conn)
col = ['ticker', 'date', 'month', 'day', 'year','open', 'high', 'low', 'close', 'volume', 'ex-dividend', 'split_ratio', 'adj_open','adj_high', 'adj_low', 'adj_close', 'adj_volume']
df  = pd.read_csv('/Users/deeptichavan/Downloads/dataAll.csv', names=col) 

df.select_dtypes(include=[np.number]).isnull().sum()
df.replace('n/a', np.nan, inplace=True)
df.fillna(0.0, inplace=True)
df.fillna(0, inplace=True)



'''
list_corr = value_col + dimention_col
df_cluster = df[list_corr]
# sns.heatmap (df_cluster.corr())
cluster = KMeans(n_clusters=5)
cluster.fit(df_cluster)
df_cluster['clusters'] = cluster.labels_
df_cluster.groupby('clusters').mean()
df_cluster_corr = df_cluster.corr()
df_heatmap = df_cluster.corr();
print(df_cluster_hm)
'''
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

















