import requests
from flask import current_app
import functools

# Try to import cache, but have a fallback if it fails
try:
    from app.cache import cache
    
    # Define a caching decorator that works with the cache
    def cached(timeout=60):
        def decorator(f):
            @functools.wraps(f)
            @cache.memoize(timeout=timeout)
            def decorated_function(*args, **kwargs):
                return f(*args, **kwargs)
            return decorated_function
        return decorator
        
except Exception:
    # Fallback decorator that does nothing if cache is not available
    def cached(timeout=60):
        def decorator(f):
            @functools.wraps(f)
            def decorated_function(*args, **kwargs):
                return f(*args, **kwargs)
            return decorated_function
        return decorator

class CoinGeckoAPI:
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    @staticmethod
    @cached(timeout=60)  # Cache for 1 minute
    def get_coin_list():
        """Get a list of all supported coins with their id, name, and symbol"""
        try:
            response = requests.get(f"{CoinGeckoAPI.BASE_URL}/coins/list")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            current_app.logger.error(f"Error fetching coin list: {str(e)}")
            return []
    
    @staticmethod
    @cached(timeout=30)  # Cache for 30 seconds
    def get_coin_price(coin_id, vs_currency="usd"):
        """Get current price of a coin in the specified currency"""
        try:
            response = requests.get(
                f"{CoinGeckoAPI.BASE_URL}/simple/price",
                params={
                    "ids": coin_id,
                    "vs_currencies": vs_currency
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            current_app.logger.error(f"Error fetching coin price for {coin_id}: {str(e)}")
            return {}
    
    @staticmethod
    @cached(timeout=60)  # Cache for 1 minute
    def get_market_data(vs_currency="usd", page=1, per_page=100):
        """Get market data for top coins"""
        try:
            response = requests.get(
                f"{CoinGeckoAPI.BASE_URL}/coins/markets",
                params={
                    "vs_currency": vs_currency,
                    "order": "market_cap_desc",
                    "per_page": per_page,
                    "page": page,
                    "sparkline": False
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            current_app.logger.error(f"Error fetching market data: {str(e)}")
            return [] 