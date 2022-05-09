# -*- coding: utf-8 -*-
from contextlib import contextmanager
import psycopg2

# this is repetitive

@contextmanager
def create_commit_close(database, user, password, host, port):
    conn = psycopg2.connect(database = database,
                            user = user,
                            password = password,
                            host = host,
                            port = port)
    yield conn.cursor()
    conn.commit()
    conn.close()

@contextmanager
def create_close(database, user, password, host, port):
    conn = psycopg2.connect(database = database,
                            user = user,
                            password = password,
                            host = host,
                            port = port)
    yield conn
    conn.close()