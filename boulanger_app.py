import os
import streamlit as st
import pandas as pd
#from oauth2client.service_account import ServiceAccountCredentials
import toml

# Retrieve credentials from environment variables
client_email = os.environ.get("GOOGLE_SHEETS_CLIENT_EMAIL")
private_key = os.environ.get("GOOGLE_SHEETS_PRIVATE_KEY") #.replace('\\n', '\n')  # Replace escaped newlines

# Authenticate with Google Sheets
# Authenticate with Google Sheets using service account file
creds_dict = {
    "client_email": client_email,
    "private_key": private_key,
    "type": "service_account",
    "project_id": "boulanger-408218",
    "private_key_id": "a30fa345c1c99cceb7e6c184e2a7330fffdbbc0a",
    "client_id": "109713103821114642089",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/boulanjesheet%40boulanger-408218.iam.gserviceaccount.com"
}
gc = gspread.authorize(credentials)

# Open the Google Sheet
worksheet = gc.open('Your Google Sheet Name').sheet1

# Get data from the Google Sheet
data = worksheet.get_all_values()

# Create a DataFrame
df = pd.DataFrame(data[1:], columns=data[0])

# Display the DataFrame
st.dataframe(df)





#st.header('Ventes et dépenses quotidiennes de boulangerie')
# This is to add Images as needed
#import streamlit as st
#st.image('sunrise.jpg', caption='Sunrise by the mountains')
