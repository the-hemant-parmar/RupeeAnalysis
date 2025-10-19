import streamlit as st
import pandas as pd
import plotly.express as px
from scripts.get_currency_data import get_currency_data
from scripts.metrics import calculate_rupee_strength, calculate_normalized_change


# Streamlit App Configuration
st.set_page_config(
    page_title="Rupee Strength Visualizer",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.title("💹 Rupee Strength Visualizer")
st.markdown(
    """
This dashboard helps you understand the performance of the **Indian Rupee (INR)** 
against major world currencies such as **USD, EUR, GBP, JPY, and CNY**.

Use the filters in the sidebar to select a time range and explore visual trends.
"""
)

# Sidebar Controls
days = st.sidebar.slider(
    "Select Time Range (Days)", min_value=30, max_value=365, value=365, step=30
)

st.sidebar.markdown(
    """
**Interpretation Guide:**
- A **rising** currency line (e.g., USD/INR) → Rupee is **weakening**.
- A **falling** currency line → Rupee is **strengthening**.
"""
)

# Data Loading
with st.spinner("Fetching currency data..."):
    df = get_currency_data(days)

st.success("Data loaded successfully!")


# Metrics
rsm = calculate_rupee_strength(df)
metric_text = "strengthened 💪" if rsm < 0 else "weakened 📉"

st.metric(
    label="Overall Rupee Strength Metric (RSM)",
    value=f"{rsm:.2f}%",
    delta=f"Rupee has {metric_text} on average over the last {days} day",
)

st.caption(
    """
**RSM Explanation:**  
This simple indicator averages the daily percentage changes across INR exchange rates.  
A **negative value** means the rupee has strengthened overall (it buys more foreign currency),  
while a **positive value** indicates weakening.
"""
)

# Charts
st.subheader("📈 Normalized change in INR compared to major currencies")

norm = calculate_normalized_change(df)
try:
    fig = px.line(
        norm,
        x="Date",
        y=norm.columns[1:],  # all except Date
        title="Rupee Performance vs Major Currencies (Base = 100)",
        labels={"value": "Index (Base=100)", "Date": "Date"},
    )
    fig.update_layout(
        yaxis_title="Rupee Value Index", legend_title="Currency", hovermode="x unified"
    )
    fig.add_hline(
        y=100, line_dash="dot", line_color="gray", annotation_text="Base Level"
    )
    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.warning(f"Could not plot Normalized data: {e}")

st.markdown("---")

# Charts
st.subheader("📈 INR Exchange Rate Trends")

cols = [col for col in df.columns if col != "Date"]
try:
    fig = px.line(
        df,
        x="Date",
        y=cols,
        title=f"Values of currencies wrt INR",
    )
    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.warning(f"Could not plot Normalized data: {e}")

for col in df.columns:
    if col != "Date":
        try:
            fig = px.line(
                df,
                x="Date",
                y=col,
                title=f"{col.split('_')[1]} per {col.split('_')[0]}",
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not plot {col}: {e}")

st.markdown("---")
st.markdown(
    """
### 💡 About the Data
Data is sourced from **Yahoo Finance (yfinance)** and cached locally to minimize API usage.  
It updates automatically every 12 hours.  
You can later extend this project with:
- Weighted basket metrics  
- Trade balance correlations  
- Sentiment indicators or volatility analysis
"""
)
