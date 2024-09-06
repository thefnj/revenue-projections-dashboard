import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="Enhanced Revenue Projections Dashboard", layout="centered")

# Title
st.title("TOL Revenue Projections")

# Input components
st.header("Subs & Engagement")

# Checkbox for Subscription Revenue
include_subscriptions = st.checkbox("Include Subscription Revenue", value=True)

# Subscribers and Engagement
subscribers = st.slider("Subscribers", min_value=1000, max_value=50000, value=12000, step=500)
engagement_increase = st.slider("Engagement Rate Increase (%)", min_value=-50, max_value=50, value=0, step=1)
avg_sub_paid = st.number_input("Monthly ARPU (€)", min_value=1.0, max_value=30.0, value=4.0)

# Checkbox for Display Revenue
st.header("Display Revenue Split")
include_display_ads = st.checkbox("Include Display Ad Revenue", value=True)

# Display Revenue Split Inputs
direct_sold_percentage = st.slider("Percentage of Direct Sold Display Ads", min_value=0, max_value=100, value=20, step=1)
open_market_percentage = 100 - direct_sold_percentage

# Effective CPM Inputs for Display Ads
effective_cpm_direct = st.number_input("Effective CPM for Direct Sold Display Ads (€)", min_value=0.5, max_value=20.0, value=4.0)
effective_cpm_open_market = st.number_input("Effective CPM for Open Marketplace Display Ads (€)", min_value=0.5, max_value=10.0, value=1.0)

# Checkbox for Video Revenue
st.header("Video Revenue Split")
include_video_ads = st.checkbox("Include Video Ad Revenue", value=True)

# Video Revenue Split Inputs
video_direct_sold_percentage = st.slider("Percentage of Direct Sold Video Ads", min_value=0, max_value=100, value=10, step=1)
video_open_market_percentage = 100 - video_direct_sold_percentage

# Effective CPM Inputs for Video Ads
effective_cpm_video_direct = st.number_input("Effective CPM for Direct Sold Video Ads (€)", min_value=0.5, max_value=20.0, value=10.0)
effective_cpm_video_open_market = st.number_input("Effective CPM for Open Marketplace Video Ads (€)", min_value=0.5, max_value=10.0, value=2.0)

# Checkbox for Native Content Revenue
st.header("Native Content")
include_native_content = st.checkbox("Include Native Content Revenue", value=True)

# Native Content Revenue Inputs
natives_per_month = st.number_input("Number of Native Articles Per Month", min_value=0, value=1)
avg_cost_per_native = st.number_input("Average Revenue Per Native Article (€)", min_value=0.0, value=4000.0)

# Calculations
monthly_subscription_revenue = subscribers * avg_sub_paid
annual_subscription_revenue = monthly_subscription_revenue * 12 if include_subscriptions else 0

# Native Content Revenue Calculations
monthly_native_revenue = natives_per_month * avg_cost_per_native
annual_native_revenue = monthly_native_revenue * 12 if include_native_content else 0

# Display Ad Impressions Calculations
base_impressions_display = (subscribers / 10000) * 2.5e6  # Scale with subscribers
additional_impressions_display = (engagement_increase / 100) * base_impressions_display  # Extra impressions from engagement
total_impressions_display = base_impressions_display + additional_impressions_display

# Display Ad Revenue Calculations
direct_sold_display_impressions = total_impressions_display * (direct_sold_percentage / 100)
open_market_display_impressions = total_impressions_display * (open_market_percentage / 100)

direct_sold_display_revenue = (direct_sold_display_impressions / 1000) * effective_cpm_direct
open_market_display_revenue = (open_market_display_impressions / 1000) * effective_cpm_open_market

monthly_display_ad_revenue = direct_sold_display_revenue + open_market_display_revenue
annual_display_ad_revenue = monthly_display_ad_revenue * 12 if include_display_ads else 0

# Video Ad Impressions Calculations (with baseline of 50,000 impressions for 10,000 subscribers)
base_impressions_video = (subscribers / 10000) * 50000  # Scale video impressions with subscribers
additional_impressions_video = (engagement_increase / 100) * base_impressions_video  # Extra impressions from engagement
total_impressions_video = base_impressions_video + additional_impressions_video

# Video Ad Revenue Calculations
direct_sold_video_impressions = total_impressions_video * (video_direct_sold_percentage / 100)
open_market_video_impressions = total_impressions_video * (video_open_market_percentage / 100)

direct_sold_video_revenue = (direct_sold_video_impressions / 1000) * effective_cpm_video_direct
open_market_video_revenue = (open_market_video_impressions / 1000) * effective_cpm_video_open_market

monthly_video_ad_revenue = direct_sold_video_revenue + open_market_video_revenue
annual_video_ad_revenue = monthly_video_ad_revenue * 12 if include_video_ads else 0

# Combined Ad Revenue for Pie Chart
annual_total_display_revenue = direct_sold_display_revenue * 12 + open_market_display_revenue * 12 if include_display_ads else 0
annual_total_video_revenue = direct_sold_video_revenue * 12 + open_market_video_revenue * 12 if include_video_ads else 0

# Total Revenue Calculations
annual_total_revenue = annual_subscription_revenue + annual_total_display_revenue + annual_total_video_revenue + annual_native_revenue

# Displaying the results
st.header("Revenue Breakdown")
st.metric("Annual Digital Revenue", f"€{annual_total_revenue:,.2f}")
st.metric("Total Display Impressions", f"{total_impressions_display:,.0f}")
st.metric("Total Video Impressions", f"{total_impressions_video:,.0f}")

# Visualization: Pie Chart
st.header("Revenue Split (Pie Chart)")
fig, ax = plt.subplots()

# Combine the display and video revenues for the pie chart
combined_revenue_data = {
    "Subscriptions": annual_subscription_revenue,
    "Display Ads": annual_total_display_revenue,
    "Video Ads": annual_total_video_revenue,
    "Native Articles": annual_native_revenue
}

ax.pie(combined_revenue_data.values(), labels=combined_revenue_data.keys(), autopct='%1.1f%%', startangle=140)
ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
st.pyplot(fig)
