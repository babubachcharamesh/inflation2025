import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_data():
    """Loads and cleans the inflation data."""
    file_path = "inflation_rates.xlsx"
    if not os.path.exists(file_path):
        st.error(f"Data file '{file_path}' not found. Please ensure it is in the repository root.")
        return pd.DataFrame()
        
    try:
        df = pd.read_excel(file_path)
        
        # Standardize column names for easier access
        # Based on peek: ['Rank', 'Country', 'Continent', 'Inflation rate percentage 2025']
        df.columns = [
            'Rank', 
            'Country', 
            'Continent', 
            'Rate'
        ]
        
        # Ensure Rate is numeric
        df['Rate'] = pd.to_numeric(df['Rate'], errors='coerce')
        df = df.dropna(subset=['Rate']).reset_index(drop=True)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def get_continent_stats(df):
    """Calculates statistics by continent."""
    if df.empty:
        return pd.DataFrame()
    stats = df.groupby('Continent')['Rate'].agg(['mean', 'max', 'min', 'count']).reset_index()
    stats.columns = ['Continent', 'Average', 'Highest', 'Lowest', 'Country Count']
    return stats

def get_top_n(df, n=10, ascending=False):
    """Returns top N countries by inflation rate."""
    if df.empty:
        return pd.DataFrame()
    return df.sort_values(by='Rate', ascending=ascending).head(n)
