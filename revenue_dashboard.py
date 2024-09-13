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
adjusted_video_impressions = INITIAL_VIDEO_IMPRESSIONS * adjustment_factor

# Calculations
def calculate_annual_revenue(subscribers, arpu, include_subs, native_count, avg_native_cost, include_native, display_impressions, rcpm_display, include_display, video_impressions, rcpm_video, include_video):
    monthly_subscription_revenue = subscribers * arpu
    annual_subscription_revenue = monthly_subscription_revenue * 12 if include_subs else 0

    monthly_native_revenue = native_count * avg_native_cost
    annual_native_revenue = monthly_native_revenue * 12 if include_native else 0

    annual_display_ad_revenue = (display_impressions / 1000) * rcpm_display if include_display else 0
    annual_video_ad_revenue = (video_impressions / 1000) * rcpm_video if include_video else 0

    total_annual_revenue = annual_subscription_revenue + annual_display_ad
