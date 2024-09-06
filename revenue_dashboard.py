import streamlit as st

# Page configuration
st.set_page_config(page_title="Revenue Projections Dashboard", layout="centered")

# Title
st.title("Digital Media Revenue Projections")

# Input components
st.header("Adjust Revenue Factors")

subscribers = st.slider("Subscribers", min_value=1000, max_value=100000, value=10000, step=500)
avg_sub_paid = st.number_input("Average Monthly Subscription Paid (€)", min_value=1.0, max_value=20.0, value=2.0)
impressions = st.slider("Digital Display Impressions (in thousands)", min_value=100, max_value=10000, value=1000, step=100)
effective_cpm = st.number_input("Effective CPM ($)", min_value=0.5, max_value=50.0, value=5.0)
native_articles = st.number_input("Native Articles Revenue ($)", min_value=0.0, value=5000.0)

# Calculations
subscription_revenue = subscribers * avg_sub_paid
ad_revenue = (impressions * 1000) * (effective_cpm / 1000)
total_revenue = subscription_revenue + ad_revenue + native_articles

# Displaying the results
st.header("Revenue Breakdown")
st.metric("Subscription Revenue", f"${subscription_revenue:,.2f}")
st.metric("Ad Revenue", f"${ad_revenue:,.2f}")
st.metric("Native Articles Revenue", f"${native_articles:,.2f}")
st.metric("Total Revenue", f"${total_revenue:,.2f}")

# Visualization
st.header("Revenue Composition")
revenue_data = {
    "Source": ["Subscriptions", "Digital Ads", "Native Articles"],
    "Revenue": [subscription_revenue, ad_revenue, native_articles]
}

st.bar_chart(data=revenue_data['Revenue'])
