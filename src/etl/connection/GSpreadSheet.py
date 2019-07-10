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

    def get_worksheet_to_json(self, name_worksheet):
        return self.spreadsheet.worksheet(name_worksheet).get_all_records()
    
    def create_worksheet(self, name_worksheet,rows="50000", cols="50"):
        self.spreadsheet.add_worksheet(title=name_worksheet,rows=rows, cols=cols)
    
    def del_worksheet(self, name_worksheet):
        self.spreadsheet.del_worksheet(self.spreadsheet.worksheet(name_worksheet))
    
    def full_load(self, name_worksheet, data,name_cols=None,truncate=False):
        work = self.spreadsheet.worksheet(name_worksheet)
        
        def set_cols(work, cols):
            work.insert_row(values=cols, value_input_option='USER_ENTERED')
        
        if truncate:
            if name_cols is not None:
                cols = name_cols
            else:
                cols = work.get_all_values()[0]
            work.clear()
            set_cols(work, cols)
        
        for d in data:
            work.append_row(d, value_input_option='USER_ENTERED')

if __name__ == '__main__':
    import os
    import etl.util.reader_json as rj
    
    name_conn = 'google'
    auth = os.environ.get(rj.reader_json(path='src/etl/config/auth_conn.json')[name_conn]['file_path'])
    print('get values in spreadsheet')
    G = GSpreadSheet(
        auth,
        key='1J8jA-atpyIpH47gEMUmlGdcrxj6dIsUGRtLbeVSlKOE'
        )

    df= G.get_worksheet_to_pandas('sales')
    print(df)

    print('full load in spreadsheet')
    data= [
        ['15/07/2019','Carlos José',105.40,'15/09/2019'],
        ['16/07/2019','Maria Aparecida',2000.45],
        ['17/07/2019','Rodinei de Jesus',50.45,'17/09/2019'],
        ['18/07/2019','Carlos Eduardo',19.08],
        ['19/07/2019','Carlos José',105.40,'19/09/2019'],
        ['20/07/2019','Maria Aparecida',2000.45,'20/09/2019']
    ]
    G.full_load(name_worksheet='sales', data=data)