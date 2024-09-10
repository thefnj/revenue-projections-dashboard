import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Define your values at the start of the code
subscribers = 20000  # Initial value for subscribers
arpu = 4.67  # Average Revenue Per User in euros
page_views = 1500000  # Monthly page views
display_impressions = 7000000  # Monthly display ad impressions
rcpm_display = 3.10  # Overall rCPM for display ads in euros
display_revenue = 22500  # Display revenue in euros
natives_per_month = 1  # Number of native articles per month
avg_cost_per_native = 4000.0  # Average revenue per native article in euros

# Page configuration
st.set_page_config(page_title="Enhanced Revenue Projections Dashboard", layout="centered")

# Title
st.title("TOL Revenue Projections")

# Step 2: Input Components in Collapsible Sections

# Subs & Engagement Section
with st.expander("Subs & Engagement", expanded=False):
    # Checkbox for Subscription Revenue
    include_subscriptions = st.checkbox("Include Subscription Revenue", value=True)

    # Subscribers and Engagement (using predefined data)
    subscribers = st.slider("Subscribers", min_value=1000, max_value=50000, value=subscribers, step=500)
    engagement_increase = st.slider("Engagement Rate Increase (%)", min_value=-50, max_value=50, value=0, step=1)
    avg_sub_paid = st.number_input("Monthly ARPU (€)", min_value=1.0, max_value=30.0, value=arpu)

# Display Revenue Section
with st.expander("Display Revenue", expanded=False):
    include_display_ads = st.checkbox("Include Display Ad Revenue", value=True)

    # Overall rCPM for Display Ads from predefined data or as an input
    overall_rcpm_display = st.number_input("Overall rCPM for Display Ads (€)", min_value=0.5, max_value=20.0, value=rcpm_display)

# Native Content Section
with st.expander("Native Content", expanded=False):
    include_native_content = st.checkbox("Include Native Content Revenue", value=True)

    # Native Content Revenue Inputs
    natives_per_month = st.number_input("Number of Native Articles Per Month", min_value=0, value=natives_per_month)
    avg_cost_per_native = st.number_input("Average Revenue Per Native Article (€)", min_value=0.0, value=avg_cost_per_native)

# Step 3: Calculations

# Subscription Revenue
monthly_subscription_revenue = subscribers * avg_sub_paid
annual_subscription_revenue = monthly_subscription_revenue * 12 if include_subscriptions else 0

# Native Content Revenue Calculations
monthly_native_revenue = natives_per_month * avg_cost_per_native
annual_native_revenue = monthly_native_revenue * 12 if include_native_content else 0

# Display Ad Revenue Calculations using overall rCPM
base_impressions_display = (subscribers / 12000) * display_impressions  # Scale with subscribers
additional_impressions_display = (engagement_increase / 100) * base_impressions_display
total_impressions_display = base_impressions_display + additional_impressions_display

# Use overall rCPM for Display Ads
monthly_display_ad_revenue = (total_impressions_display / 1000) * overall_rcpm_display
annual_display_ad_revenue = monthly_display_ad_revenue * 12 if include_display_ads else 0

# Total Revenue Calculations
annual_total_revenue = (
    annual_subscription_revenue + annual_display_ad_revenue + annual_native_revenue
)

# Step 4: Displaying the Results
st.header("Revenue Breakdown")
st.metric("Annual Digital Revenue", f"€{annual_total_revenue:,.2f}")
st.metric("Monthly Display Impressions", f"{total_impressions_display:,.0f}")

# Visualization: Pie Chart
st.header("Revenue Split (Pie Chart)")
fig, ax = plt.subplots()

combined_revenue_data = {
    "Subscriptions": annual_subscription_revenue,
    "Display Ads": annual_display_ad_revenue,
    "Native Articles": annual_native_revenue
}

ax.pie(combined_revenue_data.values(), labels=combined_revenue_data.keys(), autopct='%1.1f%%', startangle=140)
ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
st.pyplot(fig)
