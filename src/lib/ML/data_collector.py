import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class FTSEDataCollector:
    def get_stock_data(self, ticker):
        try:
            ticker = ticker.strip()
            if not ticker.endswith('.L'):
                ticker = f"{ticker}.L"

            stock = yf.Ticker(ticker)
            df = stock.history(period="2y", interval="1mo")
            
            if df.empty:
                return None

            return self._add_features(df)

        except Exception:
            return None

    def _add_features(self, df):
        try:
            # Returns
            df['return_1m'] = df['Close'].pct_change().fillna(0)
            df['return_3m'] = df['Close'].pct_change(periods=3).fillna(0)
            df['return_6m'] = df['Close'].pct_change(periods=6).fillna(0)
            
            # Moving averages
            df['SMA3'] = df['Close'].rolling(window=3).mean().bfill()
            df['SMA6'] = df['Close'].rolling(window=6).mean().bfill()
            df['sma3_cross'] = (df['Close'] > df['SMA3']).astype(float)
            df['sma6_cross'] = (df['Close'] > df['SMA6']).astype(float)
            
            # RSI
            delta = df['Close'].diff()
            gain = delta.where(delta > 0, 0).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / (loss + 1e-9)
            df['rsi'] = 100 - (100 / (1 + rs))
            
            # MACD
            exp1 = df['Close'].ewm(span=12).mean()
            exp2 = df['Close'].ewm(span=26).mean()
            df['MACD'] = exp1 - exp2
            df['Signal'] = df['MACD'].ewm(span=9).mean()
            df['macd_signal'] = (df['MACD'] > df['Signal']).astype(float)
            
            # Volatility and volume
            df['volatility'] = df['return_1m'].rolling(window=12).std().fillna(0)
            df['volume_ratio'] = (df['Volume'] / df['Volume'].rolling(window=3).mean()).fillna(1)
            
            return df.fillna(0)

        except Exception:
            return None
