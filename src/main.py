# -*- coding: utf-8 -*-
from config import BUS_DATA_URL, GEOJSON_URL
from config import get_db_params

from extract import extract_business_data, extract_geojson
from transform import transform
from load import load
from get_dashboard_data import get_dashboard_data

from get_app import get_app

from pipes_and_filters import UgPipe, UtilityPipe, DatePipe, DecimalPipe

# maybe ORM makes this better

# design to incrementally load more data into the database and building 
# an updated dashboard from it

if __name__ == '__main__':
    # EXTRACT
    
    # it does not save the csv file locally
    
    # wrap into try-except
    df = extract_business_data(BUS_DATA_URL) 
    
    #==========================================================================
    # TRANSFORM
    old_cols = ('ug_code', 'utility_code', 'date_', 'value_')
    new_cols = ('ug_id',   'utility_id',  'date_', 'value_') 
    pipes = (UgPipe, UtilityPipe, DatePipe, DecimalPipe)
    
    trans_df = transform(df, old_cols, new_cols, pipes) 
    
    #==========================================================================
    # LOAD
    db_params = get_db_params()
    
    load(trans_df, db_params)

    #==========================================================================
    # GET THE AGGREGATED DATA FOR THE DASHBOARD
    dashboard_df = get_dashboard_data(db_params) 
    
    #==========================================================================
    # BUILD DASHBOARD
    geojson = extract_geojson(GEOJSON_URL)
    
    app = get_app(dashboard_df, geojson)
    app.run_server(debug = True, use_reloader = False)
    
    

    
    