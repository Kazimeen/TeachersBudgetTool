from flask import Flask, render_template, request, redirect, url_for
from models import db, User
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    name = request.form.get('name')
    annual_income = float(request.form.get('annual_income'))
    current_savings = float(request.form.get('current_savings'))
    trs_contribution = float(request.form.get('trs_contribution'))
    b403_contribution = float(request.form.get('b403_contribution'))
    ira_contribution = float(request.form.get('ira_contribution'))
    monthly_expenses = float(request.form.get('monthly_expenses'))
    years_to_retire = int(request.form.get('years_to_retire'))
    
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

    # Debugging print statements (optional)
    print("Distribution:", distribution)
    print("Investment Growth:", investment_growth)

    return render_template('results.html',
                           name=name,
                           retirement_fund=round(retirement_fund, 2),
                           required_fund=required_fund,
                           recommendation=recommendation,
                           distribution=distribution,
                           investment_growth=investment_growth)

if __name__ == '__main__':
    app.run(debug=True)
