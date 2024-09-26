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
subscribers = st.slider("Subscribers", min_value=1000, max_value=100000, value=INITIAL_SUBSCRIBERS, step=500)
avg_sub_paid = st.number_input("Monthly ARPU (€)", min_value=1.0, max_value=30.0, value=INITIAL_ARPU, step=0.1)

# Display Revenue Section
overall_rcpm_display = st.number_input("Overall rCPM for Display Ads (€)", min_value=0.5, max_value=20.0, value=DEFAULT_RCPM_DISPLAY, step=0.1)

# Native Content Revenue Section
natives_per_month = st.number_input("Number of Native Articles Per Month", min_value=0, value=DEFAULT_NATIVES_PER_MONTH, step=1)
avg_cost_per_native = st.number_input("Average Revenue Per Native Article (€)", min_value=0.0, value=DEFAULT_AVG_COST_PER_NATIVE, step=100.0)

# Video Ad Revenue Section
overall_rcpm_video = st.number_input("Overall rCPM for Video Ads (€)", min_value=0.5, max_value=20.0, value=DEFAULT_RCPM_VIDEO, step=0.1)

# Slider for adjusting video impressions percentage
video_impression_change = st.slider("Video Impressions Change (%)", min_value=-50, max_value=100, value=0, step=1)

# Checkbox for other annual revenue
include_other_revenue = st.checkbox("Include Other Annual Revenue", value=False)
other_annual_revenue = st.number_input("Other Annual Revenue (€)", min_value=0, value=0, step=100) if include_other_revenue else 0

# Display checkboxes in a row
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    include_subscriptions = st.checkbox("Subs", value=False)
with col2:
    include_display_ads = st.checkbox("Display", value=True)
with col3:
    include_native_content = st.checkbox("Native", value=True)
with col4:
    include_video_content = st.checkbox("Video", value=False)
with col5:
    include_other_revenue_option = st.checkbox("Other", value=include_other_revenue)

# Adjust page views, display impressions, and video impressions based on subscribers and engagement rate
adjustment_factor = (subscribers / INITIAL_SUBSCRIBERS) * (1 + engagement_increase / 100)
adjusted_page_views = INITIAL_PAGE_VIEWS * adjustment_factor
adjusted_display_impressions = INITIAL_DISPLAY_IMPRESSIONS * adjustment_factor

# Dynamically adjust video impressions with slider
base_video_impressions = INITIAL_VIDEO_IMPRESSIONS * adjustment_factor
adjusted_video_impressions = base_video_impressions * (1 + video_impression_change / 100)

# Calculations
def calculate_annual_revenue(subscribers, arpu, include_subs, native_count, avg_native_cost, include_native, display_impressions, rcpm_display, include_display, video_impressions, rcpm_video, include_video, other_revenue):
    monthly_subscription_revenue = subscribers * arpu
    annual_subscription_revenue = round(monthly_subscription_revenue * 12) if include_subs else 0

    monthly_native_revenue = native_count * avg_native_cost
    annual_native_revenue = round(monthly_native_revenue * 12) if include_native else 0

    annual_display_ad_revenue = round((display_impressions / 1000) * rcpm_display) if include_display else 0
    annual_video_ad_revenue = round((video_impressions / 1000) * rcpm_video) if include_video else 0

    total_annual_revenue = (
        annual_subscription_revenue + 
        annual_display_ad_revenue + 
        annual_native_revenue + 
        annual_video_ad_revenue + 
        (round(other_revenue) if include_other_revenue_option else 0)
    )

    return total_annual_revenue, annual_subscription_revenue, annual_native_revenue, annual_display_ad_revenue, annual_video_ad_revenue, round(other_revenue)

# Perform revenue calculations
annual_total_revenue, annual_subscription_revenue, annual_native_revenue, annual_display_ad_revenue, annual_video_ad_revenue, other_annual_revenue = calculate_annual_revenue(
    subscribers, avg_sub_paid, include_subscriptions, natives_per_month, avg_cost_per_native,
    include_native_content, adjusted_display_impressions, overall_rcpm_display,
    include_display_ads, adjusted_video_impressions, overall_rcpm_video, include_video_content, other_annual_revenue
)

# Displaying the Results
st.header("Revenue Breakdown")

# Display the monthly breakdown on the left and yearly totals on the right
col_left, col_right = st.columns(2)

# Monthly Breakdown
with col_left:
    st.subheader("Monthly")
    if include_subscriptions:
        st.metric("Subs", f"€{round(annual_subscription_revenue / 12):,}")
    if include_native_content:
        st.metric("Native", f"€{round(annual_native_revenue / 12):,}")
    if include_display_ads:
        st.metric("Display", f"€{round(annual_display_ad_revenue / 12):,}")
    if include_video_content:
        st.metric("Video", f"€{round(annual_video_ad_revenue / 12):,}")
    if include_other_revenue_option:
        st.metric("Other Revenue", f"€{round(other_annual_revenue / 12):,}")

    st.markdown(
        f"<div style='background-color:#add8e6; padding: 10px; border-radius: 5px; text-align: left;'>"
        f"<span style='font-size:12px; display:block;'>Total Monthly Revenue</span>"
        f"<span style='font-size:44px; font-weight:bold;'>€{round(annual_total_revenue / 12):,}</span>"
        f"</div>",
        unsafe_allow_html=True
    )

# Yearly Totals
with col_right:
    st.subheader("Annual")
    if include_subscriptions:
        st.metric("Subs", f"€{annual_subscription_revenue:,}")
    if include_native_content:
        st.metric("Native", f"€{annual_native_revenue:,}")
    if include_display_ads:
        st.metric("Display", f"€{annual_display_ad_revenue:,}")
    if include_video_content:
        st.metric("Video", f"€{annual_video_ad_revenue:,}")
    if include_other_revenue_option:
        st.metric("Other Revenue", f"€{other_annual_revenue:,}")

    # Highlighted total at the bottom
    st.markdown(
        f"<div style='background-color:#add8e6; padding: 10px; border-radius: 5px; text-align: left;'>"
        f"<span style='font-size:12px; display:block;'>Total Annual Revenue</span>"
        f"<span style='font-size:44px; font-weight:bold;'>€{round(annual_total_revenue):,}</span>"
        f"</div>",
        unsafe_allow_html=True
    )


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
if include_other_revenue_option:
    combined_revenue_data["Other"] = other_annual_revenue

# Visualization: Pie Chart with Money Totals
st.header("Revenue Split")
if combined_revenue_data:  # Only plot if there's data to show
    fig, ax = plt.subplots()
    ax.pie(combined_revenue_data.values(), labels=combined_revenue_data.keys(),
           autopct=lambda p: f'€{round(p * sum(combined_revenue_data.values()) / 100):,.0f}' if p > 0 else '', startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    st.pyplot(fig)

# # Improved Visualization: Line Chart for Changes Relative to Starting Figures
# st.header("Changes Relative to Starting Values")
# changes = {
#     'Subscribers': subscribers / INITIAL_SUBSCRIBERS - 1 if include_subscriptions else None,
#     'Display Impressions': adjusted_display_impressions / INITIAL_DISPLAY_IMPRESSIONS - 1 if include_display_ads else None,
#     'Video Impressions': adjusted_video_impressions / INITIAL_VIDEO_IMPRESSIONS - 1 if include_video_content else None,
#     'Page Views': adjusted_page_views / INITIAL_PAGE_VIEWS - 1
# }

# fig, ax = plt.subplots()
# # Filter out None values
# filtered_changes = {k: v for k, v in changes.items() if v is not None}
# ax.plot(list(filtered_changes.keys()), [v * 100 for v in filtered_changes.values()], marker='o', linestyle='-')
# ax.axhline(0, color='gray', linewidth=0.8)
# ax.set_ylabel("Percentage Change (%)")
# ax.set_title("Percentage Change from Initial Values")
# st.pyplot(fig)
