from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    annual_income = db.Column(db.Float)
    current_savings = db.Column(db.Float)
    trs_contribution = db.Column(db.Float)
    b403_contribution = db.Column(db.Float)
    ira_contribution = db.Column(db.Float)
    monthly_expenses = db.Column(db.Float)
    years_to_retire = db.Column(db.Integer)
