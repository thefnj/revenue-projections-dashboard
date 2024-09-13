import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Initial Values

initial\_values = {
"subscribers": 20000,
"arpu": 4.60,
"page\_views": 18000000,
"display\_impressions": 84000000,
"rcpm\_display": 3.10,
"natives\_per\_month": 2,
"avg\_cost\_per\_native": 4000.0,
"video\_plays": 1800000,
"rcpm\_video": 3.10
}

# Page Configuration

st.set\_page\_config(page\_title="Enhanced Revenue Projections Dashboard", layout="centered")

Title

st.title("TOL Revenue Projections")

# User Inputs

def get\_user\_inputs(initial\_values):
engagement\_increase = st.slider("Engagement Rate Increase (%)", min\_value=-50, max\_value=50, value=0, step=1)
subscribers = st.slider("Subscribers", min\_value=1000, max\_value=50000, value=initial\_values\["subscribers"], step=500)
avg\_sub\_paid = st.number\_input("Monthly ARPU (€)", min\_value=1.0, max\_value=30.0, value=initial\_values\["arpu"], step=0.1)
overall\_rcpm\_display = st.number\_input("Overall rCPM for Display Ads (€)", min\_value=0.5, max\_value=20.0, value=initial\_values\["rcpm\_display"], step=0.1)
natives\_per\_month = st.number\_input("Number of Native Articles Per Month", min\_value=0, value=initial\_values\["natives\_per\_month"], step=1)
avg\_cost\_per\_native = st.number\_input("Average Revenue Per Native Article (€)", min\_value=0.0, value=initial\_values\["avg\_cost\_per\_native"], step=100.0)
overall\_rcpm\_video = st.number\_input("Overall rCPM for Video Ads (€)", min\_value=0.5, max\_value=20.0, value=initial\_values\["rcpm\_video"], step=0.1)

# Checkboxes for Revenue Streams

def get\_revenue\_streams():
col1, col2, col3, col4 = st.columns(4)
with col1:
include\_subscriptions = st.checkbox("Subs", value=True)
with col2:
include\_display\_ads = st.checkbox("Display", value=True)
with col3:
include\_native\_content = st.checkbox("Native", value=True)
with col4:
include\_video\_content = st.checkbox("Video", value=False)

# Revenue Calculations

def calculate\_revenue(initial\_values, engagement\_increase, subscribers, avg\_sub\_paid, overall\_rcpm\_display, natives\_per\_month, avg\_cost\_per\_native, overall\_rcpm\_video, include\_subscriptions, include\_display\_ads, include\_native\_content, include\_video\_content):
\# Adjust page views, display impressions, and video plays based on subscribers and engagement rate
adjusted\_page\_views = initial\_values\["page\_views"] \* (subscribers / initial\_values\["subscribers"]) \* (1 + engagement\_increase / 100)
adjusted\_display\_impressions = initial\_values\["display\_impressions"] \* (subscribers / initial\_values\["subscribers"]) \* (1 + engagement\_increase / 100)
adjusted\_video\_plays = initial\_values\["video\_plays"] \* (subscribers / initial\_values\["subscribers"]) \* (1 + engagement\_increase / 100)

# Display Results

def display\_results(annual\_total\_revenue, adjusted\_display\_impressions, adjusted\_page\_views, adjusted\_video\_plays):
st.header("Revenue Breakdown")
st.metric("Annual Digital Revenue", f"€{annual\_total\_revenue:,.2f}")
st.metric("Annual Display Impressions", f"{adjusted\_display\_impressions:,.0f}")
st.metric("Annual Page Views", f"{adjusted\_page\_views:,.0f}")
st.metric("Annual Video Plays", f"{adjusted\_video\_plays:,.0f}")

# Visualisation: Pie Chart with Money Totals

def display\_pie\_chart(annual\_subscription\_revenue, annual\_display\_ad\_revenue, annual\_native\_revenue, annual\_video\_ad\_revenue, include\_subscriptions, include\_display\_ads, include\_native\_content, include\_video\_content):
st.header("Revenue Split")

# Main function

def main():
engagement\_increase, subscribers, avg\_sub\_paid, overall\_rcpm\_display, natives\_per\_month, avg\_cost\_per\_native, overall\_rcpm\_video = get\_user\_inputs(initial\_values)
include\_subscriptions, include\_display\_ads, include\_native\_content, include\_video\_content = get\_revenue\_streams()

if name == "main":
main()
