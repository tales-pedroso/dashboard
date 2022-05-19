# -*- coding: utf-8 -*-
import pandas as pd
from util import create_close

def get_sql_statement(proc_name):
    sql = f'SELECT * FROM {proc_name}()'
    return sql

def get_dashboard_data(db_params):
    # gets aggregated data state_, month_, total_expense
    with create_close(db_params) as conn:
        # requires function called get_dashboard_data saved in the database
        sql = get_sql_statement('get_dashboard_data') 
        
        df = pd.read_sql(sql, conn)
        
    return df
