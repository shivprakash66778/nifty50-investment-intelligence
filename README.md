# NIFTY-50 Investment Intelligence Platform

## Project Overview

This project builds an AI-powered investment intelligence platform using historical NIFTY-50 stock market data. The system transforms raw stock price and volume data into actionable investment insights through feature engineering, machine learning-based stock ranking, portfolio construction, risk assessment, explainability, and anomaly detection.

The objective is not only to predict stock prices, but to support data-driven investment decision-making for different investor profiles.

---

## Problem Statement

Financial markets generate large volumes of historical price and trading data. However, raw market data alone does not directly help investors make informed decisions. This project aims to develop an intelligent investment decision-support platform that can:

* Analyze historical stock performance
* Evaluate investment opportunities
* Rank stocks based on expected future behavior
* Construct portfolios for different investor profiles
* Assess portfolio risk
* Explain recommendation logic
* Detect unusual market activity

---

## Dataset

The project uses the NIFTY-50 Stock Market Dataset.

### Dataset Features

The dataset contains historical daily market records including:

* Date
* Stock symbol
* Open price
* High price
* Low price
* Close price
* VWAP
* Volume
* Turnover
* Company metadata
* Industry classification

### Dataset Period

The dataset spans approximately:

```text
January 2000 to April 2021
```

Only the datasets allowed in the problem statement were used. No live market APIs, news data, sentiment data, proprietary financial data, or alternative external datasets were used.

---

## Key Features Implemented

### 1. Exploratory Data Analysis

The notebook includes detailed EDA covering:

* Market average closing price trend
* Top-performing stocks by historical total return
* Bottom-performing stocks by historical total return
* Industry-level risk-adjusted performance
* Market trend behavior
* Sectoral insights
* Volatility and return patterns

---

### 2. Feature Engineering

A wide range of financial, technical, market-relative, and industry-relative features were generated.

#### Return Features

* 1-day return
* 5-day return
* 10-day return
* 20-day return
* 60-day return
* Log return

#### Price Action Features

* High-low range
* Open-close change
* Close vs VWAP

#### Volume Features

* 1-day volume change
* 5-day volume change
* Turnover change

#### Technical Indicators

* Moving averages: MA5, MA10, MA20, MA50, MA100, MA200
* Price vs moving average ratios
* Exponential moving averages: EMA12, EMA26
* MACD
* MACD signal
* MACD histogram
* Bollinger Band width
* Bollinger Band position
* RSI
* Rolling volatility
* Momentum indicators

#### Market and Industry Relative Features

* Return vs market return
* Volatility vs market volatility
* Return vs industry return
* Volatility vs industry volatility
* Cross-sectional return rank
* Cross-sectional volatility rank
* Cross-sectional momentum rank
* Cross-sectional RSI rank

---

## Stock Predictor / Ranker Engine

Instead of focusing only on exact stock price prediction, this project builds a ranking-based investment intelligence model.

The final model ranks stocks based on their expected future 30-day relative performance.

### Targets Created

* `Future_Return_30D`: Future 30-trading-day return
* `Future_Direction_30D`: Whether future return is positive or negative
* `Future_Return_30D_Rank`: Cross-sectional future return rank
* `Top_Quartile_Outperformer_30D`: Whether the stock belongs to the top 25 percent performers
* `Future_Return_Relevance`: Ranking relevance label for LightGBM Ranker

### Model Used

The final predictive engine is a:

```text
LightGBM Ranker
```

The model ranks stocks within each trading date using future return relevance labels.

### Why Ranking Instead of Only Price Prediction?

Stock market price prediction is noisy and unstable. For an investment decision-support system, the more practical question is:

```text
Which stocks are more attractive compared to other available stocks?
```

Therefore, a ranking-based approach is more suitable for portfolio construction than simple up/down classification.

---

## Validation Strategy

A time-based validation methodology was used to prevent data leakage.

```text
Training Period:   2000 to 2017
Validation Period: 2018 to 2019
Test Period:       2020 to 2021
```

The final model was retrained on data from 2000 to 2019 and tested on unseen 2020 to 2021 data.

---

## Portfolio Construction Module

The platform constructs portfolios for three investor profiles.

### Conservative Investor Portfolio

Designed for lower risk and better drawdown control.

Logic:

* Uses model ranker score
* Penalizes high volatility
* Selects Top 10 stocks
* Equal-weight allocation

Allocation:

```text
10 stocks × 10 percent each
```

---

### Balanced Investor Portfolio

Designed for strong risk-adjusted performance.

Logic:

* Combines model confidence with volatility control
* Selects Top 10 stocks
* Equal-weight allocation

Allocation:

```text
10 stocks × 10 percent each
```

---

### Aggressive Investor Portfolio

Designed for maximum return potential.

Logic:

* Uses highest model-ranked stocks
* Selects Top 5 stocks
* Equal-weight allocation

Allocation:

```text
5 stocks × 20 percent each
```

---

## Final Results

Final test period:

```text
2020 to 2021
```

| Portfolio              | Average 30D Return | Annualized Return | Annualized Volatility | Sharpe Ratio | Sortino Ratio | Max Drawdown |
| ---------------------- | -----------------: | ----------------: | --------------------: | -----------: | ------------: | -----------: |
| Market Average         |              3.35% |            40.18% |                41.40% |         0.97 |          0.99 |      -31.57% |
| Conservative Portfolio |              3.67% |            44.00% |                39.51% |         1.11 |          1.27 |      -20.02% |
| Balanced Portfolio     |              5.11% |            61.30% |                45.15% |         1.36 |          1.50 |      -23.27% |
| Aggressive Portfolio   |              6.49% |            77.87% |                63.80% |         1.22 |          1.47 |      -36.86% |

---

## Key Insights

* The Aggressive Portfolio generated the highest average return.
* The Balanced Portfolio achieved the best risk-adjusted performance.
* The Conservative Portfolio reduced maximum drawdown compared with the market average.
* All investor-profile portfolios improved Sharpe ratio over the market benchmark.
* Ranking-based stock selection was more useful than simple direction prediction.
* Market-relative and industry-relative features provided important decision context.

---

## Risk Assessment

The following risk metrics were calculated:

* 30-day volatility
* Annualized volatility
* Sharpe ratio
* Sortino ratio
* Negative return rate
* Non-overlapping 30-day maximum drawdown

Maximum drawdown was calculated using non-overlapping 30-day returns to avoid distortion caused by overlapping forward-return windows.

---

## Explainability

The system includes both model-level and recommendation-level explainability.

### Model-Level Explainability

Feature importance from the LightGBM Ranker was used to identify the strongest model drivers.

Top influential features included:

* Symbol identity
* 60-day volatility
* Close vs MA200
* EMA indicators
* Industry identity
* 20-day volatility
* Return rank
* Industry-relative volatility
* Market-relative volatility
* MACD signals

### Recommendation-Level Explainability

Each stock recommendation is explained using:

* Model ranker score
* Momentum score
* Volatility rank
* RSI behavior
* Industry context
* Investor profile objective

Example explanation:

```text
Selected because it has strong model-ranked return potential, moderate positive momentum, low recent volatility, balanced RSI behavior, and belongs to a relevant industry group.
```

---

## Market Anomaly Detection

The project includes an anomaly detection module that identifies unusual market behavior.

Anomaly types detected:

* Unusual trading volume
* Volatility spikes
* Rolling 60-day extreme drawdowns

### Detected Anomaly Rates

| Anomaly Type                 | Percentage of Data |
| ---------------------------- | -----------------: |
| Unusual Volume               |              5.98% |
| Volatility Spike             |              7.78% |
| Rolling 60D Extreme Drawdown |             13.16% |
| Any Anomaly                  |             23.36% |

---

## Working Prototype

A Streamlit-based dashboard prototype is included to demonstrate the implemented capabilities.

The dashboard includes:

* Market Overview
* Stock Analyzer
* Portfolio Builder
* Risk Dashboard
* Explainability
* Anomaly Detection

---

## Repository Structure

```text
nifty50-investment-intelligence/
│
├── app/
│   └── streamlit_app.py
│
├── charts/
│   ├── market_average_close_trend.png
│   ├── top10_stocks_total_return.png
│   ├── industry_risk_adjusted_return.png
│   ├── portfolio_average_30d_return_comparison.png
│   ├── risk_adjusted_performance_comparison.png
│   ├── top20_feature_importance.png
│   └── market_anomaly_summary.png
│
├── data/
│   └── processed/
│       ├── final_model_dataset.csv
│       ├── final_profile_results.csv
│       ├── final_profile_risk_summary.csv
│       ├── final_test_strategy_results.csv
│       ├── feature_importance.csv
│       ├── anomaly_summary.csv
│       ├── conservative_selected_portfolio.csv
│       ├── balanced_selected_portfolio.csv
│       └── aggressive_selected_portfolio.csv
│
├── models/
│   ├── final_lgbm_ranker_model.pkl
│   ├── symbol_encoder.pkl
│   └── industry_encoder.pkl
│
├── notebooks/
│   └── NIFTY50_Investment_Intelligence_Final_Notebook.ipynb
│
├── reports/
│
├── requirements.txt
└── README.md
```
## Environment Setup

Clone the repository:

```bash
git clone <your-repository-url>
cd nifty50-investment-intelligence
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

For Windows:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

---

## Dependency Installation

Install all required Python libraries using:

```bash
pip install -r requirements.txt
```

The main dependencies are:

```text
pandas
numpy
scikit-learn
lightgbm
matplotlib
seaborn
streamlit
joblib
```

---

## Running the Application

The project includes a Streamlit-based working prototype.

Run the application using:

```bash
streamlit run app/streamlit_app.py
```

After running the command, the application will open locally at:

```text
http://localhost:8501
```

The dashboard includes:

* Market Overview
* Stock Analyzer
* Portfolio Builder
* Risk Dashboard
* Explainability
* Anomaly Detection

---

## Reproducing Results

To reproduce the full analysis and model results:

1. Download the NIFTY-50 stock market dataset.
2. Place the raw dataset files in the expected data directory.
3. Open the final notebook:

```text
notebooks/NIFTY50_Investment_Intelligence_Final_Notebook.ipynb
```

4. Run all notebook cells sequentially.
5. The notebook will generate:

   * Processed feature dataset
   * Trained LightGBM Ranker model
   * Portfolio recommendation outputs
   * Risk assessment tables
   * Feature importance results
   * Anomaly detection results
   * EDA and result charts
   * Streamlit prototype app file

The repository already includes processed outputs and trained model files, so the Streamlit app can also be run directly without retraining the model.

---

## Environment Setup

Clone the repository:

```bash
git clone <your-repository-url>
cd nifty50-investment-intelligence
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment.

For Windows:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Run the Streamlit app:

```bash
streamlit run app/streamlit_app.py
```

The application will open locally at:

```text
http://localhost:8501
```

---

## Reproducing Results

To reproduce the complete project:

1. Download the NIFTY-50 dataset.
2. Place the raw files in the expected data directory.
3. Run the final notebook:

   ```text
   notebooks/NIFTY50_Investment_Intelligence_Final_Notebook.ipynb
   ```
4. Generate processed datasets, models, charts, and portfolio outputs.
5. Run the Streamlit dashboard.

The repository also contains processed outputs and trained model files to run the dashboard directly.

---

## Main Files

| File                                                             | Purpose                                            |
| ---------------------------------------------------------------- | -------------------------------------------------- |
| `notebooks/NIFTY50_Investment_Intelligence_Final_Notebook.ipynb` | Complete end-to-end analysis and modeling notebook |
| `app/streamlit_app.py`                                           | Working Streamlit prototype                        |
| `models/final_lgbm_ranker_model.pkl`                             | Final trained LightGBM Ranker                      |
| `data/processed/final_profile_risk_summary.csv`                  | Final portfolio risk metrics                       |
| `data/processed/final_profile_results.csv`                       | Final portfolio performance results                |
| `data/processed/feature_importance.csv`                          | Model explainability output                        |
| `data/processed/anomaly_summary.csv`                             | Market anomaly detection summary                   |

---

## Limitations

* The system uses historical market data only.
* No live market data was used.
* News, sentiment, macroeconomic indicators, and financial statement data were not included due to problem constraints.
* Stock market forecasting is uncertain and results should not be interpreted as financial advice.
* Historical outperformance does not guarantee future returns.
* Some old or renamed symbols appear separately due to historical symbol changes in the dataset.

---

## Future Improvements

Possible future improvements include:

* Adding a full portfolio optimization algorithm
* Using non-overlapping walk-forward backtesting
* Building a more advanced risk-parity portfolio
* Adding sector diversification constraints
* Deploying the dashboard using Streamlit Cloud
* Adding user-defined investment horizon and risk tolerance
* Incorporating transaction costs and rebalancing frequency

---

## Disclaimer

This project is built for educational and analytical purposes only. It is not financial advice. Investment decisions should be made after independent research and professional consultation.

---

## Conclusion

This project demonstrates a complete investment intelligence pipeline for NIFTY-50 stocks. It combines machine learning, technical analysis, portfolio construction, risk assessment, explainability, anomaly detection, and a Streamlit prototype into a practical decision-support platform.
