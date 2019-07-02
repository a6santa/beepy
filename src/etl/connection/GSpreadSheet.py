import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

class GSpreadSheet(object):
    def __init__(self,file_auth,url=None,name=None,key=None,new=False):
        self.file_auth = file_auth
        self.scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.file_auth, self.scope)
        self.conn = gspread.authorize(self.creds)
        
        if not new:
            if url is not None:
                self.spreadsheet = self.conn.open_by_url(url)
            elif name is not None:
                self.spreadsheet = self.conn.open(name)
            elif key is not None:
                self.spreadsheet = self.conn.open_by_key(key)
            else:
                raise Exception('Not Found spreadsheet')
        else:
            if name is None:
                name='new_spread_sheet'
            _spreadsheet = self.conn.create(name)
            self.spreadsheet = self.conn.open(name)


    def __str__(self):
        return 'GspreadSheet: {scope}'.format(scope=self.scope)

    def __repr__(self):
        return self.__str__()
        

    def get_worksheet_to_pandas(self, name_worksheet):
        return pd.DataFrame(self.spreadsheet.worksheet(name_worksheet).get_all_records())

    def get_worksheet(self, name_worksheet):
        return self.spreadsheet.worksheet(name_worksheet).get_all_records()
    
    def create_worksheet(self, name_worksheet):
        pass
    
    def del_worksheet(self, name_worksheet):
        pass
    
    def full_load(self, name_worksheet, data,name_cols=None, truncate=False, version=False):
        pass
    
    def insert(self, name_worksheet,tupla):
        pass

if __name__ == '__main__':
    import os
    import etl.util.reader_json as rj
    name_conn = 'google'
    auth = os.environ.get(rj.reader_json(path='src/etl/config/auth_conn.json')[name_conn]['file_path'])
    G = GSpreadSheet(auth)
    df = G.get_spreadsheet('1J8jA-atpyIpH47gEMUmlGdcrxj6dIsUGRtLbeVSlKOE', 'sales')
    print(df)