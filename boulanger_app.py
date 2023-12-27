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
sheet = sheet.get_worksheet(1)
sheet = sheet.get_all_records()
# edutech_data

sheet = pd.DataFrame.from_dict(sheet)
st.write(sheet.head(3))
 #edutech_df.head(3)
# print(edutech_df)

# ---- MAINPAGE ----
st.title(":bar_chart: Rapport - hebdomadaire")
st.markdown("##")


# Get the current date and time


# ---- SIDEBAR ----
st.sidebar.header("Rapportez Ici:")

# Get input data from user
date = st.sidebar.date_input("Date", datetime.now())

# Define the materials
mat_options = ["Farine", "Mantegue", "Bois", "Gaz", "Sucre", "Ledvin", "Sel", "Autre"]

# Multiselect for selecting the mat
selected_mat = st.sidebar.multiselect("Select the mat:", mat_options)

# Create a dictionary to store the values for each selected material
mat_values = {}

# Loop through selected materials and get corresponding numbers
for mat in selected_mat:
    value = st.sidebar.number_input(f"Enter value for {mat}", key=mat)
    mat_values[mat] = value

# Prepare data to be updated
data_to_update = [date] + [mat_values.get(mat, 0) for mat in mat_options[:-1]]

# Update Google Sheet
sheet.append_row(data_to_update)

st.success("Data updated successfully.")

