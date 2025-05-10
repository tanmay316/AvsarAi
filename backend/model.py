from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # Profile-related fields
    full_name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    phone_number = db.Column(db.String(20))
    resume = db.Column(db.String(150), nullable=True)
    gender = db.Column(db.String(10))
    education = db.Column(db.Text)
    work_experience = db.Column(db.Text)
    skills = db.Column(db.Text)
    linkedin = db.Column(db.String(200))
    portfolio = db.Column(db.String(200))
    github = db.Column(db.String(200))
    projects = db.Column(db.Text)
    disabilities = db.Column(db.Text)
    credentials = db.Column(db.Text)  # Store as JSON string
    is_active = db.Column(db.Boolean, default=True)  # Required by Flask-Login

    def __repr__(self):
        return f"<User {self.username}>"

class JobApplication(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # Using a string for UUID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_url = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default="processing")
    result = db.Column(db.Text, nullable=True)
    error = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user = db.relationship('User', backref=db.backref('applications', lazy=True))

    def __repr__(self):
        return f"<JobApplication {self.id} for User {self.user_id}>"