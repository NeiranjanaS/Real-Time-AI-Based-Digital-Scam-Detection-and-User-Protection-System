from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(db.String(120), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ScanHistory(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)

    scan_type = db.Column(db.String(50))

    input_data = db.Column(db.Text)

    prediction = db.Column(db.String(50))

    confidence = db.Column(db.Float)

    reason = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)