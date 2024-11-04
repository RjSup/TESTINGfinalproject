import sys
import json
from datetime import datetime, timedelta
from predictor import StockPredictor
from scraper import company_by_industry

def process_investment_data(data):
    try:
        # Parse input data
        amount = float(data['investment_amount'])
        savings = float(data['current_savings'])
        risk = float(data['risk_tolerance'])
        industry = data.get('industry', 'General')

        # Get matching companies
        matching_companies = company_by_industry(industry)
        if not matching_companies:
            return {
                "success": False,
                "error": f"No companies found in {industry} industry"
            }

        # Initialize predictor
        predictor = StockPredictor()
        if predictor.model is None:
            return {
                "success": False,
                "error": "Model not available"
            }

        # Get predictions for matching companies (only positive returns)
        predictions = []
        for company in matching_companies:
            prediction = predictor.predict_stock(company['Ticker'])
            if prediction is not None:
                predicted_return = prediction['predicted_return']
                if predicted_return > 0:  # Only include positive returns
                    predictions.append({
                        'company': company['Company'],
                        'ticker': company['Ticker'],
                        'industry': company['Industry'],
                        'current_price': prediction['current_price'],
                        'predicted_price': prediction['predicted_price'],
                        'predicted_return': predicted_return
                    })

        if not predictions:
            return {
                "success": False,
                "error": "No positive predictions available for this industry"
            }

        # Determine number of stocks based on risk level
        if risk > 7:
            num_stocks = min(4, len(predictions))  # Take minimum of 4 or available stocks
            risk_level = "High"
        elif risk > 4:
            num_stocks = min(6, len(predictions))
            risk_level = "Medium"
        else:
            num_stocks = min(8, len(predictions))
            risk_level = "Low"

        # Sort by predicted return and select top stocks
        selected_stocks = sorted(
            predictions, 
            key=lambda x: x['predicted_return'], 
            reverse=True
        )[:num_stocks]

        # Calculate portfolio metrics with only positive returns
        allocation_per_stock = amount / len(selected_stocks)
        total_predicted_return = 0
        total_predicted_value = 0
        portfolio = []

        for stock in selected_stocks:
            shares = allocation_per_stock / stock['current_price']
            predicted_gain = (stock['predicted_price'] - stock['current_price']) * shares
            total_predicted_return += predicted_gain
            total_predicted_value += (shares * stock['predicted_price'])

            portfolio.append({
                'company': stock['company'],
                'ticker': stock['ticker'],
                'industry': stock['industry'],
                'allocation': round(allocation_per_stock, 2),
                'shares': round(shares, 2),
                'current_price': round(stock['current_price'], 2),
                'predicted_price': round(stock['predicted_price'], 2),
                'predicted_return': round(stock['predicted_return'] * 100, 2),
                'predicted_gain': round(predicted_gain, 2)
            })

        return {
            "success": True,
            "risk_level": risk_level,
            "portfolio": portfolio,
            "summary": {
                "initial_investment": round(amount, 2),
                "number_of_stocks": len(portfolio),
                "allocation_per_stock": round(allocation_per_stock, 2),
                "total_predicted_gain": round(total_predicted_return, 2),
                "predicted_portfolio_value": round(total_predicted_value, 2),
                "total_return_percentage": round((total_predicted_value - amount) / amount * 100, 2),
                "rebalance_date": (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
            }
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    
if __name__ == "__main__":
    try:
        input_data = sys.stdin.read().strip()
        data = json.loads(input_data)
        result = process_investment_data(data)
        print(json.dumps(result), flush=True)
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e)
        }), flush=True)
