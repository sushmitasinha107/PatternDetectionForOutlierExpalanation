#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 02:21:26 2017

@author: sushmitasinha
"""

from PatternFinder import PatternFinder

values = ['open', 'high', 'low', 'close', 'volume', 'split_ratio', 'adj_open',
          'adj_high', 'adj_low', 'adj_close', 'adj_volume']
# values = ['open', 'high', 'low', 'volume']
time = ["year", "month"]
dimensions = []
categories = ["ticker"]
tableName = "stock"
p = PatternFinder(time, categories, dimensions, values, "stock")

# p.findPatterns()

fixed = ["ticker"]
variable = ["year"]
p.findRegressions(fixed, variable, "avg", "open", )
