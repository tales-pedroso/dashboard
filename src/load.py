# -*- coding: utf-8 -*-
from sys import exc_info
from util import create_commit_close

def get_sql_statement(named_tuple):
    ug_id = named_tuple.ug_id
    utility_id = named_tuple.utility_id
    dh_id = named_tuple.dh_id
    date_ = named_tuple.date_
    value_ = named_tuple.value_ 
    
    sql = f'''INSERT INTO factpayment (ug_id, utility_id, dh_id, date_, value_)
          VALUES ('{ug_id}', '{utility_id}', '{dh_id}', '{date_}', {value_});   
          '''
    return sql
    
def load_one_row(cursor, sql):
    try:
        cursor.execute(sql) # creates transaction implictly
        print('One row successfully loaded')
    except:
        print(exc_info()) # prints will become logs later on
        cursor.execute('ROLLBACK')
        
def load(trans_df, db_params):
    with create_commit_close(db_params) as cursor:
    
        for named_tuple in trans_df.itertuples():
            sql = get_sql_statement(named_tuple)
            load_one_row(cursor, sql)