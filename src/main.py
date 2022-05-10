# -*- coding: utf-8 -*-
from config import URL
from config import get_db_params

from extract import extract
from transform import transform
from load import load
from get_dashboard_data import get_dashboard_data

from pipes_and_filters import UgPipe, UtilityPipe, DatePipe, DecimalPipe

# maybe ORM makes this better

# design to incrementally load more data into the database and building 
# an updated dashboard from it

if __name__ == '__main__':
    # EXTRACT
    # !!! correct data in csv_file. There are multiple dh_id for the same ug_code
    
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
    db_params = get_db_params()
    
    
    #load(trans_df, DB, USER, PASS, HOST, PORT)
    load(trans_df, db_params)

    #==========================================================================
    # GET THE AGGREGATED DATA FOR THE DASHBOARD
    dashboard_df = get_dashboard_data(db_params)
    
    #==========================================================================
    # BUILD DASHBOARD
    
    
    