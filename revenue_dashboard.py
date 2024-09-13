import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Constants
INITIAL_SUBSCRIBERS = 20000
INITIAL_ARPU = 4.60
INITIAL_PAGE_VIEWS = 18000000
INITIAL_DISPLAY_IMPRESSIONS = 84000000
INITIAL_VIDEO_IMPRESSIONS = 3500000
DEFAULT_RCPM_DISPLAY = 3.10
DEFAULT_RCPM_VIDEO = 8.10
DEFAULT_NATIVES_PER_MONTH = 2
DEFAULT_AVG_COST_PER_NATIVE = 4000.0

# Page configuration
st.set_page_config(page_title="Enhanced Revenue Projections Dashboard", layout="centered")

# Title
st.title("TOL Revenue Projections")

# Subscribers and Engagement Section
engagement_increase = st.slider("Engagement Rate Increase (%)", min_value=-50, max_value=50, value=0, step=1)
subscribers = st.slider("Subscribers", min_value=1000, max_value=50000, value=INITIAL_SUBSCRIBERS, step=500)
avg_sub_paid = st.number_input("Monthly ARPU (€)", min_value=1.0, max_value=30.0, value=INITIAL_ARPU, step=0.1)

# Display Revenue Section
overall_rcpm_display = st.number_input("Overall rCPM for Display Ads (€)", min_value=0.5, max_value=20.0, value=DEFAULT_RCPM_DISPLAY, step=0.1)

# Native Content Revenue Section
natives_per_month = st.number_input("Number of Native Articles Per Month", min_value=0, value=DEFAULT_NATIVES_PER_MONTH, step=1)
avg_cost_per_native = st.number_input("Average Revenue Per Native Article (€)", min_value=0.0, value=DEFAULT_AVG_COST_PER_NATIVE, step=100.0)

# Video Ad Revenue Section
overall_rcpm_video = st.number_input("Overall rCPM for Video Ads (€)", min_value=0.5, max_value=20.0, value=DEFAULT_RCPM_VIDEO, step=0.1)

# Slider for adjusting video impressions
adjusted_video_impressions = st.slider("Adjusted Video Impressions", min_value=1000000, max_value=10000000, value=INITIAL_VIDEO_IMPRESSIONS, step=50000)

# Display checkboxes in a row
col1, col2, col3, col4 = st.columns(4)
with col1:
    include_subscriptions = st.checkbox("Subs", value=True)
with col2:
    include_display_ads = st.checkbox("Display", value=True)
with col3:
    include_native_content = st.checkbox("Native", value=True)
with col4:
    include_video_content = st.checkbox("Video", value=False)

# Adjust page views, display impressions, and video plays based on subscribers and engagement rate
adjustment_factor = (subscribers / INITIAL_SUBSCRIBERS) * (1 + engagement_increase / 100)
adjusted_page_views = INITIAL_PAGE_VIEWS * adjustment_factor
adjusted_display_impressions = INITIAL_DISPLAY_IMPRESSIONS * adjustment_factor

# Calculations
def calculate_annual_revenue(subscribers, arpu, include_subs, native_count, avg_native_cost, include_native, display_impressions, rcpm_display, include_display, video_impressions, rcpm_video, include_video):
    monthly_subscription_revenue = subscribers * arpu
    annual_subscription_revenue = monthly_subscription_revenue * 12 if include_subs else 0

    monthly_native_revenue = native_count * avg_native_cost
    annual_native_revenue = monthly_native_revenue * 12 if include_native else 0

    annual_display_ad_revenue = (display_impressions / 1000) * rcpm_display if include_display else 0
    annual_video_ad_revenue = (video_impressions / 1000) * rcpm_video if include_video else 0

    total_annual_revenue = annual_subscription_revenue + annual_display_ad_revenue + annual_native_revenue + annual_video_ad_revenue

    return total_annual_revenue, annual_subscription_revenue, annual_native_revenue, annual_display_ad_revenue, annual_video_ad_revenue

# Perform revenue calculations
annual_total_revenue, annual_subscription_revenue, annual_native_revenue, annual_display_ad_revenue, annual_video_ad_revenue = calculate_annual_revenue(
    subscribers, avg_sub_paid, include_subscriptions, natives_per_month, avg_cost_per_native,
    include_native_content, adjusted_display_impressions, overall_rcpm_display,
    include_display_ads, adjusted_video_impressions, overall_rcpm_video, include_video_content
)

# Displaying the Results
st.header("Revenue Breakdown")

# Display the monthly breakdown on the left and yearly totals on the right
col_left, col_right = st.columns(2)
with col_left:
    st.subheader("Monthly Breakdown")
    st.metric("Monthly Subscription Revenue", f"€{annual_subscription_revenue / 12:,.2f}")
    st.metric("Monthly Native Revenue", f"€{annual_native_revenue / 12:,.2f}")
    st.metric("Monthly Display Ad Revenue", f"€{annual_display_ad_revenue / 12:,.2f}")
    st.metric("Monthly Video Ad Revenue", f"€{annual_video_ad_revenue / 12:,.2f}")

with col_right:
    st.subheader("Yearly Totals")
    st.metric("Annual Digital Revenue", f"€{annual_total_revenue:,.2f}")
    st.metric("Annual Display Impressions", f"{adjusted_display_impressions:,.0f}")
    st.metric("Annual Page Views", f"{adjusted_page_views:,.0f}")
    st.metric("Annual Video Plays", f"{adjusted_video_impressions:,.0f}")

# Create the combined revenue data dictionary dynamically
combined_revenue_data = {}
if include_subscriptions:
    combined_revenue_data["Subs"] = annual_subscription_revenue
if include_display_ads:
    combined_revenue_data["Display"] = annual_display_ad_revenue
if include_native_content:
    combined_revenue_data["Native"] = annual_native_revenue
if include_video_content:
    combined_revenue_data["Video"] = annual_video_ad_revenue

# Visualization: Pie Chart with Money Totals
st.header("Revenue Split")
fig, ax = plt.subplots()

# Plot pie chart with money totals
ax.pie(combined_revenue_data.values(), labels=combined_revenue_data.keys(),
       autopct=lambda p: f'€{p * sum(combined_revenue_data.values()) / 100:,.0f}' if p > 0 else '', startangle=140)
ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
st.pyplot(fig)

# Bar chart to show changes relative to starting positions
st.header("Relative Changes to Starting Variables")
relative_changes = {
    'Subscribers': subscribers / INITIAL_SUBSCRIBERS,
    'Display Impressions': adjusted_display_impressions / INITIAL_DISPLAY_IMPRESSIONS,
    'Video Impressions': adjusted_video_impressions / INITIAL_VIDEO_IMPRESSIONS,
    'Page Views': adjusted_page_views / INITIAL_PAGE_VIEWS
}

fig, ax = plt.subplots()
ax.bar(relative_changes.keys(), relative_changes.values())
ax.set_ylabel("Relative Change (Multiple of Initial)")
st.pyplot(fig)
