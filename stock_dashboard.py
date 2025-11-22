import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import streamlit as st
from datetime import datetime, timedelta

# Page Config
st.set_page_config(
    page_title="Stock Market Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium look
st.markdown("""
<style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
    }
    [data-testid="stMetricValue"] {
        font-size: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("⚙️ Configuration")
ticker = st.sidebar.text_input("Ticker Symbol", "AAPL").upper()

# Date Range Picker
start_date = st.sidebar.date_input("Start Date", datetime.now() - timedelta(days=365))
end_date = st.sidebar.date_input("End Date", datetime.now())

# Technical Indicators Selection
st.sidebar.subheader("Technical Indicators")
indicators = st.sidebar.multiselect(
    "Select Indicators",
    ["SMA 20", "SMA 50", "EMA 20", "Bollinger Bands", "MACD", "RSI"],
    default=["SMA 20"]
)

# Fetch Data
@st.cache_data
def get_data(ticker, start, end):
    try:
        data = yf.download(ticker, start=start, end=end)
        return data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

@st.cache_data
def get_company_info(ticker):
    try:
        info = yf.Ticker(ticker).info
        return info
    except:
        return None

data = get_data(ticker, start_date, end_date)
company_info = get_company_info(ticker)

if data is not None and not data.empty:
    # Main Content
    st.title(f"📈 {ticker} Dashboard")
    
    if company_info:
        st.markdown(f"**{company_info.get('longName', ticker)}** | {company_info.get('sector', 'N/A')} | {company_info.get('industry', 'N/A')}")
        with st.expander("Company Description"):
            st.write(company_info.get('longBusinessSummary', 'No description available.'))

    # Metrics Row
    last_close = data['Close'].iloc[-1]
    prev_close = data['Close'].iloc[-2]
    change = last_close - prev_close
    pct_change = (change / prev_close) * 100
    volume = data['Volume'].iloc[-1]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Price", f"${last_close:.2f}", f"{change:.2f} ({pct_change:.2f}%)")
    col2.metric("Volume", f"{volume:,}")
    col3.metric("High", f"${data['High'].iloc[-1]:.2f}")
    col4.metric("Low", f"${data['Low'].iloc[-1]:.2f}")

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Charts", "🔢 Data", "📋 Financials"])

    with tab1:
        # Calculations
        if "SMA 20" in indicators:
            data['SMA_20'] = data['Close'].rolling(window=20).mean()
        if "SMA 50" in indicators:
            data['SMA_50'] = data['Close'].rolling(window=50).mean()
        if "EMA 20" in indicators:
            data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()
        if "Bollinger Bands" in indicators:
            data['BB_Middle'] = data['Close'].rolling(window=20).mean()
            data['BB_Upper'] = data['BB_Middle'] + 2 * data['Close'].rolling(window=20).std()
            data['BB_Lower'] = data['BB_Middle'] - 2 * data['Close'].rolling(window=20).std()
        if "RSI" in indicators:
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            data['RSI'] = 100 - (100 / (1 + rs))
        if "MACD" in indicators:
            data['MACD_12_26'] = data['Close'].ewm(span=12, adjust=False).mean() - data['Close'].ewm(span=26, adjust=False).mean()
            data['MACD_Signal'] = data['MACD_12_26'].ewm(span=9, adjust=False).mean()

        # Main Chart
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Price'
        ))

        if "SMA 20" in indicators:
            fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], line=dict(color='orange', width=1), name='SMA 20'))
        if "SMA 50" in indicators:
            fig.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], line=dict(color='blue', width=1), name='SMA 50'))
        if "EMA 20" in indicators:
            fig.add_trace(go.Scatter(x=data.index, y=data['EMA_20'], line=dict(color='purple', width=1), name='EMA 20'))
        if "Bollinger Bands" in indicators:
            fig.add_trace(go.Scatter(x=data.index, y=data['BB_Upper'], line=dict(color='gray', width=1, dash='dash'), name='BB Upper'))
            fig.add_trace(go.Scatter(x=data.index, y=data['BB_Lower'], line=dict(color='gray', width=1, dash='dash'), name='BB Lower', fill='tonexty'))

        fig.update_layout(
            title=f"{ticker} Price Chart",
            yaxis_title="Price (USD)",
            xaxis_rangeslider_visible=False,
            height=600,
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Sub-charts for separate indicators
        if "RSI" in indicators:
            st.subheader("Relative Strength Index (RSI)")
            fig_rsi = go.Figure(go.Scatter(x=data.index, y=data['RSI'], line=dict(color='purple')))
            fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
            fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")
            fig_rsi.update_layout(height=200, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_rsi, use_container_width=True)
        
        if "MACD" in indicators:
            st.subheader("MACD")
            fig_macd = go.Figure()
            fig_macd.add_trace(go.Scatter(x=data.index, y=data['MACD_12_26'], name='MACD'))
            fig_macd.add_trace(go.Scatter(x=data.index, y=data['MACD_Signal'], name='Signal'))
            fig_macd.update_layout(height=200, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_macd, use_container_width=True)

    with tab2:
        st.subheader("Raw Data")
        st.dataframe(data.sort_index(ascending=False))

    with tab3:
        st.subheader("Financials (Annual)")
        try:
            financials = yf.Ticker(ticker).financials
            if not financials.empty:
                st.dataframe(financials)
            else:
                st.info("No financial data available.")
        except:
            st.info("Could not fetch financials.")

else:
    st.warning("No data found. Please check the ticker symbol or date range.")
