import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Step 1: Connect to Google Sheets and Read Data
# Define scope and authenticate using service account credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('your-credentials-file.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheet by name
sheet = client.open("Your Google Sheet Name").sheet1

# Get all values and load into a pandas DataFrame
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Fetch data from Google Sheet
subs = df.loc[df['Metric'] == 'Subscribers', 'Value'].values[0]
page_views = df.loc[df['Metric'] == 'Page Views', 'Value'].values[0]
rcpm_display = df.loc[df['Metric'] == 'Overall rCPM Display Ads', 'Value'].values[0]
rcpm_video = df.loc[df['Metric'] == 'Overall rCPM Video Ads', 'Value'].values[0]

# Page configuration
st.set_page_config(page_title="Enhanced Revenue Projections Dashboard", layout="centered")

# Title
st.title("TOL Revenue Projections")

# Step 2: Input Components in Collapsible Sections

# Subs & Engagement Section
with st.expander("Subs & Engagement", expanded=False):
    # Checkbox for Subscription Revenue
    include_subscriptions = st.checkbox("Include Subscription Revenue", value=True)

    # Subscribers and Engagement (using Google Sheet data)
    subscribers = st.slider("Subscribers", min_value=1000, max_value=50000, value=int(subs), step=500)
    engagement_increase = st.slider("Engagement Rate Increase (%)", min_value=-50, max_value=50, value=0, step=1)
    avg_sub_paid = st.number_input("Monthly ARPU (€)", min_value=1.0, max_value=30.0, value=4.50)

# Display Revenue Section
with st.expander("Display Revenue", expanded=False):
    include_display_ads = st.checkbox("Include Display Ad Revenue", value=True)

    # Effective CPM for Display Ads from Google Sheet or as an input
    overall_rcpm_display = st.number_input("Overall rCPM for Display Ads (€)", min_value=0.5, max_value=20.0, value=rcpm_display)

# Video Revenue Section
with st.expander("Video Revenue", expanded=False):
    include_video_ads = st.checkbox("Include Video Ad Revenue", value=True)

    # Effective CPM for Video Ads from Google Sheet or as an input
    overall_rcpm_video = st.number_input("Overall rCPM for Video Ads (€)", min_value=0.5, max_value=20.0, value=rcpm_video)

# Native Content Section
with st.expander("Native Content", expanded=False):
    include_native_content = st.checkbox("Include Native Content Revenue", value=True)

    # Native Content Revenue Inputs
    natives_per_month = st.number_input("Number of Native Articles Per Month", min_value=0, value=1)
    avg_cost_per_native = st.number_input("Average Revenue Per Native Article (€)", min_value=0.0, value=4000.0)

# Step 3: Calculations

# Subscription Revenue
monthly_subscription_revenue = subscribers * avg_sub_paid
annual_subscription_revenue = monthly_subscription_revenue * 12 if include_subscriptions else 0

# Native Content Revenue Calculations
monthly_native_revenue = natives_per_month * avg_cost_per_native
annual_native_revenue = monthly_native_revenue * 12 if include_native_content else 0

# Display Ad Revenue Calculations using overall rCPM
base_impressions_display = (subscribers / 12000) * 2.5e6  # Scale with subscribers
additional_impressions_display = (engagement_increase / 100) * base_impressions_display
total_impressions_display = base_impressions_display + additional_impressions_display

# Use overall rCPM for Display Ads
monthly_display_ad_revenue = (total_impressions_display / 1000) * overall_rcpm_display
annual_display_ad_revenue = monthly_display_ad_revenue * 12 if include_display_ads else 0

# Video Ad Revenue Calculations using overall rCPM
base_impressions_video = (subscribers / 12000) * 50000  # Scale video impressions with subscribers
additional_impressions_video = (engagement_increase / 100) * base_impressions_video
total_impressions_video = base_impressions_video + additional_impressions_video

# Use overall rCPM for Video Ads
monthly_video_ad_revenue = (total_impressions_video / 1000) * overall_rcpm_video
annual_video_ad_revenue = monthly_video_ad_revenue * 12 if include_video_ads else 0

# Total Revenue Calculations
annual_total_revenue = (
    annual_subscription_revenue + annual_display_ad_revenue + annual_video_ad_revenue + annual_native_revenue
)

# Step 4: Displaying the Results
st.header("Revenue Breakdown")
st.metric("Annual Digital Revenue", f"€{annual_total_revenue:,.2f}")
st.metric("Monthly Display Impressions", f"{total_impressions_display:,.0f}")
st.metric("Monthly Video Impressions", f"{total_impressions_video:,.0f}")

# Visualization: Pie Chart
st.header("Revenue Split (Pie Chart)")
fig, ax = plt.subplots()

combined_revenue_data = {
    "Subscriptions": annual_subscription_revenue,
    "Display Ads": annual_display_ad_revenue,
    "Video Ads": annual_video_ad_revenue,
    "Native Articles": annual_native_revenue
}

ax.pie(combined_revenue_data.values(), labels=combined_revenue_data.keys(), autopct='%1.1f%%', startangle=140)
ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
st.pyplot(fig)
