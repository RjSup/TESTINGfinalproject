import sys
import json
from scraper import company_by_industry

def process_investment_data(data):
    try:
        # Parse incoming data
        amount = float(data['investment_amount'])
        savings = float(data['current_savings'])
        risk = float(data['risk_tolerance'])
        industry = data.get('industry', 'General')  # Default to 'General' if industry is not provided

        # Calculate risk score based on amount and risk tolerance
        risk_score = (amount * 0.4 + savings * 0.3 + risk * 0.3) / 100
        
        # Determine portfolio allocation based on risk_score
        if risk_score > 0.7:
            portfolio = {"stocks": 80, "bonds": 15, "cash": 5}
            risk_level = "High"
        elif risk_score > 0.4:
            portfolio = {"stocks": 60, "bonds": 30, "cash": 10}
            risk_level = "Medium"
        else:
            portfolio = {"stocks": 40, "bonds": 40, "cash": 20}
            risk_level = "Low"

        industry_match = company_by_industry(industry)
        
        return {
            "success": True,
            "risk_score": round(risk_score, 2),
            "risk_level": risk_level,
            "portfolio": portfolio,
            "industry_match": industry_match
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    try:
        # Read input from stdin
        input_data = sys.stdin.read().strip()
        data = json.loads(input_data)
        
        # Process the data
        result = process_investment_data(data)
        
        # Print result as JSON
        print(json.dumps(result), flush=True)
        
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e)
        }), flush=True)
