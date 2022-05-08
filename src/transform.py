# -*- coding: utf-8 -*-

def change_one_col(df, old_col, new_col, pipe):
    s = df[old_col]
    pipe = pipe()
    df[old_col] = pipe.execute(s)
    df.rename(columns = {old_col : new_col}, inplace = True)
    
    return df

def transform(df, old_cols, new_cols, pipes):
    zip_obj = zip(old_cols, new_cols, pipes)
    
    for old_col, new_col, pipe in zip_obj:
        df = change_one_col(df, old_col, new_col, pipe)
        
    return df
