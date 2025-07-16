import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'etl'))

import fetch_data
import transform

df = fetch_data.fetch_campaign_data()
df = transform.add_metrics(df)

st.set_page_config(page_title="Campaign Dashboard", layout="wide")

st.title("📊 Campaign Performance Dashboard")
st.markdown("""
**Project:** Campaign Performance Dashboard

This interactive dashboard demonstrates how marketing teams can consolidate multi-channel ad campaign data 
(Google Ads, Meta, LinkedIn) into one place.

**Key Metrics:**
- **CTR (Click-Through Rate)** — the percentage of ad impressions that resulted in clicks.
- **CPC (Cost Per Click)** — how much each click costs, on average.
- **CPA (Cost Per Acquisition)** — cost for each conversion (e.g., sign-up, sale).
- **Revenue** — estimated revenue generated per campaign (assumed: £20 per conversion).
- **ROI (Return on Investment)** — calculated as *(Revenue – Spend) / Spend* to show how efficiently spend converts to profit.

Use this dashboard to:
- **View raw campaign data alongside calculated KPIs**
- **Compare average CTR by platform**
- **Spot trends & optimize ad spend**

_All data shown is dummy data for demonstration purposes._
""")


st.subheader("📄 Raw + Calculated Data")
st.dataframe(df)

ctr_df = df.groupby('platform', as_index=False)['ctr'].mean()

fig_ctr = px.bar(
    ctr_df,
    x='platform',
    y='ctr',
    color='platform',
    text_auto='.2f'
)

fig_ctr.update_traces(width=0.4)  

spend_df = df.groupby('platform', as_index=False)['spend'].sum()

fig_pie = px.pie(
    spend_df,
    names='platform',
    values='spend',
    hole=0.3
)

# Show Charts Side by Side with Subheaders in Columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Average CTR (%) by Platform")
    st.plotly_chart(fig_ctr, use_container_width=True)

with col2:
    st.subheader("💰 Total Spend by Platform")
    st.plotly_chart(fig_pie, use_container_width=True)

    # ======== Campaign Performance Metrics ========
st.subheader("🏆 Campaign Performance Comparison")
st.markdown("""
This section shows how each campaign performs overall, helping you identify which campaign delivers 
the **best results for the spend**. 

- **Total Spend (£):** How much was spent on each campaign.
- **Total Conversions:** How many conversions each campaign achieved.
- **Average CTR (%):** The average click-through rate across all dates for the campaign.
- **Average ROI (%):** Shows how effectively each pound spent generated profit.

Use this to compare campaigns and decide where to allocate budget for maximum ROI.
""")

campaign_df = df.groupby('campaign_name').agg({
    'spend': 'sum',
    'impressions': 'sum',
    'clicks': 'sum',
    'conversions': 'sum',
    'ctr': 'mean',
    'roi': 'mean'
}).reset_index()

# Rename columns for clarity
campaign_df = campaign_df.rename(columns={
    'spend': 'Total Spend (£)',
    'impressions': 'Total Impressions',
    'clicks': 'Total Clicks',
    'conversions': 'Total Conversions',
    'ctr': 'Average CTR (%)',
    'roi': 'Average ROI (%)'
})

st.dataframe(campaign_df)

# ======== ROI Bar Chart by Campaign ========
fig_campaign_roi = px.bar(
    campaign_df,
    x='campaign_name',
    y='Average ROI (%)',
    color='campaign_name',
    title='ROI (%) by Campaign',
    text_auto='.2f'
)
fig_campaign_roi.update_traces(width=0.4)

st.plotly_chart(fig_campaign_roi, use_container_width=True)

