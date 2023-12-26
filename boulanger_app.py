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


# ---- SIDEBAR ----

# Get input data from user
date = st.date_input("Date", datetime.now())
farine = st.number_input("Farine")
mantegue = st.number_input("Mantegue")
bois = st.number_input("Bois")
gaz = st.number_input("Gaz")
sucre = st.number_input("Sucre")
ledvin = st.number_input("Ledvin")
sel = st.number_input("Sel")

# Prepare data to be updated
data_to_update = [date, farine, mantegue, bois, gaz, sucre, ledvin, sel]

# Update Google Sheet
sheet.append_row(data_to_update)

st.success("Data updated successfully.")

current_date_time = datetime.now()
# Format the date as a string
formatted_date = current_date_time.strftime("%Y-%m-%d %H:%M:%S")
# Display the date in your Streamlit app
st.write("Last Updated:", formatted_date)



