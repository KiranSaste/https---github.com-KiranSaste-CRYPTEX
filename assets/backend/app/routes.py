# "'This code for only testing purpose'"

# from flask import Blueprint, render_template

# main = Blueprint('main', __name__)

# @main.route('/')
# def home():
#     return "Welcome to Cryptex!"

from flask import render_template, current_app as app
from app import db

from flask import Blueprint,request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
from app.models import User
from flask import current_app as app
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, RegisterForm

from app.models import User  # Import your User model

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route("/")
#@login_required  # Protects home route, requires login
def home():
    #with app.app_context():  
        return render_template("index.html")

@main.route("/market.html")
def market():
    return render_template("market.html")

@main.route("/trade.html")
def trade():
    return render_template("trade.html")

@main.route("/blog.html")
def blog():
    return render_template("blog.html")



# # Edited code for testing purpose

from app.forms import RegisterForm  # Ensure RegisterForm is imported

@main.route('/register.html', methods=['GET', 'POST'])
def register():
    form = RegisterForm()  # Create a form instance
    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('main.register'))

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please login.', 'danger')
            return redirect(url_for('main.login'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)  # Hash the password
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now login.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)  # Pass form to template


@main.route('/login.html', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html' , form=form)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('main.login'))

@main.route('/index')
@login_required
def dashboard():
    return f"Welcome {current_user.username}, this is your dashboard."


# trading view
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Order, Transaction
from app import db, socketio

trading = Blueprint('trading', __name__)

@trading.route('/api/place_order', methods=['POST'])
@login_required
def place_order():
    data = request.json
    order = Order(
        user_id=current_user.id,
        crypto_id=data['crypto_id'],
        order_type=data['order_type'],
        quantity=data['quantity'],
        price=data['price'],
        status='pending'
    )
    db.session.add(order)
    db.session.commit()
    
    # Emit order update via WebSocket
    socketio.emit('order_update', order.to_dict())
    return jsonify({'status': 'success'})

# Add crypto API routes
from flask import Blueprint, jsonify
from app.api import CoinGeckoAPI
import functools

# Try to import limiter, but have a fallback if it fails
try:
    from app.cache import limiter
    
    # Define a rate limiting decorator that works with the limiter
    def rate_limit(limit_string):
        def decorator(f):
            @functools.wraps(f)
            @limiter.limit(limit_string)
            def decorated_function(*args, **kwargs):
                return f(*args, **kwargs)
            return decorated_function
        return decorator
        
except Exception:
    # Fallback decorator that does nothing if limiter is not available
    def rate_limit(limit_string):
        def decorator(f):
            @functools.wraps(f)
            def decorated_function(*args, **kwargs):
                return f(*args, **kwargs)
            return decorated_function
        return decorator

crypto_api = Blueprint('crypto_api', __name__, url_prefix='/api/crypto')

@crypto_api.route('/list', methods=['GET'])
@rate_limit("10 per minute")
def get_coins():
    """Get a list of all supported coins"""
    coins = CoinGeckoAPI.get_coin_list()
    return jsonify(coins)

@crypto_api.route('/price/<coin_id>', methods=['GET'])
@rate_limit("30 per minute")
def get_price(coin_id):
    """Get current price of a coin"""
    price = CoinGeckoAPI.get_coin_price(coin_id)
    if not price:
        return jsonify({"error": "Coin not found or API error"}), 404
    return jsonify(price)

@crypto_api.route('/markets', methods=['GET'])
@rate_limit("10 per minute")
def get_markets():
    """Get market data for top coins"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 100, type=int)
    data = CoinGeckoAPI.get_market_data(page=page, per_page=per_page)
    return jsonify(data)