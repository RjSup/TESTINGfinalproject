# train_model.py
import requests
from bs4 import BeautifulSoup
import pickle
import os
from datetime import datetime
from config import Config
from data_collector import FTSEDataCollector
from random_forest import RandomForest
from sklearn.model_selection import GridSearchCV, cross_val_score

class ModelTrainer:
    def __init__(self):
        print("Initializing ModelTrainer...")
        self.data_collector = FTSEDataCollector()
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
                        
                        # Handle division by zero
                        if df['Close'].iloc[i] == 0:
                            target = 0
                        else:
                            target = float(df['Close'].iloc[i + 1] / df['Close'].iloc[i] - 1)
                        
                        if all(str(x) != 'nan' for x in features + [target]):
                            X.append(features)
                            y.append(target)
                        else:
                            print(f"Skipping row {i} due to NaN values in features or target")
                    else:
                        print(f"Skipping row {i} due to missing features")
            
            return X, y
        except Exception as e:
            print(f"Error preparing training data: {e}")
            return [], []

    def train_and_save_model(self, all_X, all_y):
        try:
            # Define the parameter grid
            param_grid = {
                'n_trees': [50, 100, 200],
                'max_depth': [5, 10, 20],
                'n_jobs': [-1]
            }

            # Initialize the RandomForest model
            rf = RandomForest()

            # Initialize GridSearchCV
            grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, scoring='accuracy')

            # Fit the model
            grid_search.fit(all_X, all_y)

            # Get the best parameters
            best_params = grid_search.best_params_
            print(f"Best parameters: {best_params}")

            # Train the model with the best parameters
            best_model = RandomForest(**best_params)
            best_model.fit(all_X, all_y)

            # Evaluate the model
            scores = cross_val_score(best_model, all_X, all_y, cv=5)
            print(f"Cross-validation scores: {scores}")
            print(f"Mean cross-validation score: {scores.mean()}")

            # Save model with timestamp
            timestamp = datetime.now().strftime('%Y%m%d')
            filename = f'trained_model_{timestamp}.pkl'
            
            print(f"Saving model as {filename}...")
            with open(filename, 'wb') as f:
                pickle.dump(best_model, f)
                
            print("Model training completed successfully!")
            return True
            
        except Exception as e:
            print(f"Error in training process: {e}")
            return False

    def train_and_save_model_wrapper(self):
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
                    else:
                        print(f"No valid data for {stock['Ticker']}")
                else:
                    print(f"No data found for {stock['Ticker']}")
            
            if not all_X or not all_y:
                print("No training data collected")
                return False

            print(f"\nTraining model with {len(all_X)} samples...")
            success = self.train_and_save_model(all_X, all_y)
            return success
            
        except Exception as e:
            print(f"Error in training process: {e}")
            return False

def main():
    print("Starting FTSE250 model training...")
    trainer = ModelTrainer()
    success = trainer.train_and_save_model_wrapper()
    if success:
        print("\nModel training and saving completed successfully!")
    else:
        print("\nModel training failed!")

if __name__ == "__main__":
    main()