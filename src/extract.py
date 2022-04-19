# -*- coding: utf-8 -*-

import pandas as pd

def extract(url):
    df = pd.read_csv(url, dtype = 'object')
    return df