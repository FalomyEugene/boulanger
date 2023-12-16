import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Adding a title and description
st.title('🍞 Falomy Boulanger🥖')
st.markdown('"Où la farine et le sucre dansent avec délice"')

# Google Sheets authentication
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('path/to/your/credentials.json', scope)
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
