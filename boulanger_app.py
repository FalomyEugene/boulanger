import pandas as pd
import gspread as gs
from google.oauth2 import service_account
import streamlit as st
from datetime import datetime


SCOPES = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]
SERVICE_ACCOUNT_FILE = 'boulanjer cred.json'

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

client = gs.authorize(credentials)


sheet = client.open('Test1')
edutech_data = sheet.get_worksheet(0)
edutech_data = edutech_data.get_all_records()
# edutech_data

edutech_df = pd.DataFrame.from_dict(edutech_data)
st.write(edutech_df.head(3))
# edutech_df.head(3)
# print(edutech_df)

# ---- MAINPAGE ----
st.title(":bar_chart: Rapport - hebdomadaire")
st.markdown("##")


# Get the current date and time

current_date_time = datetime.now()
# Format the date as a string
formatted_date = current_date_time.strftime("%Y-%m-%d %H:%M:%S")
# Display the date in your Streamlit app
st.write("Current Date and Time:", formatted_date)



