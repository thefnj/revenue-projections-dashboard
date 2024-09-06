import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="Enhanced Revenue Projections Dashboard", layout="centered")

# Title
st.title("TOL Revenue Projections")

# Input components
st.header("Subs & Engagement")

# Subscribers and Engagement
subscribers = st.slider("Subscribers", min_value=1000, max_value=50000, value=20000, step=500)
engagement_increase = st.slider("Engagement Rate Increase (%)", min_value=-50, max_value=50, value=0, step=1)
avg_sub_paid = st.number_input("Monthly ARPU (€)", min_value=1.0, max_value=30.0, value=4.0)

# Ad Revenue Split for Display Ads
st.header("Display Revenue Split")
direct_sold_percentage = st.slider("Percentage of Direct Sold Display Ads", min_value=0, max_value=100, value=20, step=1)
open_market_percentage = 100 - direct_sold_percentage

# Effective CPM Inputs for Display Ads
effective_cpm_direct = st.number_input("Effective CPM for Direct Sold Display Ads (€)", min_value=0.5, max_value=20.0, value=4.0)
effective_cpm_open_market = st.number_input("Effective CPM for Open Marketplace Display Ads (€)", min_value=0.5, max_value=10.0, value=1.0)

# Video Ad Revenue Split
st.header("Video Revenue Split")
video_direct_sold_percentage = st.slider("Percentage of Direct Sold Video Ads", min_value=0, max_value=100, value=20, step=1)
video_open_market_percentage = 100 - video_direct_sold_percentage

# Effective CPM Inputs for Video Ads
effective_cpm_video_direct = st.number_input("Effective CPM for Direct Sold Video Ads (€)", min_value=0.5, max_value=20.0, value=6.0)
effective_cpm_video_open_market = st.number_input("Effective CPM for Open Marketplace Video Ads (€)", min_value=0.5, max_value=10.0, value=2.0)

# Native Content Revenue
st.header("Native Content")
natives_per_month = st.number_input("Number of Native Articles Per Month", min_value=0, value=10)
avg_cost_per_native = st.number_input("Average Revenue Per Native Article (€)", min_value=0.0, value=500.0)

# Calculations
monthly_subscription_revenue = subscribers * avg_sub_paid
annual_subscription_revenue = monthly_subscription_revenue * 12

# Native Content Revenue Calculations
monthly_native_revenue = natives_per_month * avg_cost_per_native
annual_native_revenue = monthly_native_revenue * 12

# Display Ad Impressions Calculations
base_impressions = (subscribers / 10000) * 2.5e6  # Scale with subscribers
additional_impressions = (engagement_increase / 100) * base_impressions  # Extra impressions from engagement
total_impressions = base_impressions + additional_impressions

# Display Ad Revenue Calculations
direct_sold_display_impressions = total_impressions * (direct_sold_percentage / 100)
open_market_display_impressions = total_impressions * (open_market_percentage / 100)

direct_sold_display_revenue = (direct_sold_display_impressions / 1000) * effective_cpm_direct
open_market_display_revenue = (open_market_display_impressions / 1000) * effective_cpm_open_market

monthly_display_ad_revenue = direct_sold_display_revenue + open_market_display_revenue
annual_display_ad_revenue = monthly_display_ad_revenue * 12

# Video Ad Revenue Calculations
direct_sold_video_impressions = total_impressions * (video_direct_sold_percentage / 100)
open_market_video_impressions = total_impressions * (video_open_market_percentage / 100)

direct_sold_video_revenue = (direct_sold_video_impressions / 1000) * effective_cpm_video_direct
open_market_video_revenue = (open_market_video_impressions / 1000) * effective_cpm_video_open_market

monthly_video_ad_revenue = direct_sold_video_revenue + open_market_video_revenue
annual_video_ad_revenue = monthly_video_ad_revenue * 12

# Total Revenue Calculations
annual_total_revenue = annual_subscription_revenue + annual_display_ad_revenue + annual_video_ad_revenue + annual_native_revenue

# Displaying the results
st.header("Revenue Breakdown")
st.metric("Annual Digital Revenue", f"€{annual_total_revenue:,.2f}")

# Visualization: Bar Chart
st.header("Revenue Composition (Bar Chart)")
revenue_data = {
    "Source": ["Subscriptions", "Direct Sold Display Ads", "Open Marketplace Display Ads", "Direct Sold Video Ads", "Open Marketplace Video Ads", "Native Articles"],
    "Revenue": [annual_subscription_revenue, direct_sold_display_revenue * 12, open_market_display_revenue * 12, direct_sold_video_revenue * 12, open_market_video_revenue * 12, annual_native_revenue]
}

st.bar_chart(pd.DataFrame.from_dict(revenue_data).set_index('Source'))

# Visualization: Pie Chart
st.header("Revenue Split (Pie Chart)")
fig, ax = plt.subplots()
ax.pie(revenue_data['Revenue'], labels=revenue_data['Source'], autopct='%1.1f%%', startangle=140)
ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
st.pyplot(fig)
