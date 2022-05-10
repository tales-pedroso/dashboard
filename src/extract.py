# -*- coding: utf-8 -*-
import pandas as pd

def extract(url):
    df = pd.read_csv(url, index_col = False, dtype = 'object')
    return df