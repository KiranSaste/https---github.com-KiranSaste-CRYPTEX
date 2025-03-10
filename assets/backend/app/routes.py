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
@login_required  # Protects home route, requires login
def home():
    with app.app_context():  
        return render_template("index.html")

@main.route("/login", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect("login.html")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "danger")
    return render_template("login.html", form=form)

@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect("login.html")
        flash("Invalid credentials", "danger")
    return render_template("index.html", form=form)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login.html"))
