# -*- coding: utf-8 -*-
def change_one_col(df, col, pipe):
    s = df[col]
    pipe = pipe()
    df[col] = pipe.execute(s)
    
    return df

def transform(df, cols, pipes):
    zip_obj = zip(cols, pipes)
    
    for col, pipe in zip_obj:
        df = change_one_col(df, col, pipe)
        
    return df