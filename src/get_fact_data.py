# -*- coding: utf-8 -*-
import pandas as pd
from util import create_close

def get_sql_statement(table_name):
    sql = f'SELECT * FROM {table_name}'
    return sql

def get_fact_data(database, user, password, host, port):
    with create_close(database, user, password, host, port) as conn:
        sql = get_sql_statement('factpayment')
        df = pd.read_sql(sql, conn)
        
    return df



