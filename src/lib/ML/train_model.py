# train_model.py
import requests
from bs4 import BeautifulSoup
import pickle
import os
from datetime import datetime
from config import Config
from data_collector import FTSEDataCollector
from random_forest import RandomForest

class ModelTrainer:
    def __init__(self):
        print("Initializing ModelTrainer...")
        self.data_collector = FTSEDataCollector(Config.API_KEY)
        self.model = RandomForest(n_trees=100, max_depth=10)
        
    def get_ftse250_stocks(self):
        print("Fetching FTSE250 stocks...")
        try:
            url = "https://en.wikipedia.org/wiki/FTSE_250_Index#Constituents"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            tables = soup.find_all('table', class_='wikitable')
            
            stocks = []
            if len(tables) >= 3:
                for row in tables[2].find_all('tr')[1:]:
                    cols = row.find_all('td')
                    if len(cols) > 1:
                        stocks.append({
                            'Company': cols[0].text.strip(),
                            'Ticker': cols[1].text.strip(),
                            'Industry': cols[2].text.strip()
                        })
                print(f"Found {len(stocks)} stocks")
                return stocks
            else:
                print("Error: Could not find FTSE250 table")
                return []
        except Exception as e:
            print(f"Error fetching FTSE250 stocks: {e}")
            return []

    def prepare_training_data(self, df):
        try:
            X = []
            y = []
            
            if df is not None and not df.empty:
                for i in range(len(df) - 1):
                    if all(col in df.columns for col in Config.FEATURES):
                        features = [float(df[col].iloc[i]) for col in Config.FEATURES]
                        target = float(df['Close'].iloc[i + 1] / df['Close'].iloc[i] - 1)
                        
                        if all(str(x) != 'nan' for x in features + [target]):
                            X.append(features)
                            y.append(target)
            
            return X, y
        except Exception as e:
            print(f"Error preparing training data: {e}")
            return [], []

    def train_and_save_model(self):
        try:
            print("\nStarting model training process...")
            stocks = self.get_ftse250_stocks()
            if not stocks:
                print("No stocks found to train on")
                return False

            all_X = []
            all_y = []
            processed_count = 0
            
            print("\nCollecting training data...")
            for stock in stocks:
                print(f"Processing {stock['Ticker']}...")
                data = self.data_collector.get_stock_data(stock['Ticker'])
                if data is not None:
                    X, y = self.prepare_training_data(data)
                    if X and y:
                        all_X.extend(X)
                        all_y.extend(y)
                        processed_count += 1
                        print(f"Added {len(X)} samples from {stock['Ticker']}")
            
            if not all_X or not all_y:
                print("No training data collected")
                return False

            print(f"\nTraining model with {len(all_X)} samples...")
            self.model.fit(all_X, all_y)
            
            # Save model with timestamp
            timestamp = datetime.now().strftime('%Y%m%d')
            filename = f'trained_model_{timestamp}.pkl'
            
            print(f"Saving model as {filename}...")
            with open(filename, 'wb') as f:
                pickle.dump(self.model, f)
                
            print("Model training completed successfully!")
            return True
            
        except Exception as e:
            print(f"Error in training process: {e}")
            return False

def main():
    print("Starting FTSE250 model training...")
    trainer = ModelTrainer()
    success = trainer.train_and_save_model()
    if success:
        print("\nModel training and saving completed successfully!")
    else:
        print("\nModel training failed!")

if __name__ == "__main__":
    main()