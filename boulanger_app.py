import streamlit as st
import pandas as pd
import requests
from urllib.error import URLError
#from streamlit_gsheets import GSheetsConnection

# Adding a title and description

st.title('🍞 Falomy Boulanger🥖')
st.markdown('"Où la farine et le sucre dansent avec délice"')

#establishing a goodgle sheet connection

conn = st.experimental_connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="test1", usecols=list(range(6)), ttl=5)
df = df.dropna(how="all")


st.dataframe(df)




#st.header('Ventes et dépenses quotidiennes de boulangerie')
# This is to add Images as needed
#import streamlit as st
#st.image('sunrise.jpg', caption='Sunrise by the mountains')
