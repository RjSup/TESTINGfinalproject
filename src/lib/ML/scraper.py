import pandas as pd
import requests 
from bs4 import BeautifulSoup

def get_ftse250():
    # url and web headers
    url="https://en.wikipedia.org/wiki/FTSE_250_Index#Constituents"

    try:
        # fetch data from website
        response =  requests.get(url)

        # parsing htlm
        soup = BeautifulSoup(response.content, 'html.parser')

        # data to find
        table = soup.find_all('table', class_='wikitable')
        
        # the target table was third
        if len(table) >= 3:
            # select third table
            t = table[2]
        
            # take stock data
            stocks = []

            # skip header row
            for row in t.find_all('tr')[1:]:
                cols = row.find_all('td')
                if len(cols) > 1:
                    company = cols[0].text.strip()
                    ticker = cols[1].text.strip() + '.L'
                    industry = cols[2].text.strip()

                    stocks.append({
                        'Company': company,
                        'Ticker': ticker,
                        'Industry': industry
                    })
            
            stocks.sort(key=lambda x: x['Industry'])

            # create a dataframe and save it to csv
            df = pd.DataFrame(stocks)
            df.to_csv('FTSE250.csv', index=False)
            return stocks
        return None
    except requests.RequestException as e:
        print(f"Error fetching: {str(e)}")
        return None
    
def company_by_industry(industry):
    stocks = get_ftse250()
    if not stocks:
        return []
        
    industry = industry.lower()
    keywords = {
        'technology': ['tech', 'software', 'digital', 'computer', 'it'],
        'financial': ['bank', 'insurance', 'invest', 'finance'],
        'healthcare': ['health', 'medical', 'pharma', 'biotech'],
    }
    
    search_terms = keywords.get(industry, [industry])
    
    matching_companies = [
        stock for stock in stocks
        if any(term in stock['Industry'].lower() or term in stock['Company'].lower() 
              for term in search_terms)
    ]
    
    return matching_companies

if __name__ == "__main__":
    print("Getting data from FTSE 250")
    data = get_ftse250()

    if data is None:
        print("Fail")
    else:
        print("Data scraped sucessfully")

    matches = company_by_industry()