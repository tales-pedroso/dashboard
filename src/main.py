# -*- coding: utf-8 -*-
from extract import extract
from config import URL
from pipes_and_filters import UgPipe, UtilityPipe, DecimalPipe, DatePipe
from transform import transform

if __name__ == '__main__':
    # EXTRACT
    
    # wrap into try-except
    df = extract(URL)
    
    #==========================================================================
    # TRANSFORM
    
    cols  = ('ug_code', 'utility_code', 'date', 'value')
    pipes = (UgPipe, UtilityPipe, DatePipe, DecimalPipe)
    
    trans_df = transform(df, cols, pipes)
    # 
    
    #==========================================================================
    # LOAD
    
    