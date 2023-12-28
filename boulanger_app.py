import pandas as pd
import gspread as gs
from google.oauth2 import service_account
import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Boulanger Rapport", page_icon=":bar_chart:", layout="wide")

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
SERVICE_ACCOUNT_FILE = 'boulanjer cred.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

client = gs.authorize(credentials)

# Open the second worksheet
worksheet = client.open('Test1').get_worksheet(0)

# Get all records from the worksheet
records = worksheet.get_all_records()

# Convert records to a DataFrame
df = pd.DataFrame.from_dict(records)

# ---- MAINPAGE ----

st.title(":bar_chart: Boulangerie Rapport De Vente")
st.markdown("##")

# ---- SIDEBAR ----

# Replace 'YOUR_GOOGLE_FORM_URL' with the actual URL of your Google Form
google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfw0wN0hundqYfBytzI_P1KBG5MrTsdwlAMmd1wz41hd5T7xA/viewform"

# Additional content in the sidebar
st.sidebar.header(":baguette_bread: Cliquez Ici :baguette_bread:")

# Create a hyperlink to the Google Form
st.sidebar.markdown(f"[ Boulanger Rapport]({google_form_url})")

# Add a date range filter in the sidebar
start_date = st.sidebar.date_input("Select Start Date", datetime.now() - timedelta(days=7))
end_date = st.sidebar.date_input("Select End Date", datetime.now())

# Convert the date column to datetime if it's stored as a string
df['1. Date du compte rendu?'] = pd.to_datetime(df['1. Date du compte rendu?'], errors='coerce')

# Filter DataFrame based on the selected date range
filtered_df = df[
    (df['1. Date du compte rendu?'].dt.floor("D") >= start_date) & 
    (df['1. Date du compte rendu?'].dt.floor("D") <= end_date)
]

# Display the filtered DataFrame
st.write(filtered_df)

# TOP KPI's
numeric_columns = filtered_df.select_dtypes(include='number').columns
total_sales = filtered_df[numeric_columns].sum(axis=1)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    formatted_total_sales = f"US $ {total_sales.sum():,}" if total_sales.dtype in ['int64', 'float64'] else total_sales.sum()
    st.subheader(f"Total Sales: {formatted_total_sales}")

st.markdown("""---""")

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Rest of your Streamlit app
# ...
