import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data, get_continent_stats, get_top_n

# Page Configuration
st.set_page_config(
    page_title="Global Inflation Pulse 2025",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Premium Design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

    :root {
        --glass-bg: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.1);
        --accent-glow: 0 0 20px rgba(0, 242, 255, 0.3);
    }

    * {
        font-family: 'Outfit', sans-serif !important;
    }

    .stApp {
        background: radial-gradient(circle at top right, #1a1a2e, #16213e, #0f3460);
        color: #e9ecef;
    }

    /* Glassmorphism containers */
    div.stMetric, .stApp [data-testid="stVerticalBlock"] > div:has(div.stMetric) {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    div.stMetric:hover {
        transform: translateY(-5px);
        box-shadow: var(--accent-glow);
    }

    /* Custom Header */
    .main-header {
        text-align: center;
        padding: 60px 0;
        background: linear-gradient(90deg, #00f2ff, #0061ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4rem;
        font-weight: 800;
        letter-spacing: -2px;
        margin-bottom: 10px;
    }

    .sub-header {
        text-align: center;
        color: #8892b0;
        font-size: 1.2rem;
        margin-bottom: 50px;
        font-weight: 300;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background-color: transparent;
        justify-content: center;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: var(--glass-bg);
        border-radius: 10px 10px 0px 0px;
        color: #8892b0;
        padding: 0 30px;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(0, 242, 255, 0.1) !important;
        color: #00f2ff !important;
        border-bottom: 2px solid #00f2ff !important;
    }

    /* Impact Cards */
    .impact-card {
        background: var(--glass-bg);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid var(--glass-border);
        margin-bottom: 20px;
    }

    </style>
    """, unsafe_allow_html=True)

# App Title & Header
st.markdown('<h1 class="main-header">Global Inflation Pulse</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Advanced Economic Insights & Forecasting for 2025</p>', unsafe_allow_html=True)

# Load Data
df = load_data()

if not df.empty:
    # Top Metrics
    m1, m2, m3, m4 = st.columns(4)
    avg_inflation = df['Rate'].mean()
    highest_country = df.loc[df['Rate'].idxmax()]
    lowest_country = df.loc[df['Rate'].idxmin()]
    
    m1.metric("World Average", f"{avg_inflation:.2f}%")
    m2.metric("Highest Rate", f"{highest_country['Rate']}%", highest_country['Country'])
    m3.metric("Lowest Rate", f"{lowest_country['Rate']}%", lowest_country['Country'])
    m4.metric("Total Countries", len(df))

    # Sidebar Filters (Hidden initially but useful)
    with st.sidebar:
        st.title("Filters")
        continent_filter = st.multiselect("Select Continents", options=df['Continent'].unique(), default=df['Continent'].unique())
        rate_range = st.slider("Inflation Range (%)", float(df['Rate'].min()), float(df['Rate'].max()), (float(df['Rate'].min()), float(df['Rate'].max())))

    filtered_df = df[(df['Continent'].isin(continent_filter)) & (df['Rate'].between(rate_range[0], rate_range[1]))]

    # Main Dashboard Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🌎 Global Map", "📊 Regional Analytics", "📉 Rankings", "🧮 Impact Calculator"])

    with tab1:
        st.markdown("### 🌎 Interactive Global Heatmap")
        fig = px.choropleth(
            filtered_df,
            locations="Country",
            locationmode='country names',
            color="Rate",
            hover_name="Country",
            color_continuous_scale=px.colors.sequential.Viridis,
            labels={'Rate':'Inflation %'},
            template="plotly_dark",
            height=600
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular',
                bgcolor='rgba(0,0,0,0)'
            ),
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("### 📊 Distribution by Continent")
        col_left, col_right = st.columns(2)
        
        with col_left:
            cont_stats = get_continent_stats(filtered_df)
            fig_bar = px.bar(
                cont_stats, 
                x='Continent', 
                y='Average', 
                color='Average',
                text_auto='.2s',
                template="plotly_dark",
                color_continuous_scale='Bluered'
            )
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with col_right:
            # Radar Chart for Continent Comparison
            cont_stats = get_continent_stats(filtered_df)
            fig_radar = go.Figure()
            
            fig_radar.add_trace(go.Scatterpolar(
                r=cont_stats['Average'],
                theta=cont_stats['Continent'],
                fill='toself',
                name='Average Inflation'
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, cont_stats['Highest'].max()]),
                    bgcolor='rgba(0,0,0,0)'
                ),
                showlegend=False,
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                title="Regional Economic Signature (Radar)"
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        # Engine Insights at the bottom of Regional Analytics
        st.markdown("### 🤖 Engine Insights")
        avg_v = filtered_df['Rate'].mean()
        high_c = filtered_df.loc[filtered_df['Rate'].idxmax()]
        
        insight_col1, insight_col2 = st.columns(2)
        with insight_col1:
            st.markdown(f"""
            <div class="impact-card">
                <h4>Global Climate</h4>
                <p>The average inflation across selected regions is <b>{avg_v:.2f}%</b>. 
                Focusing on <b>{high_c['Country']}</b>, which leads with <b>{high_c['Rate']}%</b>, 
                signals extreme economic pressure in the {high_c['Continent']} region.</p>
            </div>
            """, unsafe_allow_html=True)
        with insight_col2:
            st.markdown(f"""
            <div class="impact-card">
                <h4>Economic Forecast</h4>
                <p>Based on current trends, nations with inflation below 2% are positioned 
                for high capital preservation. Conversely, high-rate zones may experience 
                significant currency devaluation in fiscal year 2025.</p>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.markdown("### 📉 Ranking Extremes")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top 10 High Inflation")
            top_10 = get_top_n(filtered_df, 10)
            fig_top = px.bar(top_10, x='Rate', y='Country', orientation='h', color='Rate', color_continuous_scale='Reds')
            fig_top.update_layout(yaxis={'categoryorder':'total ascending'}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_top, use_container_width=True)
            
        with col2:
            st.subheader("Top 10 Stable Economies")
            bottom_10 = get_top_n(filtered_df, 10, ascending=True)
            fig_bot = px.bar(bottom_10, x='Rate', y='Country', orientation='h', color='Rate', color_continuous_scale='Blues')
            fig_bot.update_layout(yaxis={'categoryorder':'total descending'}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_bot, use_container_width=True)

    with tab4:
        st.markdown("### 🧮 Purchasing Power Calculator")
        st.info("Calculate how inflation in different countries affects your money's value in 2025.")
        
        calc_col1, calc_col2 = st.columns(2)
        
        with calc_col1:
            amount = st.number_input("Enter Amount ($)", value=1000, step=100)
            country_select = st.selectbox("Select Country", options=df['Country'].unique())
            
        country_rate = df[df['Country'] == country_select]['Rate'].values[0]
        loss = amount * (country_rate / 100)
        final_val = amount - loss
        
        with calc_col2:
            st.markdown(f"""
            <div class="impact-card">
                <h3>Impact Analysis for {country_select}</h3>
                <p>Inflation Rate: <b>{country_rate}%</b></p>
                <hr>
                <p>Purchasing Power Loss: <span style="color: #ff4b4b;">-${loss:.2f}</span></p>
                <p>Effective Value: <span style="color: #00f2ff; font-size: 1.5rem;">${final_val:.2f}</span></p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### Comparison with Global Average")
        avg_loss = amount * (avg_inflation / 100)
        diff = loss - avg_loss
        
        if diff > 0:
            st.warning(f"Investing in **{country_select}** loses ${abs(diff):.2f} more value than the global average.")
        else:
            st.success(f"**{country_select}** is overperforming the global average by preserving ${abs(diff):.2f} more value.")

else:
    st.error("Could not load data. Please check the Excel file.")

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #8892b0; font-size: 0.8rem;">'
    'Created with ❤️ by Antigravity Digital | Data Source: Global Economic Outlook 2025'
    '</p>', 
    unsafe_allow_html=True
)
