# Cryptex - Cryptocurrency Trading Platform

Cryptex is a modern cryptocurrency trading and portfolio management web application that allows users to track, buy, and sell cryptocurrencies with real-time price data.

## Features

- **Real-time Crypto Data**: Live cryptocurrency prices and charts using the CoinGecko API
- **Responsive Design**: Beautiful UI that works on both desktop and mobile devices
- **User Authentication**: Secure login and registration system
- **Portfolio Tracking**: View and manage your cryptocurrency holdings
- **Trading Interface**: Buy and sell cryptocurrencies with an intuitive interface
- **Market Overview**: Comprehensive market data with filtering and search capabilities

## Screenshots

### Home Page
![Homepage](assets/backend/app/static/images/screenshot-home.png)

### Trading Page
![Trading](assets/backend/app/static/images/screenshot-trade.png)

### Markets Page
![Markets](assets/backend/app/static/images/screenshot-markets.png)

## Installation and Setup

### Prerequisites
- Python 3.7+
- SQLite

### Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/cryptex.git
   cd cryptex
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   cd assets/backend
   python app/main.py
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Demo Credentials

For testing purposes, you can use the following credentials:

- **Username**: demo
- **Password**: password123

## Project Structure

```
└── assets/
    └── backend/
        └── app/
            ├── static/          # Static assets (CSS, JS, images)
            │   ├── css/         # Stylesheets
            │   ├── js/          # JavaScript files
            │   └── images/      # Image files
            ├── templates/       # HTML templates
            │   ├── index.html   # Homepage
            │   ├── login.html   # Login page
            │   ├── trade.html   # Trading interface
            │   └── ...          # Other templates
            └── main.py          # Flask application
```

## API Integration

Cryptex uses the [CoinGecko API](https://www.coingecko.com/en/api) to fetch real-time cryptocurrency data. No API key is required for basic usage, but there are rate limits.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **Backend**: Flask (Python web framework)
- **Database**: SQLite
- **Authentication**: Flask session-based authentication

## Future Enhancements

- Add support for limit orders and stop-loss orders
- Implement email notifications for price alerts
- Add two-factor authentication for increased security
- Create a mobile app version using React Native

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 