import streamlit as st
import pandas as pd
from yahooquery import Ticker
from datetime import date

# Set page config
st.set_page_config(page_title="Global Index Tracker", layout="wide")

st.title("🌍 Global Index Tracker")
st.markdown("Select an index to view live data, historical chart, and summary statistics.")

# Define available indices
index_options = {
    "NIFTY 50": "^NSEI",
    "NIFTY BANK": "^NSEBANK",
    "NIFTY IT": "^CNXIT",
    "Sensex (BSE 30)": "^BSESN",
    "S&P 500": "^GSPC",
    "NASDAQ": "^IXIC",
    "Dow Jones": "^DJI",
    "Nikkei 225 (Japan)": "^N225",
    "FTSE 100 (UK)": "^FTSE",
    "DAX (Germany)": "^GDAXI"
}

# Helper function to format numbers
def format_number(val):
    if isinstance(val, (int, float)):
        return f"{val:,}"
    return val

# Sidebar controls
selected_index = st.sidebar.selectbox("Choose an Index", list(index_options.keys()))
start_date = st.sidebar.date_input("Start Date", date(2023, 1, 1))
end_date = st.sidebar.date_input("End Date", date.today())

# Fetch data
symbol = index_options[selected_index]
ticker = Ticker(symbol)
history = ticker.history(start=start_date, end=end_date)

# Display data
if isinstance(history, pd.DataFrame) and not history.empty:
    history = history.reset_index()
    history = history[history["symbol"] == symbol]

    # Display summary details
    info = ticker.summary_detail.get(symbol, {})
    st.subheader(f"🔍 {selected_index} Overview")
    st.markdown(f"""
    - **Current Price**: ₹{info.get('previousClose', 'N/A')}
    - **52-Week High**: ₹{info.get('fiftyTwoWeekHigh', 'N/A')}
    - **52-Week Low**: ₹{info.get('fiftyTwoWeekLow', 'N/A')}
    - **Volume**: {format_number(info.get('volume', 'N/A'))}
    - **Market Cap**: ₹{format_number(info.get('marketCap', 'N/A'))}
    """)

    # Line chart
    st.subheader("📊 Price Chart")
    st.line_chart(history.set_index("date")[["close"]])

    # Show basic stats
    st.subheader("📉 Historical Data Summary")
    st.dataframe(history.describe())
else:
    st.warning("⚠️ Unable to fetch data. Try a different index or check your network.")
