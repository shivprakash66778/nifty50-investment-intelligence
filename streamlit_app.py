
import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="NIFTY-50 Investment Intelligence Platform",
    layout="wide"
)

BASE_DIR = "nifty50_outputs"
DATA_DIR = os.path.join(BASE_DIR, "data")
CHART_DIR = os.path.join(BASE_DIR, "charts")

@st.cache_data
def load_data():
    return {
        "model_df": pd.read_csv(os.path.join(DATA_DIR, "final_model_dataset.csv")),
        "profile_results": pd.read_csv(os.path.join(DATA_DIR, "final_profile_results.csv")),
        "risk_summary": pd.read_csv(os.path.join(DATA_DIR, "final_profile_risk_summary.csv")),
        "feature_importance": pd.read_csv(os.path.join(DATA_DIR, "feature_importance.csv")),
        "anomaly_summary": pd.read_csv(os.path.join(DATA_DIR, "anomaly_summary.csv")),
        "conservative": pd.read_csv(os.path.join(DATA_DIR, "conservative_selected_portfolio.csv")),
        "balanced": pd.read_csv(os.path.join(DATA_DIR, "balanced_selected_portfolio.csv")),
        "aggressive": pd.read_csv(os.path.join(DATA_DIR, "aggressive_selected_portfolio.csv"))
    }

data = load_data()
model_df = data["model_df"]
model_df["Date"] = pd.to_datetime(model_df["Date"])

st.title("NIFTY-50 Investment Intelligence Platform")
st.caption("AI-powered stock ranking, portfolio construction, risk analytics, and explainable investment insights.")

page = st.sidebar.radio(
    "Navigate",
    ["Market Overview", "Stock Analyzer", "Portfolio Builder", "Risk Dashboard", "Explainability", "Anomaly Detection"]
)

if page == "Market Overview":
    st.header("Market Overview")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records", f"{len(model_df):,}")
    col2.metric("Stocks", model_df["Symbol"].nunique())
    col3.metric("Industries", model_df["Industry"].nunique())
    col4.metric("Date Range", f"{model_df['Date'].min().date()} to {model_df['Date'].max().date()}")

    for chart in [
        "market_average_close_trend.png",
        "top10_stocks_total_return.png",
        "industry_risk_adjusted_return.png"
    ]:
        path = os.path.join(CHART_DIR, chart)
        if os.path.exists(path):
            st.image(path, use_container_width=True)

elif page == "Stock Analyzer":
    st.header("Stock Analyzer")

    selected_stock = st.selectbox("Select stock", sorted(model_df["Symbol"].unique()))
    stock_data = model_df[model_df["Symbol"] == selected_stock].copy().sort_values("Date")

    st.subheader(f"{selected_stock} — {stock_data['Company Name'].iloc[0]}")
    st.write(f"Industry: **{stock_data['Industry'].iloc[0]}**")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Latest Close", round(stock_data["Close"].iloc[-1], 2))
    col2.metric("Avg 30D Future Return", f"{stock_data['Future_Return_30D'].mean() * 100:.2f}%")
    col3.metric("Avg 20D Volatility", f"{stock_data['Volatility_20D'].mean() * 100:.2f}%")
    col4.metric("Top Quartile Rate", f"{stock_data['Top_Quartile_Outperformer_30D'].mean() * 100:.2f}%")

    st.line_chart(stock_data.set_index("Date")["Close"])
    st.dataframe(stock_data[["Date", "Close", "EMA_12", "EMA_26", "MACD", "RSI_14", "Volatility_20D"]].tail(20), use_container_width=True)

elif page == "Portfolio Builder":
    st.header("Investor Profile Portfolio Builder")

    profile = st.selectbox("Select investor profile", ["Conservative", "Balanced", "Aggressive"])

    if profile == "Conservative":
        portfolio_df = data["conservative"]
    elif profile == "Balanced":
        portfolio_df = data["balanced"]
    else:
        portfolio_df = data["aggressive"]

    portfolio_df["Date"] = pd.to_datetime(portfolio_df["Date"])
    selected_date = st.selectbox("Select recommendation date", sorted(portfolio_df["Date"].dt.date.unique()))
    selected_portfolio = portfolio_df[portfolio_df["Date"].dt.date == selected_date].copy()

    st.subheader(f"{profile} Portfolio Recommendations for {selected_date}")
    display_cols = [
        "Symbol", "Company Name", "Industry", "Allocation", "Future_Return_30D", 
        "Top_Quartile_Outperformer_30D", "Explanation"
    ]
    display_cols = [col for col in display_cols if col in selected_portfolio.columns]
    st.dataframe(selected_portfolio[display_cols], use_container_width=True)

    st.subheader("Portfolio Performance Summary")
    st.dataframe(data["profile_results"], use_container_width=True)

    chart_path = os.path.join(CHART_DIR, "portfolio_average_30d_return_comparison.png")
    if os.path.exists(chart_path):
        st.image(chart_path, use_container_width=True)

elif page == "Risk Dashboard":
    st.header("Risk Dashboard")
    st.dataframe(data["risk_summary"], use_container_width=True)

    chart_path = os.path.join(CHART_DIR, "risk_adjusted_performance_comparison.png")
    if os.path.exists(chart_path):
        st.image(chart_path, use_container_width=True)

    st.info("Balanced Portfolio shows the strongest risk-adjusted performance, while Aggressive Portfolio delivers the highest average return.")

elif page == "Explainability":
    st.header("Explainability")

    st.subheader("Feature Importance")
    st.dataframe(data["feature_importance"].head(25), use_container_width=True)

    chart_path = os.path.join(CHART_DIR, "top20_feature_importance.png")
    if os.path.exists(chart_path):
        st.image(chart_path, use_container_width=True)

    st.subheader("Sample Explainable Recommendations")
    aggressive = data["aggressive"].copy()
    cols = ["Date", "Symbol", "Company Name", "Industry", "Investor_Profile", "Allocation", "Future_Return_30D", "Explanation"]
    cols = [col for col in cols if col in aggressive.columns]
    st.dataframe(aggressive[cols].head(20), use_container_width=True)

elif page == "Anomaly Detection":
    st.header("Market Anomaly Detection")
    st.write("The anomaly module identifies unusual trading volume, volatility spikes, and rolling 60-day extreme drawdowns.")
    st.dataframe(data["anomaly_summary"], use_container_width=True)

    chart_path = os.path.join(CHART_DIR, "market_anomaly_summary.png")
    if os.path.exists(chart_path):
        st.image(chart_path, use_container_width=True)
