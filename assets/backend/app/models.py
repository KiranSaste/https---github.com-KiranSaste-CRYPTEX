from app import db, bcrypt
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Index

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    # Add indexes for frequently queried fields
    __table_args__ = (
        Index('idx_user_username', 'username'),
        Index('idx_user_email', 'email'),
        Index('idx_user_created_at', 'created_at'),
    )

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Cryptocurrency(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    symbol = db.Column(db.String(10), unique=True, nullable=False)

    __table_args__ = (
        Index('idx_crypto_symbol', 'symbol'),
        Index('idx_crypto_name', 'name'),
    )

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    crypto_id = db.Column(db.Integer, db.ForeignKey('cryptocurrency.id'), nullable=False)
    order_type = db.Column(db.Enum('buy', 'sell', name='order_type'), nullable=False)
    price = db.Column(db.Numeric(18, 8), nullable=False)
    quantity = db.Column(db.Numeric(18, 8), nullable=False)
    status = db.Column(db.Enum('pending', 'completed', 'cancelled', name='order_status'), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)

    # Add composite indexes
    __table_args__ = (
        Index('idx_order_user_id', 'user_id'),
        Index('idx_order_status', 'status'),
        Index('idx_order_created_at', 'created_at'),
        Index('idx_order_type', 'order_type'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'crypto_id': self.crypto_id,
            'order_type': self.order_type,
            'price': float(self.price),
            'quantity': float(self.quantity),
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    crypto_id = db.Column(db.Integer, db.ForeignKey('cryptocurrency.id'), nullable=False)
    transaction_type = db.Column(db.Enum('buy', 'sell', name='transaction_type'), nullable=False)
    price = db.Column(db.Numeric(18, 8), nullable=False)
    quantity = db.Column(db.Numeric(18, 8), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)

    __table_args__ = (
        Index('idx_transaction_user_id', 'user_id'),
        Index('idx_transaction_created_at', 'created_at'),
        Index('idx_transaction_type', 'transaction_type'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'crypto_id': self.crypto_id,
            'transaction_type': self.transaction_type,
            'price': float(self.price),
            'quantity': float(self.quantity),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
