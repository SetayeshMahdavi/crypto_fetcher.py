import json
import requests

def get_crypto_prices_from_api(api_url, symbols, currency="IRT"):
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        data_string = response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching data from API: {e}"

    if data_string.strip().endswith(',"IRT":{"high_24":"14'):
        data_string = data_string.rsplit(',"IRT":{"high_24":"14', 1)[0] + '}'
        print("Warning: Incomplete JSON data detected and partially corrected.")

    try:
        data = json.loads(data_string)
    except json.JSONDecodeError as e:
        return f"Error parsing JSON data: {e}"

    results = {}
    if 'currencies' not in data:
        return "Error: 'currencies' key not found in the response data."
        
    for symbol in symbols:
        try:
            if symbol in data['currencies'] and currency in data['currencies'][symbol]:
                price = data['currencies'][symbol][currency]['price']
                results[symbol] = price
            else:
                results[symbol] = "Not found"
        except KeyError:
            results[symbol] = "Price not found"
        except Exception as e:
            results[symbol] = f"Error: {e}"
            
    return results

API_URL = "https://api-web.tabdeal.org/r/plots/currencies/dynamic-info/"
TARGET_SYMBOLS = ["BTC", "ETH", "BNB", "XRP", "LTC", "BCH", "ETC", "TRX", "DOGE", "USDT"] 
TARGET_CURRENCY = "IRT" 

print(f"Fetching prices for {TARGET_SYMBOLS} in {TARGET_CURRENCY}...")

prices = get_crypto_prices_from_api(API_URL, TARGET_SYMBOLS, TARGET_CURRENCY)

if isinstance(prices, str): 
    print(prices)
else:
    print("\nCurrent Prices:")
    for symbol, price in prices.items():
        print(f"- {symbol}: {price}")
