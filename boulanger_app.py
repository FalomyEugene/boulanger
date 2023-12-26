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
st.sidebar.header("Please Filter Here:")

# Multiselect for selecting the mat
mat_options = ["Farine", "Mantegue", "Bois", "Gaz", "Sucre", "Ledvin", "Sel"]
selected_mat = st.sidebar.multiselect("Select the mat:", mat_options)

# Get input data from user
date = st.sidebar.date_input("Date", datetime.now())
farine = st.sidebar.number_input("Farine")
mantegue = st.sidebar.number_input("Mantegue")
bois = st.sidebar.number_input("Bois")
gaz = st.sidebar.number_input("Gaz")
sucre = st.sidebar.number_input("Sucre")
ledvin = st.sidebar.number_input("Ledvin")
sel = st.sidebar.number_input("Sel")

# Now you can use the selected values in your Streamlit app as needed

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



