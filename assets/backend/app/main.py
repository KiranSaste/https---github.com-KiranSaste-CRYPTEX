from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Initialize database
def get_db_connection():
    conn = sqlite3.connect('cryptex.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create portfolio table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS portfolio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        coin_id TEXT NOT NULL,
        amount REAL NOT NULL,
        purchase_price REAL,
        purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Create transactions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        coin_id TEXT NOT NULL,
        amount REAL NOT NULL,
        price REAL NOT NULL,
        transaction_type TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Helper function to check if user is logged in
def is_logged_in():
    return 'user' in session

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user'] = {
                'id': user['id'],
                'username': user['username'],
                'email': user['email']
            }
            flash('You are now logged in!', 'success')
            return redirect(url_for('wallet'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
        if not all([username, email, password, confirm_password]):
            flash('All fields are required', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        # Check if username or email already exists
        conn = get_db_connection()
        existing_user = conn.execute('SELECT * FROM users WHERE username = ? OR email = ?', 
                                  (username, email)).fetchone()
        
        if existing_user:
            conn.close()
            flash('Username or email already exists', 'error')
            return render_template('register.html')
        
        # Create new user
        hashed_password = generate_password_hash(password)
        conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                  (username, email, hashed_password))
        conn.commit()
        conn.close()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('home'))

@app.route('/wallet')
def wallet():
    if not is_logged_in():
        flash('Please log in to access your wallet', 'error')
        return redirect(url_for('login'))
    
    # Get user's portfolio
    conn = get_db_connection()
    portfolio = conn.execute('''
        SELECT p.coin_id, p.amount, p.purchase_price, p.purchase_date
        FROM portfolio p
        WHERE p.user_id = ?
    ''', (session['user']['id'],)).fetchall()
    
    # Get user's transactions
    transactions = conn.execute('''
        SELECT t.coin_id, t.amount, t.price, t.transaction_type, t.timestamp
        FROM transactions t
        WHERE t.user_id = ?
        ORDER BY t.timestamp DESC
        LIMIT 10
    ''', (session['user']['id'],)).fetchall()
    
    conn.close()
    
    # If no portfolio data, create some example data
    if not portfolio:
        example_portfolio = [
            {"coin_id": "bitcoin", "amount": 0.12, "symbol": "BTC", "name": "Bitcoin"},
            {"coin_id": "ethereum", "amount": 2.5, "symbol": "ETH", "name": "Ethereum"},
            {"coin_id": "tether", "amount": 1000, "symbol": "USDT", "name": "Tether"},
            {"coin_id": "cardano", "amount": 1250, "symbol": "ADA", "name": "Cardano"},
            {"coin_id": "solana", "amount": 3.8, "symbol": "SOL", "name": "Solana"}
        ]
    else:
        example_portfolio = []
        for coin in portfolio:
            example_portfolio.append({
                "coin_id": coin['coin_id'],
                "amount": coin['amount'],
                "symbol": coin['coin_id'][:3].upper(),  # Simplified for example
                "name": coin['coin_id'].capitalize()
            })
    
    return render_template('wallet.html', portfolio=example_portfolio, transactions=transactions)

@app.route('/trade')
def trade():
    return render_template('trade.html')

@app.route('/market')
def market():
    return render_template('market.html')

@app.route('/sell')
def sell():
    return render_template('sell.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/bitusd')
def bitusd():
    return render_template('bitusd.html')

@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    if not is_logged_in():
        return json.dumps({'error': 'Not authenticated'}), 401
    
    conn = get_db_connection()
    portfolio = conn.execute('''
        SELECT p.coin_id, p.amount, p.purchase_price, p.purchase_date
        FROM portfolio p
        WHERE p.user_id = ?
    ''', (session['user']['id'],)).fetchall()
    conn.close()
    
    # Convert to list of dicts
    result = []
    for coin in portfolio:
        result.append({
            'coin_id': coin['coin_id'],
            'amount': coin['amount'],
            'purchase_price': coin['purchase_price'],
            'purchase_date': coin['purchase_date']
        })
    
    return json.dumps(result)

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    if not is_logged_in():
        return json.dumps({'error': 'Not authenticated'}), 401
    
    conn = get_db_connection()
    transactions = conn.execute('''
        SELECT t.coin_id, t.amount, t.price, t.transaction_type, t.timestamp
        FROM transactions t
        WHERE t.user_id = ?
        ORDER BY t.timestamp DESC
        LIMIT 20
    ''', (session['user']['id'],)).fetchall()
    conn.close()
    
    # Convert to list of dicts
    result = []
    for tx in transactions:
        result.append({
            'coin_id': tx['coin_id'],
            'amount': tx['amount'],
            'price': tx['price'],
            'transaction_type': tx['transaction_type'],
            'timestamp': tx['timestamp']
        })
    
    return json.dumps(result)

@app.route('/api/trade', methods=['POST'])
def execute_trade():
    if not is_logged_in():
        return json.dumps({'error': 'Not authenticated'}), 401
    
    data = request.json
    
    # Validate request
    required_fields = ['coin_id', 'amount', 'price', 'transaction_type']
    if not all(field in data for field in required_fields):
        return json.dumps({'error': 'Missing required fields'}), 400
    
    coin_id = data['coin_id']
    amount = float(data['amount'])
    price = float(data['price'])
    transaction_type = data['transaction_type']
    
    # Validate data
    if amount <= 0 or price <= 0:
        return json.dumps({'error': 'Amount and price must be positive'}), 400
    
    if transaction_type not in ['buy', 'sell']:
        return json.dumps({'error': 'Invalid transaction type'}), 400
    
    user_id = session['user']['id']
    
    conn = get_db_connection()
    
    # Add transaction
    conn.execute('''
        INSERT INTO transactions (user_id, coin_id, amount, price, transaction_type)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, coin_id, amount, price, transaction_type))
    
    # Update portfolio
    if transaction_type == 'buy':
        # Check if user already owns this coin
        existing = conn.execute('''
            SELECT id, amount FROM portfolio
            WHERE user_id = ? AND coin_id = ?
        ''', (user_id, coin_id)).fetchone()
        
        if existing:
            # Update existing portfolio entry
            conn.execute('''
                UPDATE portfolio
                SET amount = amount + ?
                WHERE id = ?
            ''', (amount, existing['id']))
        else:
            # Add new portfolio entry
            conn.execute('''
                INSERT INTO portfolio (user_id, coin_id, amount, purchase_price)
                VALUES (?, ?, ?, ?)
            ''', (user_id, coin_id, amount, price))
    else:  # Sell
        # Check if user has enough of this coin
        existing = conn.execute('''
            SELECT id, amount FROM portfolio
            WHERE user_id = ? AND coin_id = ?
        ''', (user_id, coin_id)).fetchone()
        
        if not existing or existing['amount'] < amount:
            conn.close()
            return json.dumps({'error': 'Insufficient balance'}), 400
        
        # Update portfolio
        new_amount = existing['amount'] - amount
        if new_amount > 0:
            conn.execute('''
                UPDATE portfolio
                SET amount = ?
                WHERE id = ?
            ''', (new_amount, existing['id']))
        else:
            # Remove coin from portfolio if amount is 0
            conn.execute('''
                DELETE FROM portfolio
                WHERE id = ?
            ''', (existing['id'],))
    
    conn.commit()
    conn.close()
    
    return json.dumps({'success': True})

if __name__ == '__main__':
    app.run(debug=True) 