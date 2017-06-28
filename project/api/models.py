"""user models module."""

import datetime
import jwt

from flask import current_app
from project import db, bcrypt


class User(db.Model):
    """User model class."""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, email, password, created_at=datetime.datetime.now()):
        """Initialize a user object."""
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BRCYPT_LOG_ROUNDS')
        ).decode()
        self.created_at = created_at

    def encode_auth_token(self, user_id):
        """Generate an auth token."""
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e
