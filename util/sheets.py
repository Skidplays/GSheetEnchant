import gspread
from gspread.models import Worksheet
from oauth2client.service_account import ServiceAccountCredentials

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def update_sheets(sheet_num:int, values: list, col:str):
    sheet = client.open('Lab Enchants').get_worksheet(sheet_num)
    count = len(values)
    cell_range = f'{col}2:{col}{str(count+1)}'
    cell_list = sheet.range(cell_range)
    for idx, val in enumerate(values):
        cell_list[idx].value = val
    sheet.update_cells(cell_list)


creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scopes)

client = gspread.authorize(creds)
