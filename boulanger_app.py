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

# Open the second worksheet
worksheet = client.open('Test1').get_worksheet(1)

# Get all records from the worksheet
records = worksheet.get_all_records()

# Convert records to a DataFrame
df = pd.DataFrame.from_dict(records)
st.write(df.head(3))

# ---- MAINPAGE ----
st.title(":bar_chart: Rapport - hebdomadaire")
st.markdown("##")

# ---- SIDEBAR ----
st.sidebar.header("Rapportez Ici:")

# Get input data from user
date = st.sidebar.date_input("Date", datetime.now())
# Convert date to a string
date_str = date.strftime("%Y-%m-%d")

# Define the materials
mat_options = ["Farine", "Mantegue", "Bois", "Gaz", "Sucre", "Ledvin", "Sel", "Excell", "Autre"]

# Initialize session state
if "mat_values" not in st.session_state:
    st.session_state.mat_values = {mat: 0 for mat in mat_options}

# Loop through each material and create an input field for its value
for mat in mat_options:
    # Use st.number_input to display the value
    value = st.sidebar.number_input(f"Enter value for {mat}", key=mat, value=st.session_state.mat_values[mat])
    st.session_state.mat_values[mat] = value

# Display the current values on the sidebar
st.sidebar.write("Current values:")
for mat in mat_options:
    st.sidebar.write(f"{mat}: {st.session_state.mat_values[mat]}")

# Add a custom submit button with on_click method
submit_button = st.sidebar.button("Submit")

# Use on_click method to set values to zero after submission
if submit_button:
    # Prepare data to be updated
    data_to_update = [date_str] + [st.session_state.mat_values.get(mat, 0) for mat in mat_options]

    # Update the worksheet with the new row
    worksheet.append_row(data_to_update)

    st.success("Data updated successfully.")
    
    # Set values to zero after submission
    st.session_state.mat_values = {mat: 0 for mat in mat_options}
