import streamlit as st
import pandas as pd
import requests
from urllib.error import URLError
from streamlit_gsheets import GSheetsConnection

# Adding a title for the app

st.title('🍞 Falomy Boulanger🥖')
st.text('"Où la farine et le sucre dansent avec délice"')


#Trying, to be deleted

# example/st_app.py

url = "https://docs.google.com/spreadsheets/d/1JDy9md2VZPz4JbYtRPJLs81_3jUK47nx6GYQjgU8qNY/edit?usp=sharing"
conn = st.experimental_connection("gsheets", type=GSheetsConnection)
data = conn.read(spreadsheet=url, usecols=[0, 1])
st.dataframe(data)




#st.header('Ventes et dépenses quotidiennes de boulangerie')
# This is to add Images as needed
#import streamlit as st
#st.image('sunrise.jpg', caption='Sunrise by the mountains')
