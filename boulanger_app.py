import pandas as pd
import gspread as gs
from google.oauth2 import service_account
import streamlit as st
from datetime import datetime, timedelta
import plotly.express as px

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

# Convert the 'Date du compte rendu?' column to Pandas Timestamp
df['Date du compte rendu?'] = pd.to_datetime(df['Date du compte rendu?'])


# getting the employee info
# employee = client.open('Test1').get_worksheeet(1)
# records1 = employee.get_all_records()
# df1 = pd.DataFrame.from_dict(records1)

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

# Add separate date inputs for start and end dates
start_date = pd.to_datetime(st.sidebar.date_input("Select Start Date", datetime.now() - timedelta(days=7)))
end_date = pd.to_datetime(st.sidebar.date_input("Select End Date", datetime.now()))

# Filter DataFrame based on the selected date range
filtered_df = df[df['Date du compte rendu?'].between(start_date, end_date)]

# Display the filtered DataFrame
st.write(filtered_df)

# TOP KPI's
numeric_columns = filtered_df.select_dtypes(include='number').columns
total_sales = filtered_df[numeric_columns].sum(axis=1)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    formatted_total_sales = f"HT {total_sales.sum():,}" if total_sales.dtype in ['int64', 'float64'] else total_sales.sum()

    # Increase font size using HTML-style tags
    st.subheader("Total Sales:")
    st.markdown(f"<p style='font-size: 24px;'>{formatted_total_sales}</p>", unsafe_allow_html=True)


# with left_column:
#     formatted_total_sales = f"HT {total_sales.sum():,}" if total_sales.dtype in ['int64', 'float64'] else total_sales.sum()
#     st.subheader("Total Sales:")
#     st.write(formatted_total_sales)

st.markdown("""---""")


# Assuming your DataFrame has a datetime column named 'Date du compte rendu?'
df['Date du compte rendu?'] = pd.to_datetime(df['Date du compte rendu?'])

# Extract month from the 'Date du compte rendu?' column
df['Month'] = df['Date du compte rendu?'].dt.month_name()

# Group by month and sum the 'Total' sales
sales_by_month = df.groupby(by=["Month"])[["total_sales"]].sum().reset_index()

# Create a bar chart for sales by month
fig_monthly_sales = px.bar(
    sales_by_month,
    x="Month",
    y="total_sales",
    title="<b>Sales by Month</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_month),
    template="plotly_white",
)

fig_monthly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)



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
