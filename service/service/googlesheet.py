import json
import os
from datetime import datetime

import apiclient
import httplib2
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

TRACKED_SHEET_HEADER_OFFSET = 1
CHUNK_SIZE = 1000
TRACKED_SHEET_NAME = 'SourceSheet'
START_COLUMN = 'A'
END_COLUMN = 'D'
CREDENTIALS_FILE = 'creds.json'


class GSheets:
    def __init__(self):
        """Инициализация переменных  и данных."""
        with open(os.path.join(
            'secret/', 'gsheets_cached_config.json'
        ), 'r') as config_file:
            json_data = json.load(config_file)

        self.spreadsheet_id = '1asMC2phmDnNOx_wBsCLLqiz7LOXHrO32zCMM5GIXUXo'
        self.main_sheet_id = 123456
        self.start_page_token = json_data.get('startPageToken')
        self.page_token = '0'
        self.last_update = '0'

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())

        self.service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
        self.drive_service = apiclient.discovery.build(
            'drive', 'v3', http=httpAuth
        )

    def get_values(self):
        """Метод для извлечения данных с гугл-таблицы."""
        values = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range='A2:D',
            majorDimension='ROWS'
        ).execute()
        return values.get('values')

    def dump_config(self):
        """Метод записывает данные о гугл-таблице в файл."""
        with open(os.path.join(
            'secret/', 'gsheets_cached_config.json'
        ), 'w') as config_file:
            json.dump({
                "spreadsheetId": self.spreadsheet_id,
                "mainSheetId":   self.main_sheet_id,
                "startPageToken": self.start_page_token,
                "lastUpdate": self.last_update,
            }, config_file)

    # def first(self):
    #     response = self.drive_service.changes().getStartPageToken().execute()
    #     print(response)

    def check_changes(self):
        """Метод проверяет то, были ли изменения в гугл-табдице."""
        self.page_token = self.start_page_token
        were_changes_in_a_file = False
        start_page_token = self.start_page_token

        try:
            while self.page_token is not None:

                response = self.drive_service.changes().list(
                    pageToken=self.page_token,
                    spaces='drive',
                ).execute()

                for change in response.get('changes'):
                    file_id = change.get("fileId")
                    if file_id == self.spreadsheet_id:
                        were_changes_in_a_file = True
                        print('Changes was found')
                if 'newStartPageToken' in response:
                    self.start_page_token = response.get('newStartPageToken')
                self.page_token = response.get('nextPageToken')

            if start_page_token != self.start_page_token:
                self.last_update = f'{datetime.now():%X %d.%m.%Y}'
                self.dump_config()

        except Exception as e:
            print(f'GSheets error: unable to fetch {self.spreadsheet_id} table with Google Sheets API:', e)
        finally:
            return were_changes_in_a_file
