from random_forest import RandomForest
from data_collector import FTSEDataCollector
from config import Config
from scraper import get_ftse250
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import numpy as np
import pickle
from datetime import datetime

class ModelTrainer:
    def __init__(self):
        self.data_collector = FTSEDataCollector()
        self.model = RandomForest()
        self.scaler = StandardScaler()
        
    def prepare_training_data(self, df):
        if df is not None and not df.empty:
            feature_matrix = df[Config.FEATURES].values[:-1]
            close_prices = df['Close'].values
            
            # Handle zero or negative prices
            valid_prices = close_prices > 0
            if not np.any(valid_prices[:-1]):
                return None, None
                
            returns = np.zeros(len(close_prices) - 1)
            valid_indices = valid_prices[:-1] & valid_prices[1:]
            returns[valid_indices] = np.diff(close_prices)[valid_indices] / close_prices[:-1][valid_indices]
            
            # Remove any invalid returns
            valid_mask = (~np.isnan(feature_matrix).any(axis=1) & 
                         ~np.isinf(feature_matrix).any(axis=1) &
                         ~np.isnan(returns) & 
                         ~np.isinf(returns))
            
            if np.sum(valid_mask) < 2:  # Need at least 2 valid samples
                return None, None
                
            return feature_matrix[valid_mask].tolist(), returns[valid_mask].tolist()
        
        return None, None

    def train_model(self):
        print("Getting FTSE250 stocks...")
        stocks = get_ftse250()
        
        if not stocks:
            print("Failed to get FTSE250 stocks")
            return False

        all_X = []
        all_y = []
        
        print(f"\nCollecting data for {len(stocks)} stocks...")
        for stock in stocks:
            ticker = stock['Ticker']
            print(f"Processing {ticker}...")
            data = self.data_collector.get_stock_data(ticker)
            if data is not None:
                X, y = self.prepare_training_data(data)
                if X is not None and len(X) > 0:
                    all_X.extend(X)
                    all_y.extend(y)
                    print(f"Added {len(X)} samples from {ticker}")
                else:
                    print(f"No valid data points for {ticker}")
            else:
                print(f"Failed to collect data for {ticker}")
        
        if not all_X:
            print("No training data collected")
            return False
        
        print(f"\nTotal samples collected: {len(all_X)}")
        
        X_train, X_test, y_train, y_test = train_test_split(
            np.array(all_X),
            np.array(all_y),
            test_size=0.2,
            random_state=42
        )
        
        print("\nScaling features...")
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        print("Training model...")
        self.model.fit(X_train_scaled, y_train)
        
        print("Making predictions...")
        y_pred = self.model.predict(X_test_scaled)
        
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print("\nModel Performance Metrics:")
        print(f"MSE: {mse:.6f}")
        print(f"RMSE: {rmse:.6f}")
        print(f"MAE: {mae:.6f}")
        print(f"R²: {r2:.4f}")
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'metrics': {
                'mse': mse,
                'rmse': rmse,
                'mae': mae,
                'r2': r2
            }
        }
        
        timestamp = datetime.now().strftime('%Y%m%d')
        filename = f'trained_model_{timestamp}.pkl'
        print(f"\nSaving model as {filename}...")
        
        with open(filename, 'wb') as f:
            pickle.dump(model_data, f)
        
        return True

def main():
    print("Starting FTSE250 model training...")
    trainer = ModelTrainer()
    success = trainer.train_model()
    if success:
        print("\nModel training and saving completed successfully!")
    else:
        print("\nModel training failed!")

if __name__ == "__main__":
    main()