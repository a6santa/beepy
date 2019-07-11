import json
import os

def reader_json(path='src/etl/config/auth_conn.json'):
    arq = open(f'{path}', 'r')
    data = json.load(arq)
    arq.close()
    return data