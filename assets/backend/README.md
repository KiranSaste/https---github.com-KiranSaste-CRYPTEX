# Cryptex Trading Platform

Cryptex is a modern cryptocurrency trading platform built with Flask, SQLAlchemy, and WebSockets for real-time updates. The platform allows users to track crypto prices, place orders, and manage their portfolio.

## Features

- User authentication with secure password hashing
- Real-time cryptocurrency price updates
- Live order book and trade execution
- Portfolio tracking with profit/loss calculations
- RESTful API for crypto market data
- Rate limiting and caching for performance optimization
- Error handling and logging

## Tech Stack

- **Backend:** Flask, SQLAlchemy, Flask-SocketIO
- **Database:** MySQL
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **API Integration:** CoinGecko API
- **Caching:** Redis
- **Security:** Flask-Login, Flask-WTF, Flask-Bcrypt

## Getting Started

### Prerequisites

- Python 3.8+
- MySQL database
- Redis (for caching and rate limiting)

### Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Create a `.env` file in the project root with the following variables:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   FLASK_DEBUG=1
   SECRET_KEY=your-secret-key
   SQLALCHEMY_DATABASE_URI=mysql+pymysql://user:password@localhost:3306/cryptex
   SENTRY_DSN=your-sentry-dsn
   ```
6. Initialize the database:
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```
7. Start the development server:
   ```
   flask run
   ```

## Project Structure

```
cryptex/
├── app/
│   ├── __init__.py           # Application factory and extension initialization
│   ├── models.py             # Database models
│   ├── routes.py             # Route handlers
│   ├── forms.py              # Form definitions
│   ├── api.py                # CoinGecko API integration
│   ├── sockets.py            # WebSocket event handlers
│   ├── cache.py              # Caching and rate limiting configuration
│   ├── logging_config.py     # Logging configuration
│   ├── error_handlers.py     # Error handlers
│   ├── config.py             # Application configuration
│   ├── static/               # Static assets
│   └── templates/            # HTML templates
├── migrations/               # Database migrations
├── tests/                    # Test files
├── app.py                    # Application entry point
├── wsgi.py                   # WSGI entry point for production
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## API Endpoints

### Authentication

- `POST /login.html` - User login
- `POST /register.html` - User registration
- `GET /logout` - User logout

### Cryptocurrency Data

- `GET /api/crypto/list` - List all cryptocurrencies
- `GET /api/crypto/price/<coin_id>` - Get price for a specific coin
- `GET /api/crypto/markets` - Get market data for top coins

### Trading

- `POST /api/place_order` - Place a buy/sell order

## Testing

Run the test suite:

```
pytest
```

## Deployment

For production deployment:

1. Set up a production server (Heroku, AWS, etc.)
2. Configure Gunicorn as the WSGI server
3. Set up Nginx as a reverse proxy
4. Configure SSL for secure connections
5. Set environment variables for production settings
6. Run database migrations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 