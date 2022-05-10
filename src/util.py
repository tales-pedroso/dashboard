# -*- coding: utf-8 -*-
from contextlib import contextmanager
import psycopg2

# this is repetitive

@contextmanager
def create_commit_close(db_params):
    conn = psycopg2.connect(**db_params)
    
    yield conn.cursor()
    
    conn.commit()
    conn.close()

@contextmanager
def create_close(db_params):
    conn = psycopg2.connect(**db_params)
    
    yield conn
    conn.close()