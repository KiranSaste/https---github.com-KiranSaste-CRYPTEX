from flask import Flask, render_template, redirect, url_for, flash, request, session, Blueprint

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['SECRET_KEY'] = 'supersecretkey'

# Create a blueprint for main routes
main = Blueprint('main', __name__)

# Hard-coded test user for demo
TEST_USER = {
    'username': 'test',
    'password': 'password123',
    'email': 'test@example.com'
}

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/login.html', methods=['GET', 'POST'])
def login():
    username_error = None
    password_error = None
    
    # Clear previous flash messages
    session.pop('_flashes', None)
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple fixed user authentication
        if username == TEST_USER['username'] and password == TEST_USER['password']:
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            # Only show one generic error message
            flash('Invalid username or password!', 'danger')
            
            # Store detailed errors for form display
            if username != TEST_USER['username']:
                username_error = "Invalid username"
            if password != TEST_USER['password']:
                password_error = "Invalid password"
    
    return render_template('login.html', 
                          username_error=username_error, 
                          password_error=password_error, 
                          test_username=TEST_USER['username'],
                          test_password=TEST_USER['password'])

@main.route('/register.html', methods=['GET', 'POST'])
def register():
    # Clear previous flash messages
    session.pop('_flashes', None)
    
    username_error = None
    password_error = None
    email_error = None
    confirm_password_error = None
    
    if request.method == 'POST':
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html', 
                          username_error=username_error,
                          password_error=password_error,
                          email_error=email_error,
                          confirm_password_error=confirm_password_error)

@main.route('/logout')
def logout():
    # Clear previous flash messages
    session.pop('_flashes', None)
    
    # Check if user is logged in
    was_logged_in = 'user' in session
    
    # Clear user session
    if was_logged_in:
        username = session.get('user', 'User')
        session.pop('user', None)
        flash(f'You have been logged out, {username}!', 'info')
    
    # Render logout confirmation page
    return render_template('logout.html')

@main.route('/market.html')
def market():
    if 'user' not in session:
        flash('Please log in to view this page', 'warning')
        return redirect(url_for('main.login'))
    return render_template('market.html')

@main.route('/trade.html')
def trade():
    if 'user' not in session:
        flash('Please log in to view this page', 'warning')
        return redirect(url_for('main.login'))
    return render_template('trade.html')

@main.route('/wallet.html')
def wallet():
    if 'user' not in session:
        flash('Please log in to view this page', 'warning')
        return redirect(url_for('main.login'))
    return render_template('wallet.html')

@main.route('/blog.html')
def blog():
    return render_template('blog.html')

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

# Register the blueprint with the app
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)