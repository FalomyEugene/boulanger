import pandas as pd
import gspread as gs
from google.oauth2 import service_account
import streamlit as st


SCOPES = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]
SERVICE_ACCOUNT_FILE = r'C:\Users\Feugene\boulanjer secrets.toml'

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

client = gs.authorize(credentials)


sheet = client.open('Test1')
edutech_data = sheet.get_worksheet(0)
edutech_data = edutech_data.get_all_records()
edutech_data

edutech_df = pd.DataFrame.from_dict(edutech_data)
edutech_df.head(3)
print(edutech_df)
