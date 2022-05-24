# -*- coding: utf-8 -*-
from configparser import ConfigParser

# EXTRACT

BUS_DATA_URL = 'https://raw.githubusercontent.com/tales-pedroso/dashboard/main/data_files/business_data.csv'
GEOJSON_URL = 'https://raw.githubusercontent.com/tales-pedroso/dashboard/main/data_files/brazilian_states.json'

# Database
INI_FILE = 'database.ini'
SECTION = 'postgresql'

def get_db_params(ini_file = INI_FILE, section = SECTION):
    '''
    https://www.postgresqltutorial.com/postgresql-python/connect/
    '''
    parser = ConfigParser()
    parser.read(ini_file)
    
    if parser.has_section(section):
        params = parser.items(section) # list of tuples that need to be unpacked
        
        db_params = {param[0]:param[1] for param in params}
        
    else:
        raise Exception(f'Section {section} not found in {ini_file}')
    
    return db_params
                                   
