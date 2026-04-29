# Data

Historical financial data for backtesting.

## raw/

Original downloaded data from yfinance.

## processed/

Cleaned and processed data ready for analysis.

## How to download data

```python
import yfinance as yf

df = yf.download('AAPL', start='2021-01-01', end='2026-04-01')
df.to_csv('data/raw/AAPL.csv')
```
