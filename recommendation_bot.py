import yfinance as yf
import pandas as pd
import ta

def get_recommendations():
    df = pd.read_csv("nse_200_stocks.csv")
    tickers = df['Ticker'].tolist()
    recommendations = []

    for ticker in tickers:
        try:
            stock = yf.download(ticker, period='3mo', interval='1d', progress=False)
            if stock.empty:
                continue

            stock['RSI'] = ta.momentum.RSIIndicator(stock['Close']).rsi()
            macd = ta.trend.MACD(stock['Close'])
            stock['MACD_diff'] = macd.macd_diff()
            latest = stock.iloc[-1]

            if latest['RSI'] < 30 and latest['MACD_diff'] > 0:
                recommendations.append({
                    'Ticker': ticker,
                    'Action': 'Buy',
                    'RSI': round(latest['RSI'], 2),
                    'MACD Diff': round(latest['MACD_diff'], 2),
                    'Reason': 'RSI < 30 and MACD crossover'
                })
            elif latest['RSI'] > 70 and latest['MACD_diff'] < 0:
                recommendations.append({
                    'Ticker': ticker,
                    'Action': 'Sell',
                    'RSI': round(latest['RSI'], 2),
                    'MACD Diff': round(latest['MACD_diff'], 2),
                    'Reason': 'RSI > 70 and MACD reversal'
                })

        except Exception as e:
            print(f"Error for {ticker}: {e}")
            continue

    return pd.DataFrame(recommendations)
