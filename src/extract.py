# -*- coding: utf-8 -*-
import pandas as pd

def extract_business_data(url):
    df = pd.read_csv(url, index_col = False, dtype = 'object')
    return df

def extract_geojson(url):
    pass