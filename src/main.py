# -*- coding: utf-8 -*-
from extract import extract
from config import URL

from pipes_and_filters import UgPipe, UtilityPipe, DatePipe, DecimalPipe
from transform import transform

from load import load
from config import DB, USER, PASS, HOST, PORT

from get_fact_data import get_fact_data

# maybe ORM makes this better

# design to incrementally load more data into the database and building 
# an updated dashboard from it

if __name__ == '__main__':
    # EXTRACT
    # correct data in csv_file. There are multiple dh_id for the same ug_code
    
    # it does not save the csv file locally
    
    # wrap into try-except
    df = extract(URL) 
    
    #==========================================================================
    # TRANSFORM
    old_cols = ('ug_code', 'utility_code', 'date_', 'value_')
    new_cols = ('ug_id',   'utility_id',  'date_', 'value_') 
    pipes = (UgPipe, UtilityPipe, DatePipe, DecimalPipe)
    
    trans_df = transform(df, old_cols, new_cols, pipes) 
    
    #==========================================================================
    # LOAD
    
    load(trans_df, DB, USER, PASS, HOST, PORT)

    #==========================================================================
    # GET THE WHOLE factpayment DATA
    fact_df = get_fact_data(DB, USER, PASS, HOST, PORT)
    
    #==========================================================================
    # BUILD DASHBOARD
    
    
    