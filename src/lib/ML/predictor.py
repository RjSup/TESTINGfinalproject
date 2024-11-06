import os

import pickle

from data_collector import FTSEDataCollector

from config import Config



class StockPredictor:

    def __init__(self):

        self.data_collector = FTSEDataCollector()

        self.model_data = self.load_latest_model()

        

    def load_latest_model(self):

        try:

            # Get the absolute path to the ML directory

            current_dir = os.path.dirname(os.path.abspath(__file__))

            ml_dir = os.path.join(current_dir, '..', 'lib', 'ML')

            model_path = os.path.join(ml_dir, 'trained_model_20241106.pkl')

            

            print(f"Looking for model at: {model_path}")

            

            if os.path.exists(model_path):

                print(f"Found model at: {model_path}")

                with open(model_path, 'rb') as f:

                    return pickle.load(f)

            else:

                # Try alternative path

                alternative_path = os.path.join(current_dir, 'trained_model_20241106.pkl')

                print(f"Trying alternative path: {alternative_path}")

                

                if os.path.exists(alternative_path):

                    print(f"Found model at: {alternative_path}")

                    with open(alternative_path, 'rb') as f:

                        return pickle.load(f)

                else:

                    print("Model file not found in either location")

                    print(f"Current directory: {current_dir}")

                    print(f"Directory contents: {os.listdir(current_dir)}")

                    return None

                

        except Exception as e:

            print(f"Error loading model: {e}")

            print(f"Current working directory: {os.getcwd()}")

            print(f"Directory contents: {os.listdir()}")

            return None



    def predict_stock(self, ticker):

        try:

            if self.model_data is None:

                print("Model data not available")

                return None

                

            data = self.data_collector.get_stock_data(ticker)

            if data is None or data.empty:

                return None

                

            latest_features = [data[col].iloc[-1] for col in Config.FEATURES]

            scaled_features = self.model_data['scaler'].transform([latest_features])

            predicted_return = self.model_data['model'].predict(scaled_features)[0]

            

            current_price = float(data['Close'].iloc[-1])

            predicted_price = current_price * (1 + predicted_return)

            

            return {

                'current_price': current_price,

                'predicted_return': predicted_return,

                'predicted_price': predicted_price

            }

            

        except Exception as e:

            print(f"Error making prediction: {e}")

            return None