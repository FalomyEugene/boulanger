import os
import streamlit as st
import pandas as pd
import subprocess
#from gspread.service_account import ServiceAccountCredentials
import toml
#from google.oauth2 import service_account
#from googleapiclient.discovery import build

# Load Google Sheets credentials from secrets.toml
gsheets_config = st.secrets["connections.gsheets"]

# Load service account credentials
credentials = service_account.Credentials.from_service_account_info({
    "type": gsheets_config["type"],
    "project_id": gsheets_config["project_id"],
    "private_key_id": gsheets_config["private_key_id"],
    "private_key": gsheets_config["private_key"].replace("\\n", "\n"),
    "client_email": gsheets_config["client_email"],
    "client_id": gsheets_config["client_id"],
    "auth_uri": gsheets_config["auth_uri"],
    "token_uri": gsheets_config["token_uri"],
    "auth_provider_x509_cert_url": gsheets_config["auth_provider_x509_cert_url"],
    "client_x509_cert_url": gsheets_config["client_x509_cert_url"],
})

# Connect to Google Sheets API
service = build('sheets', 'v4', credentials=credentials)

# Read data from Google Sheets
spreadsheet_url = gsheets_config["spreadsheet"]
worksheet = gsheets_config["worksheet"]

# Example: Reading data from Google Sheets
try:
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_url, range=worksheet).execute()
    values = result.get('values', [])

    if not values:
        st.write("No data found.")
    else:
        # Display the data in a DataFrame
        df = pd.DataFrame(values[1:], columns=values[0])
        st.write("Data from Google Sheets:")
        st.write(df)

except Exception as e:
    st.write("An error occurred:", e)

