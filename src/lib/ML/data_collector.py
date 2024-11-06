import yfinance as yf
import pandas as pd
import numpy as np

class FTSEDataCollector:
    def __init__(self):
        pass
        
    def get_stock_data(self, ticker):
        try:
            if not ticker.endswith('.L'):
                ticker = f"{ticker}.L"
                
            stock = yf.Ticker(ticker)
            df = stock.history(period="5y", interval="1wk")
            
            if df.empty:
                return None
                
            return self._add_features(df)
            
        except Exception as e:
            print(f"Error collecting data for {ticker}: {e}")
            return None
            
    def _add_features(self, df):
        try:
            close = df['Close'].values
            
            # Basic returns
            for period in [1, 4, 12]:
                df[f'return_{period}w'] = df['Close'].pct_change(period)
            # Simple moving average crossover
            sma20 = pd.Series(close).rolling(window=3).mean()
            df['sma_cross'] = (close > sma20).astype(float)
            
            # Basic RSI
            delta = np.diff(close, prepend=close[0])
            gain = np.where(delta > 0, delta, 0)
            loss = np.where(delta < 0, -delta, 0)
            avg_gain = pd.Series(gain).rolling(window=14).mean()
            avg_loss = pd.Series(loss).rolling(window=14).mean()
            rs = avg_gain / (avg_loss + 1e-9)
            df['rsi'] = 100 - (100 / (1 + rs))
            
            # Simple MACD
            exp12 = pd.Series(close).ewm(span=12).mean()
            exp26 = pd.Series(close).ewm(span=26).mean()
            macd = exp12 - exp26
            signal = macd.rolling(window=9).mean()
            df['macd_signal'] = (macd > signal).astype(float)
            
            # Basic volatility
            df['volatility'] = pd.Series(df['return_1w']).rolling(window=12).std()
            
            return df.fillna(0)
            
        except Exception as e:
            print(f"Error adding features: {e}")
            return None