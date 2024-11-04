import os
import pickle
from config import Config
from data_collector import FTSEDataCollector

class StockPredictor:
    def __init__(self):
        self.data_collector = FTSEDataCollector()
        self.model = self.load_latest_model()

    def load_latest_model(self):
        try:
            current_dir = os.getcwd()
            ml_dir = os.path.join(current_dir, 'src', 'lib', 'ML')
            
            model_files = []
            if os.path.exists(ml_dir):
                model_files.extend([f for f in os.listdir(ml_dir) if f.startswith('trained_model_')])
            model_files.extend([f for f in os.listdir(current_dir) if f.startswith('trained_model_')])

            if not model_files:
                return None

            latest_model = max(model_files)
            model_path = os.path.join(ml_dir, latest_model) if latest_model in os.listdir(ml_dir) else latest_model

            with open(model_path, 'rb') as f:
                return pickle.load(f)

        except Exception:
            return None

    def predict_stock(self, ticker):
        try:
            if self.model is None:
                return None

            data = self.data_collector.get_stock_data(ticker)
            if data is None or data.empty:
                return None

            if not all(feature in data.columns for feature in Config.FEATURES):
                return None

            latest_features = [float(data[col].iloc[-1]) for col in Config.FEATURES]
            predicted_return = self.model.predict([latest_features])[0]
            current_price = float(data['Close'].iloc[-1])

            return {
                'current_price': current_price,
                'predicted_return': predicted_return,
                'predicted_price': current_price * (1 + predicted_return)
            }

        except Exception:
            return None