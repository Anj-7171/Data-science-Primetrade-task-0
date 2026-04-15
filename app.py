import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Trader Performance vs Market Sentiment", layout="wide")

st.title("Trader Performance vs Market Sentiment")
st.markdown("This dashboard explores how overall trader behaviors and outcomes vary depending on Fear & Greed sentiment.")

# Load Data
@st.cache_data
def load_data():
    if os.path.exists("merged_daily_trader_data.csv"):
        return pd.read_csv("merged_daily_trader_data.csv")
    return None

df = load_data()

if df is None:
    st.error("Data not found. Please run data_processor.py first.")
else:
    # Sidebar Filters
    st.sidebar.header("Filters")
    segments = ["All"] + list(df['frequency_segment'].unique())
    selected_freq = st.sidebar.selectbox("Frequency Segment", segments)

    v_segments = ["All"] + list(df['volume_segment'].unique())
    selected_vol = st.sidebar.selectbox("Volume Segment", v_segments)

    filtered_df = df.copy()
    if selected_freq != "All":
        filtered_df = filtered_df[filtered_df['frequency_segment'] == selected_freq]
    if selected_vol != "All":
        filtered_df = filtered_df[filtered_df['volume_segment'] == selected_vol]

    st.subheader(f"Trader Segmentation: {selected_freq} Frequency | {selected_vol} Volume")
    st.write(f"**Total Records:** {len(filtered_df)}")
    
    # Group by broad sentiment
    def classify_broad(sentiment):
        if 'Fear' in sentiment: return 'Fear'
        elif 'Greed' in sentiment: return 'Greed'
        return 'Neutral'
        
    filtered_df['broad_sentiment'] = filtered_df['sentiment_class'].apply(classify_broad)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Average Daily PnL")
        pnl_agg = filtered_df.groupby('broad_sentiment')['daily_pnl'].mean().reset_index()
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(data=pnl_agg, x='broad_sentiment', y='daily_pnl', palette='coolwarm', ax=ax)
        st.pyplot(fig)

    with col2:
        st.markdown("### Average Win Rate")
        win_agg = filtered_df.groupby('broad_sentiment')['win_rate'].mean().reset_index()
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(data=win_agg, x='broad_sentiment', y='win_rate', palette='viridis', ax=ax)
        st.pyplot(fig)
        
    st.markdown("---")
    st.subheader("Raw Data Preview")
    st.dataframe(filtered_df.head(50))
