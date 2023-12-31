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

# Convert the 'Date du compte rendu?' column to Pandas Timestamp
df['Date du compte rendu?'] = pd.to_datetime(df['Date du compte rendu?'])

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
#st.write(filtered_df)

# TOP KPI's
numeric_columns = filtered_df.select_dtypes(include='number').columns
total_sales = filtered_df[numeric_columns].sum(axis=1)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    formatted_total_sales = f"HT {total_sales.sum():,}" if total_sales.dtype in ['int64', 'float64'] else total_sales.sum()

    # Increase font size using HTML-style tags
    st.subheader("Total Sales:")
    st.markdown(f"<p style='font-size: 24px;'>{formatted_total_sales}</p>", unsafe_allow_html=True)
    
with middle_column:
    # Calculate total profit
    benefit_total = filtered_df["11. Benefice"].sum()
    formatted_benefit_total = f"HT {benefit_total:,}"

    # Display the total profit
    st.subheader("Total Profit:")
    st.markdown(f"<p style='font-size: 24px;'>{formatted_benefit_total}</p>", unsafe_allow_html=True)


# I want to do Avererage weekly sales
with right_column:
    # Assuming your DataFrame has a datetime column named 'Date du compte rendu?'
    filtered_df['Week'] = filtered_df['Date du compte rendu?'].dt.strftime('%Y-%U')

    # Calculate weekly average sales for each week
    weekly_avg_sales = filtered_df.groupby('Week')[numeric_columns].mean()

    # Calculate the overall average of weekly averages
    overall_avg_sales = weekly_avg_sales.mean().mean()

    # Format and display the overall weekly average sales
    formatted_weekly_avg_sales = f"HT {overall_avg_sales:,.2f}"
    st.subheader("Weekly Average Sales:")
    st.markdown(f"<p style='font-size: 24px;'>{formatted_weekly_avg_sales}</p>", unsafe_allow_html=True)



st.markdown("""---""")

left_column, right_column = st.columns(2)

with left_column:
    # Assuming your DataFrame has a datetime column named 'Date du compte rendu?'
    df['Date du compte rendu?'] = pd.to_datetime(df['Date du compte rendu?'])

    # Extract month from the 'Date du compte rendu?' column
    df['Month'] = df['Date du compte rendu?'].dt.month_name()

    # Calculate total sales dynamically based on numeric columns
    numeric_columns = df.select_dtypes(include='number').columns
    df['Total Sales'] = df[numeric_columns].sum(axis=1)

    # Group by month and sum the 'Total Sales'
    sales_by_month = df.groupby(by=["Month"])[["Total Sales"]].sum().reset_index()

    # Create a bar chart for sales by month using Streamlit
    st.bar_chart(sales_by_month.set_index("Month"))


with right_column:
    # Assuming your DataFrame has a datetime column named 'Date du compte rendu?'
    filtered_df['DayOfWeek'] = filtered_df['Date du compte rendu?'].dt.day_name()

    # Calculate average sales for each day of the week
    avg_sales_per_day = filtered_df('DayOfWeek')[numeric_columns].mean()

    # Transpose the DataFrame to swap x and y axes
    avg_sales_per_day_transposed = avg_sales_per_day.transpose()

    # Create a bar chart for average sales per day using Streamlit
    st.bar_chart(avg_sales_per_day_transposed)

    # Set chart labels and title using Streamlit functions
    st.xlabel("Average Sales")
    st.ylabel("Day of the Week")
    st.title("Average Sales Per Day")
    st.subheader("Average Sales Per Day:")



# with right_column:
#     # Calculate average sales per day
#     avg_sales_per_day = filtered_df[numeric_columns].mean(axis=0)

#     # Create a line chart for average sales per day using Streamlit
#     st.line_chart(avg_sales_per_day)

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
