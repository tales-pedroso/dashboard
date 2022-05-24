# -*- coding: utf-8 -*-
import pandas as pd
import requests

def extract_business_data(url):
    df = pd.read_csv(url, index_col = False, dtype = 'object')
    return df

def extract_geojson(url):
    res = requests.get(url)
    geojson = res.json()
    return geojson