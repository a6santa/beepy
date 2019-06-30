import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

class GSpreadSheet(object):
    """
        classe para inserção e busca de dados nas planilhas do Google
        Atenção é nescessario a as chaves em arquivo json para a conexão

        Parâmetros
        
        scope_list : lista com serviços do google para se conectar
            ex: ['https://spreadsheets.google.com/feeds']
        
        file_auth = arquivo json de autenticacao na api Google  
    """
    def __init__(self, file_auth):
        self.file_auth = file_auth
        self.scope = ['https://spreadsheets.google.com/feeds']
        
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.file_auth, self.scope)

        self.conn = gspread.authorize(self.creds)


    def __str__(self):
        return 'GspreadSheet: {scope}'.format(scope=self.scope)

    def __repr__(self):
        return self.__str__()

    def get_spreadsheet_to_pandas(self, id_spreadsheet=None, name_worksheet=None):
        """
            id_spreadsheet: id da planilha do google
                EX:.
                    '1Scm62YFz8s6DL2INsaW6otiPxlYQI_9imxFANvQwYLc'
            name_worksheet: nome da pasta de trabalho da planilha selecionada
        """
        return pd.DataFrame(self.conn.open_by_key(id_spreadsheet).worksheet(name_worksheet).get_all_records())

    def get_spreadsheet(self, id_spreadsheet=None, name_worksheet=None):
        """
            id_spreadsheet: id da planilha do google
                EX:.
                    '1Scm62YFz8s6DL2INsaW6otiPxlYQI_9imxFANvQwYLc'
            name_worksheet: nome da pasta de trabalho da planilha selecionada
        """
        return self.conn.open_by_key(id_spreadsheet).worksheet(name_worksheet).get_all_records()

if __name__ == '__main__':
    import os
    import etl.util.reader_json as rj
    name_conn = 'google'
    auth = os.environ.get(rj.reader_json(path='src/etl/config/auth_conn.json')[name_conn]['file_path'])
    G = GSpreadSheet(auth)
    df = G.get_spreadsheet('1J8jA-atpyIpH47gEMUmlGdcrxj6dIsUGRtLbeVSlKOE', 'sales')
    print(df)