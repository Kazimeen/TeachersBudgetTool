# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'database.db')

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_default_secret_key')  # Replace with a secure key in production

# Initialize Extensions
db.init_app(app)
csrf = CSRFProtect(app)

with app.app_context():
    db.create_all()

# Define WTForm
class BudgetForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    annual_income = FloatField('Annual Income ($)', validators=[DataRequired(), NumberRange(min=0)])
    current_savings = FloatField('Current Savings ($)', validators=[DataRequired(), NumberRange(min=0)])
    trs_contribution = FloatField('TRS Contribution ($)', validators=[DataRequired(), NumberRange(min=0)])
    b403_contribution = FloatField('403(b) Contribution ($)', validators=[DataRequired(), NumberRange(min=0)])
    ira_contribution = FloatField('IRA Contribution ($)', validators=[DataRequired(), NumberRange(min=0)])
    monthly_expenses = FloatField('Monthly Expenses ($)', validators=[DataRequired(), NumberRange(min=0)])
    years_to_retire = IntegerField('Years to Retire', validators=[DataRequired(), NumberRange(min=1)])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = BudgetForm()
    if form.validate_on_submit():
        # Get form data
        name = form.name.data.strip()
        annual_income = form.annual_income.data
        current_savings = form.current_savings.data
        trs_contribution = form.trs_contribution.data
        b403_contribution = form.b403_contribution.data
        ira_contribution = form.ira_contribution.data
        monthly_expenses = form.monthly_expenses.data
        years_to_retire = form.years_to_retire.data

        # Save to database
        user = User(
            name=name,
            annual_income=annual_income,
            current_savings=current_savings,
            trs_contribution=trs_contribution,
            b403_contribution=b403_contribution,
            ira_contribution=ira_contribution,
            monthly_expenses=monthly_expenses,
            years_to_retire=years_to_retire
        )
        db.session.add(user)
        db.session.commit()

        # Perform calculations
        total_contribution = trs_contribution + b403_contribution + ira_contribution
        annual_saving = total_contribution
        future_savings = current_savings
        rate_of_return = 0.05  # 5% annual return

        # Calculate future savings at retirement
        for _ in range(years_to_retire):
            future_savings = future_savings * (1 + rate_of_return) + annual_saving

        retirement_fund = future_savings
        annual_expenses = monthly_expenses * 12
        retirement_years = 25  # Assume 25 years in retirement
        required_fund = annual_expenses * retirement_years

        recommendation = "You are on track for a secure retirement."
        if retirement_fund < required_fund:
            recommendation = "Consider increasing your retirement contributions or extending your working years."

        # Calculate distribution for Pie Chart
        # Categories: TRS, 403(b), IRA, Expenses, Savings
        expenses_annual = annual_income - total_contribution - (monthly_expenses * 12)
        remaining_savings = current_savings  # Assuming current savings are part of remaining
        distribution = {
            'TRS': trs_contribution,
            '403(b)': b403_contribution,
            'IRA': ira_contribution,
            'Expenses': monthly_expenses * 12,
            'Savings': remaining_savings
        }

        # Calculate Investment Growth for Graph
        investment_growth = {}
        increments = [5, 10, 20, 30]
        for increment in increments:
            future = current_savings
            saving = annual_saving
            for _ in range(increment):
                future = future * (1 + rate_of_return) + saving
            investment_growth[increment] = round(future, 2)

        # Redirect to results page
        return render_template('results.html',
                               name=name,
                               retirement_fund=round(retirement_fund, 2),
                               required_fund=required_fund,
                               recommendation=recommendation,
                               distribution=distribution,
                               investment_growth=investment_growth)
    else:
        if request.method == 'POST':
            flash('Please correct the errors in the form.', 'error')

    return render_template('index.html', form=form)

@app.errorhandler(400)
def bad_request(error):
    return render_template('error.html', error_message="Bad Request: " + str(error)), 400

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_message="Internal Server Error: " + str(error)), 500

if __name__ == '__main__':
    app.run(debug=True)
