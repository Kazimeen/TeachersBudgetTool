# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    annual_income = db.Column(db.Float, nullable=False)
    current_savings = db.Column(db.Float, nullable=False)
    trs_contribution = db.Column(db.Float, nullable=False)
    b403_contribution = db.Column(db.Float, nullable=False)
    ira_contribution = db.Column(db.Float, nullable=False)
    monthly_expenses = db.Column(db.Float, nullable=False)
    years_to_retire = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'
