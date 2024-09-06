import streamlit as st

# Page configuration
st.set_page_config(page_title="Enhanced Revenue Projections Dashboard", layout="centered")

# Title
st.title("TOL Revenue Projections")

# Input components
st.header("Adjust Revenue Factors")

# Subscribers and Engagement
subscribers = st.slider("Subscribers", min_value=1000, max_value=50000, value=20000, step=500)
engagement_increase = st.slider("Engagement Rate Increase (%)", min_value=-50, max_value=50, value=0, step=1)
avg_sub_paid = st.number_input("Average Monthly Subscription Paid (€)", min_value=1.0, max_value=100.0, value=10.0)


# Ad Revenue Split
st.header("Ad Revenue Split")
direct_sold_percentage = st.slider("Percentage of Direct Sold Ads", min_value=0, max_value=100, value=20, step=1)
open_market_percentage = 100 - direct_sold_percentage

# Effective CPM Inputs
effective_cpm_direct = st.number_input("Effective CPM for Direct Sold Ads (€)", min_value=0.5, max_value=20.0, value=4.0)
effective_cpm_open_market = st.number_input("Effective CPM for Open Marketplace Ads (€)", min_value=0.5, max_value=10.0, value=1.0)

# Native Revenue
native_articles = st.number_input("Native Articles Revenue (€)", min_value=0.0, value=5000.0)

# Calculations
subscription_revenue = subscribers * avg_sub_paid

# Ad Impressions Calculations
base_impressions = (subscribers / 10000) * 2.5e6  # Scale with subscribers
additional_impressions = (engagement_increase / 100) * base_impressions  # Extra impressions from engagement
total_impressions = base_impressions + additional_impressions

# Ad Revenue Calculations
direct_sold_impressions = total_impressions * (direct_sold_percentage / 100)
open_market_impressions = total_impressions * (open_market_percentage / 100)

direct_sold_revenue = (direct_sold_impressions / 1000) * effective_cpm_direct
open_market_revenue = (open_market_impressions / 1000) * effective_cpm_open_market

ad_revenue = direct_sold_revenue + open_market_revenue
total_revenue = subscription_revenue + ad_revenue + native_articles

# Displaying the results
st.header("Revenue Breakdown")
st.metric("Subscription Revenue", f"€{subscription_revenue:,.2f}")
st.metric("Ad Revenue (Direct Sold)", f"€{direct_sold_revenue:,.2f}")
st.metric("Ad Revenue (Open Marketplace)", f"€{open_market_revenue:,.2f}")
st.metric("Total Ad Revenue", f"€{ad_revenue:,.2f}")
st.metric("Native Articles Revenue", f"€{native_articles:,.2f}")
st.metric("Total Revenue", f"€{total_revenue:,.2f}")

# Visualization
st.header("Revenue Composition")
revenue_data = {
    "Source": ["Subscriptions", "Direct Sold Ads", "Open Marketplace Ads", "Native Articles"],
    "Revenue": [subscription_revenue, direct_sold_revenue, open_market_revenue, native_articles]
}

st.bar_chart(data=revenue_data['Revenue'])
