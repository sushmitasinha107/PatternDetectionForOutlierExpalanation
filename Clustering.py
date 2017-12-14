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

from sklearn.cluster import KMeans

df = None


def Cluster(dimensions, values, tablename, conn):
    global df
    df = pd.read_sql_query('select * from '+tablename, con=conn)

    df.select_dtypes(include=[np.number]).isnull().sum()
    df.replace('n/a', np.nan, inplace=True)
    df.fillna(0.0, inplace=True)
    df.fillna(0, inplace=True)
    return heatMap(dimensions, values)


def correlation(dataset, thresholdpos, thresholdneg):
    col_corr = set()  # Set of all the names of columns

    corr_matrix = dataset.corr()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):

            if (corr_matrix.iloc[i, j] >= thresholdpos or
                        corr_matrix.iloc[i, j] <= thresholdneg):
                colname = corr_matrix.columns[i]  # getting the name of column
                colname2 = corr_matrix.columns[j]  # getting the name of column

                # statistic , pvalue = stats.chisquare( df[colname], df[colname2])
                # if(pvalue < 0.2):
                col_corr.add(colname)
                col_corr.add(colname2)

    return col_corr


def heatMap(dimension, value):
    thresholdpos = 0.7
    thresholdneg = -0.5
    df_cluster = df[dimension + value]
    sns.heatmap (df_cluster.corr())
    df_cluster = df[dimension + value]
    sns.heatmap (df_cluster.corr())
    cluster = KMeans(n_clusters=10)
    cluster.fit(df_cluster)
    df_cluster['clusters'] = cluster.labels_
    df_cluster.groupby('clusters').mean()
    df_heatmap = df_cluster.corr()

    col_corrheat_dim = set()  # Set of all the names of columns
    col_corrheat_val = set()  # Set of all the names of columns

    corr_matrix = df_heatmap.corr()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):

            if (corr_matrix.iloc[i, j] >= thresholdpos or corr_matrix.iloc[
                i, j] <= thresholdneg):
                colname = corr_matrix.columns[i]  # getting the name of column
                colname2 = corr_matrix.columns[j]  # getting the name of column
                if(colname in dimension):
                    col_corrheat_dim.add(colname)
                elif (colname in value):
                    col_corrheat_val.add(colname)
                if(colname2 in dimension):
                    col_corrheat_dim.add(colname2)
                elif (colname2 in value):
                    col_corrheat_val.add(colname2)
    return list(col_corrheat_dim), list(col_corrheat_val)


