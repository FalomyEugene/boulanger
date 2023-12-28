import pandas as pd
import gspread as gs
from google.oauth2 import service_account
import streamlit as st
from datetime import datetime
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
st.write(df.head(3))

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


#st.sidebar.text("This is additional content in the sidebar.")


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
