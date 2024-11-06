import sys
import json
from datetime import datetime, timedelta
from predictor import StockPredictor
from scraper import company_by_industry
import traceback
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('portfolio_prediction.log'),
        logging.StreamHandler(sys.stderr)
    ]
)

def validate_input(data):
    """Validate input data and return error message if invalid"""
    try:
        # Check required fields
        required_fields = ['investment_amount', 'risk_tolerance']
        for field in required_fields:
            if field not in data:
                return f"Missing required field: {field}"

        # Convert and validate investment amount
        amount = float(data['investment_amount'])
        if amount <= 0:
            return "Investment amount must be greater than 0"
        if amount > 1000000000:  # Arbitrary upper limit
            return "Investment amount too large"

        # Convert and validate risk tolerance
        risk = float(data['risk_tolerance'])
        if risk < 1 or risk > 10:
            return "Risk tolerance must be between 1 and 10"

        return None  # No error
    except ValueError as e:
        return f"Invalid numeric value: {str(e)}"
    except Exception as e:
        return f"Validation error: {str(e)}"

def process_investment_data(data):
    """Process investment data and generate portfolio recommendations"""
    try:
        logging.info("Starting investment data processing")
        
        # Validate input
        error = validate_input(data)
        if error:
            logging.error(f"Input validation failed: {error}")
            return {
                "success": False,
                "error": error
            }

        # Parse input data
        amount = float(data['investment_amount'])
        risk = float(data['risk_tolerance'])
        industry = data.get('industry', 'General')
        
        logging.info(f"Processing request - Amount: {amount}, Risk: {risk}, Industry: {industry}")

        # Get matching companies
        logging.info(f"Fetching companies for industry: {industry}")
        matching_companies = company_by_industry(industry)
        if not matching_companies:
            logging.warning(f"No companies found for industry: {industry}")
            return {
                "success": False,
                "error": f"No companies found in {industry} industry"
            }

        # Initialize predictor
        logging.info("Initializing stock predictor")
        predictor = StockPredictor()
        if predictor.model_data is None:
            logging.error("Model not available")
            return {
                "success": False,
                "error": "Model not available"
            }

        # Get predictions for matching companies
        logging.info("Making predictions for matching companies")
        predictions = []
        for company in matching_companies:
            try:
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
            except Exception as e:
                logging.warning(f"Failed to process prediction for {company['Ticker']}: {str(e)}")
                continue

        if not predictions:
            logging.warning("No positive predictions available")
            return {
                "success": False,
                "error": "No positive predictions available for this industry"
            }

        # Determine portfolio size based on risk
        logging.info("Determining portfolio size based on risk level")
        if risk > 7:
            num_stocks = min(4, len(predictions))
            risk_level = "High"
        elif risk > 4:
            num_stocks = min(6, len(predictions))
            risk_level = "Medium"
        else:
            num_stocks = min(8, len(predictions))
            risk_level = "Low"

        # Select top performing stocks
        selected_stocks = sorted(
            predictions, 
            key=lambda x: x['predicted_return'], 
            reverse=True
        )[:num_stocks]

        # Calculate portfolio allocation
        logging.info("Calculating portfolio allocation")
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

        # Prepare response
        result = {
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

        logging.info("Successfully generated portfolio recommendation")
        return result

    except Exception as e:
        logging.error(f"Error in process_investment_data: {str(e)}")
        logging.error(traceback.format_exc())
        return {
            "success": False,
            "error": str(e)
        }

def main():
    """Main entry point for the script"""
    try:
        logging.info("Starting portfolio prediction process")
        
        # Read input from stdin
        input_data = sys.stdin.read().strip()
        if not input_data:
            logging.error("No input data provided")
            print(json.dumps({
                "success": False,
                "error": "No input data provided"
            }), flush=True)
            return

        # Parse JSON input
        try:
            data = json.loads(input_data)
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON input: {str(e)}")
            print(json.dumps({
                "success": False,
                "error": f"Invalid JSON input: {str(e)}"
            }), flush=True)
            return

        # Process data and return result
        result = process_investment_data(data)
        print(json.dumps(result), flush=True)

    except Exception as e:
        logging.error(f"Unexpected error in main: {str(e)}")
        logging.error(traceback.format_exc())
        print(json.dumps({
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }), flush=True)

if __name__ == "__main__":
    main()