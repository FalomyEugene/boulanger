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

# Add a date filter in the sidebar
selected_date = st.sidebar.date_input("Select Date", datetime.now())

# Filter DataFrame based on the selected date
filtered_df = df[df['1. Date du compte rendu?'].dt.date == selected_date.date()]

# Display the filtered DataFrame
st.write(filtered_df)


#st.sidebar.text("This is additional content in the sidebar.")


# TOP KPI's
numeric_columns = df.select_dtypes(include='number').columns
total_sales = df[numeric_columns].sum(axis=1)


left_column, middle_column, right_column = st.columns(3)
with left_column:
    # Format total_sales only if it's a numeric value, otherwise display as is
    formatted_total_sales = f"US $ {total_sales.sum():,}" if total_sales.dtype in ['int64', 'float64'] else total_sales.sum()

    # Display the formatted total sales
    st.subheader(f"Total Sales: {formatted_total_sales}")

   # st.subheader("Total Sales:")
   # st.subheader(f"US $ {total_sales:,}")

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
