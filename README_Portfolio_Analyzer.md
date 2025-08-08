# 💼 Portfolio Health Analyzer · Streamlit App

An all-in-one interactive tool that helps you understand, improve, and simulate your stock portfolio using real-time market data, risk metrics, and financial logic.

---

## 📘 What Is This Project About?

**Portfolio Health Analyzer** is a web app built with [Streamlit](https://streamlit.io/) that empowers investors and learners to:

- Track portfolio performance with **real-time stock prices**
- Identify **risks and weaknesses** in allocation, sector exposure, and volatility
- Explore **what-if scenarios** by simulating new stock purchases or sales
- Forecast **profit or loss** based on expected market changes
- Get **smart suggestions** to improve diversification and risk-adjusted return

It’s perfect for:
- Beginners learning about investing
- DIY investors managing their portfolios
- Educators explaining portfolio concepts
- Developers building financial tools

---

## 🚀 Try It Online

Click here to launch the app on Streamlit Cloud:

🔗 [https://portfolio-health-analyzer-yourusername.streamlit.app](https://portfolio-health-analyzer-yourusername.streamlit.app)

> ⚠️ Replace `yourusername` with your actual Streamlit app subdomain.

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 📁 **Upload CSV** | Upload a simple portfolio file with tickers and shares |
| 📊 **Visualize Allocation** | Pie chart of value allocation by stock |
| 📋 **Portfolio Table** | Live prices, shares, market value, sector |
| 📈 **Rebalancing Tool** | Suggests trades to match your target weights |
| 📉 **Risk Metrics** | Volatility, Sharpe ratio, and correlation heatmap |
| 🧠 **Improvement Engine** | Recommends stocks to add/remove for better diversification |
| 🧪 **Scenario Simulation** | Try adding/removing stocks and recalculate instantly |
| 🔄 **Reset Simulation** | Return to original uploaded portfolio |
| 💹 **Profit/Loss Forecaster** | Type tickers + % change to estimate total gain/loss |
| 📥 **Download Report** | Export forecast data to CSV |
| 📈 **P&L Bar Chart** | See predicted gains/losses visually by ticker |

---

## 📁 Upload Format (CSV)

Use a basic `.csv` file with this format:

```csv
Ticker,Shares
AAPL,10
MSFT,8
TSLA,5
```

- Header must be `Ticker,Shares`
- Stock symbols must be valid U.S. tickers

---

## 🧪 Forecast Without Upload (Optional)

You can test predictions without a file by entering:

```
AAPL:10, MSFT:-5:20, TSLA:15
```

- Format: `TICKER:CHANGE[:SHARES]`
  - `AAPL:10` → +10% with default 10 shares
  - `MSFT:-5:20` → –5% change with 20 shares
- App will estimate portfolio value change, per-stock gain/loss, and chart

---

## 🧠 How Risk & Suggestions Work

- **Volatility (σ)**: Higher = riskier stock
- **Sharpe Ratio**: Measures return per unit risk (compared to 2% risk-free rate)
- **Correlation Matrix**: Shows how similarly your stocks behave
- **Improvement Suggestions**:
  - Flag over-correlated or high-volatility holdings
  - Detect missing sectors
  - Recommend ETFs or uncorrelated stocks

---

## 📚 Tech Stack

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly](https://plotly.com/)
- [yfinance](https://pypi.org/project/yfinance/)
- Python 3.9+

---

## 🛠️ Run Locally

Clone this repo and run:

```bash
git clone https://github.com/yourusername/portfolio-health-analyzer.git
cd portfolio-health-analyzer
pip install -r requirements.txt
streamlit run app.py
```

---

## 🧪 Example Use Cases

✅ Visualize where your money is concentrated  
✅ Simulate adding TSLA and removing NVDA — does Sharpe ratio improve?  
✅ Predict a 10% gain in AAPL and see total profit instantly  
✅ Identify hidden risk from stocks moving too similarly (correlation > 0.9)

---

## 📄 License

This project is licensed under the MIT License — free to use and modify.

---

## 🙋 Feedback and Contributions

- Questions? Open an issue
- Have an idea? Submit a pull request
- Like it? Give a ⭐ on GitHub or share it!
