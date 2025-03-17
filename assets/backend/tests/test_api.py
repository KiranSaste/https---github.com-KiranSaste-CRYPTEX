import pytest
from app.api import CoinGeckoAPI
from unittest.mock import patch, MagicMock

def test_coin_list(app, client):
    """Test getting the coin list API endpoint"""
    with patch('app.api.requests.get') as mock_get:
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin"},
            {"id": "ethereum", "symbol": "eth", "name": "Ethereum"}
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Make the request
        response = client.get('/api/crypto/list')
        
        # Assert response
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2
        assert data[0]['id'] == 'bitcoin'
        assert data[1]['id'] == 'ethereum'

def test_coin_price(app, client):
    """Test getting a coin price"""
    with patch('app.api.requests.get') as mock_get:
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {"bitcoin": {"usd": 50000}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Make the request
        response = client.get('/api/crypto/price/bitcoin')
        
        # Assert response
        assert response.status_code == 200
        data = response.get_json()
        assert 'bitcoin' in data
        assert 'usd' in data['bitcoin']
        assert data['bitcoin']['usd'] == 50000 