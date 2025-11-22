📈 Stock Market Data Dashboard

An interactive Streamlit-based web dashboard that fetches real-time stock market data using the yfinance API and visualizes it with Plotly.
This project demonstrates integration of APIs, data analysis, and front-end visualization — perfect for portfolios and data analyst / Python developer resumes.

🧠 Project Overview

This dashboard allows users to:
 Fetch live market data of any listed stock (e.g., AAPL, TSLA, MSFT, INFY.NS).
 Calculate and visualize technical indicators such as:
  20-day and 50-day Simple Moving Averages (SMA)
  Relative Strength Index (RSI)
 Interactively explore data with a clean UI built using Streamlit and Plotly.
 Display charts with dark mode visualization for a modern analytics look.

 ⚙️ Technologies Used
 
 | Tool / Library          | Purpose                                                        |
| ----------------------- | -------------------------------------------------------------- |
| **Python**              | Core programming language                                      |
| **Streamlit**           | Front-end interactive dashboard framework                      |
| **Plotly**              | Interactive charting library for candlestick and RSI charts    |
| **yfinance**            | Yahoo Finance API wrapper for fetching live market data        |
| **pandas**              | Data manipulation and rolling window calculations              |
| **ngrok / localtunnel** | For creating public URLs when running on Colab (testing phase) |

🧩 Features

✅ Fetch real-time stock prices from Yahoo Finance
✅ Calculate 20-day & 50-day Moving Averages (SMA)
✅ Compute Relative Strength Index (RSI) using price momentum
✅ Display interactive candlestick charts and RSI graphs
✅ Dark-themed Streamlit interface
✅ Works in Google Colab (using ngrok/localtunnel) or locally on VS Code
✅ Ready for deployment on Streamlit Cloud

📸 Project Preview

🔹 Dashboard Interface
🔹 RSI Chart Example

🧠 How It Works
1️⃣ Fetching Data

We use the yfinance API:
```
data = yf.download(ticker, period=period, interval=interval)
```
This retrieves Open, High, Low, Close, and Volume data directly from Yahoo Finance.

2️⃣ Calculating Indicators

We calculate 20-day and 50-day SMAs and RSI:
```
data['SMA_20'] = data['Close'].rolling(window=20).mean()
data['SMA_50'] = data['Close'].rolling(window=50).mean()

def compute_rsi(df, window=14):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
```
3️⃣ Visualization with Plotly

Interactive candlestick charts:
```
fig = go.Figure()
fig.add_trace(go.Candlestick(x=data.index, open=data['Open'],
                             high=data['High'], low=data['Low'],
                             close=data['Close'], name='Candlestick'))
fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], name='SMA 20'))
fig.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], name='SMA 50'))
```
4️⃣ Streamlit Dashboard Layout
```
st.title("📊 Stock Market Data Dashboard")
st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, TSLA, INFY.NS)")
st.plotly_chart(fig)
st.line_chart(data['RSI'])
```
🧪 Setup & Installation
🖥️ Run Locally (Recommended)
```
git clone https://github.com/<your-username>/stock-market-dashboard.git
cd stock-market-dashboard
pip install -r requirements.txt
streamlit run stock_dashboard.py
```
Then open 👉 http://localhost:8501

💻 Run on Google Colab (for testing)

1.Upload stock_dashboard.py to Colab.
2.Run:
```
!pip install streamlit yfinance plotly pandas pyngrok -q
from pyngrok import ngrok
import threading, subprocess, time

def run_streamlit():
    subprocess.call(["streamlit", "run", "stock_dashboard.py", "--server.port", "8501"])
threading.Thread(target=run_streamlit).start()

time.sleep(10)
public_url = ngrok.connect(8501)
print("Public URL:", public_url)
```
3.Click the generated public URL to open your Streamlit app.

🖥️ Dasboard image

<img width="1907" height="826" alt="image2" src="https://github.com/user-attachments/assets/0f3dbcc9-bfd9-4c01-b3d9-1afb7b470e83" />
<img width="1902" height="848" alt="image" src="https://github.com/user-attachments/assets/d5659b31-8ee2-4dc7-8586-8ef77fceb07b" />


📦 requirements.txt
```
streamlit
yfinance
pandas
plotly
```
🚀 Future Enhancements

Add Volume and MACD indicators
Integrate news sentiment analysis
Add portfolio tracker and alerts system
Deploy on Streamlit Cloud for public portfolio access
