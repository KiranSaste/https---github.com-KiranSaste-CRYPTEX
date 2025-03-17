from app import socketio
from flask_socketio import emit
import requests
import json

@socketio.on('connect')
def handle_connect():
    emit('connection_response', {'data': 'Connected'})

@socketio.on('subscribe_price_updates')
def handle_price_updates(data):
    # Fetch from CoinGecko API
    coin_id = data['coin_id']
    response = requests.get(
        f'https://api.coingecko.com/api/v3/simple/price',
        params={'ids': coin_id, 'vs_currencies': 'usd'}
    )
    price_data = response.json()
    emit('price_update', price_data) 