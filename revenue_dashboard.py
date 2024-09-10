import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Define your initial values (yearly totals)
initial_subscribers = 20000  # Initial baseline value for subscribers
arpu = 4.60  # Average Revenue Per User in euros
initial_page_views = 18000000  # Baseline total page views per year
initial_display_impressions = 84000000  # Baseline total display ad impressions per year
rcpm_display = 3.10  # Overall rCPM for display ads in euros
natives_per_month = 2  # Starting number of native articles per month
avg_cost_per_native = 4000.0  # Starting average revenue per native article in euros
initial_video_plays = 1800000  # Baseline total video plays per year
rcpm_video = 3.10  # Overall rCPM for video ads in euros

# Page configuration
st.set_page_config(page_title="Enhanced Revenue Projections Dashboard", layout="centered")

# Title
st.title("TOL Revenue Projections")

# Subscribers and Engagement Section
engagement_increase = st.slider("Engagement Rate Increase (%)", min_value=-50, max_value=50, value=0, step=1)
subscribers = st.slider("Subscribers", min_value=1000, max_value=50000, value=initial_subscribers, step=500)
avg_sub_paid = st.number_input("Monthly ARPU (€)", min_value=1.0, max_value=30.0, value=arpu, step=0.1)

# Display Revenue Section
overall_rcpm_display = st.number_input("Overall rCPM for Display Ads (€)", min_value=0.5, max_value=20.0, value=rcpm_display, step=0.1)

# Native Content Revenue Section
natives_per_month = st.number_input("Number of Native Articles Per Month", min_value=0, value=natives_per_month, step=1)
avg_cost_per_native = st.number_input("Average Revenue Per Native Article (€)", min_value=0.0, value=avg_cost_per_native, step=100.0)

# Video Ad Revenue Section
overall_rcpm_video = st.number_input("Overall rCPM for Video Ads (€)", min_value=0.5, max_value=20.0, value=rcpm_video, step=0.1)

# Display checkboxes in a row
col1, col2, col3, col4 = st.columns(4)
with col1:
    include_subscriptions = st.checkbox("Include Subscription Revenue", value=True)
with col2:
    include_display_ads = st.checkbox("Include Display Ad Revenue", value=True)
with col3:
    include_native_content = st.checkbox("Include Native Content Revenue", value=True)
with col4:
    include_video_content = st.checkbox("Include Video Ad Revenue", value=False)

# Adjust page views, display impressions, and video plays based on subscribers and engagement rate
adjusted_page_views = initial_page_views * (subscribers / initial_subscribers) * (1 + engagement_increase / 100)
adjusted_display_impressions = initial_display_impressions * (subscribers / initial_subscribers) * (1 + engagement_increase / 100)
adjusted_video_plays = initial_video_plays * (subscribers / initial_subscribers) * (1 + engagement_increase / 100)

# Calculations
monthly_subscription_revenue = subscribers * avg_sub_paid
annual_subscription_revenue = monthly_subscription_revenue * 12 if include_subscriptions else 0

# Native Content Revenue Calculations
monthly_native_revenue = natives_per_month * avg_cost_per_native
annual_native_revenue = monthly_native_revenue * 12 if include_native_content else 0

# Display Ad Revenue Calculations using overall rCPM
annual_display_ad_revenue = (adjusted_display_impressions / 1000) * overall_rcpm_display if include_display_ads else 0

# Video Ad Revenue Calculations using overall rCPM
annual_video_ad_revenue = (adjusted_video_plays / 1000) * overall_rcpm_video if include_video_content else 0

# Total Revenue Calculations
annual_total_revenue = (
    annual_subscription_revenue + annual_display_ad_revenue + annual_native_revenue + annual_video_ad_revenue
)

# Displaying the Results
st.header("Revenue Breakdown")
st.metric("Annual Digital Revenue", f"€{annual_total_revenue:,.2f}")
st.metric("Annual Display Impressions", f"{adjusted_display_impressions:,.0f}")
st.metric("Annual Page Views", f"{adjusted_page_views:,.0f}")
st.metric("Annual Video Plays", f"{adjusted_video_plays:,.0f}")

# Create the combined revenue data dictionary dynamically
combined_revenue_data = {}
if include_subscriptions:
    combined_revenue_data["Subscriptions"] = annual_subscription_revenue
if include_display_ads:
    combined_revenue_data["Display Ads"] = annual_display_ad_revenue
if include_native_content:
    combined_revenue_data["Native Articles"] = annual_native_revenue
if include_video_content:
    combined_revenue_data["Video Ads"] = annual_video_ad_revenue

# Visualization: Pie Chart with Money Totals
st.header("Revenue Split (Pie Chart)")
fig, ax = plt.subplots()

# Plot pie chart with money totals
ax.pie(combined_revenue_data.values(), labels=combined_revenue_data.keys(),
       autopct=lambda p: f'€{p * sum(combined_revenue_data.values()) / 100:,.0f}' if p > 0 else '', startangle=140)
ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
st.pyplot(fig)
