# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 15:16:00 2019

@author: DGuo
"""

# define a function which is used to calculate months difference
def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month
