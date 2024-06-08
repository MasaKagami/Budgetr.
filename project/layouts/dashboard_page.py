from dash import html, dcc, dash_table
import pandas as pd
from load_data import current_month, current_year, monthsToInt, load_transactions

def dashboard_page():
    transactions_df = load_transactions()

    # Prepare the transactions data by converting the date to a datetime object
    transactions_df['date'] = pd.to_datetime(transactions_df['date'])
    transactions_df['date_display'] = transactions_df['date'].dt.strftime('%Y-%m-%d')
    transactions_df.sort_values('date', ascending=False, inplace=True)  # Sort by date descending

    return html.Div([

        html.Div([
            html.Div([
                html.H1("Year and Month"),
                html.Div([
                    html.H2('select year:'),
                    dcc.Dropdown(
                        id="slct_year",
                        options=[
                            {'label': str(year), 'value': year} for year in range(2023 , (current_year()+1)+1)
                        ],
                        multi=False,
                        value=current_year()-1, # Initial value (last year)
                        placeholder="select year",
                        className='dashboard--input',
                    ),
                ], className= 'dashboard-date-format-year'),
                html.Div([
                    html.H2('select month:'),
                    dcc.Dropdown(
                        id="slct_month",
                        options=[{'label': key, 'value': value} for key, value in monthsToInt().items()],
                        multi=False,
                        value=current_month(), # Initial value
                        placeholder="select month",
                        className='dashboard--input',
                    )
                ], className = 'dashboard-date-format-month')
            ], className='dashboard-date-input'),

            html.Div([
                html.H1("Net Balance"),
                html.P(id='net-balance-output', className='dashboard-outputBox'),
                html.H1("Performance"),
                html.P(id='status-output', className='dashboard-outputBox')
            ], className= 'dashboard-net-balance'),

            html.Div([
                html.H1("Expense Categorization"),
                dcc.Graph(id='expense_categorization_graph', figure={}),
            ], className= 'dashboard-categorization')
        ], className= 'dashboard-left-side'),


        html.Div([
            html.Div([
                html.Div([
                    html.H1("Daily Spending Trend"),
                    dcc.Graph(id='daily_spending_trend_graph', figure={}),
                ], className= 'daily-spending-trend'),

                html.Div([
                    html.H1("Budget vs. Spending Per Category"),
                    dcc.Graph(id='budget_vs_actual_spending_graph', figure={}),
                ], className= 'budget-vs-actual-spending'),
                
            ], className= 'dashboard-right-top'),

            html.Div([
                html.H1("Recent Transactions"),
                dash_table.DataTable(
                    id='transactions_table',
                    columns=[
                                {"name": "Date", "id": "date_display"},
                                {"name": "Category Name", "id": "categoryname"},
                                {"name": "Amount", "id": "amount"},
                                {"name": "Description", "id": "description"}
                    ],

                    data=transactions_df.to_dict('records'),
                )
            ], className= 'dashboard-right-bottom')
            
        ], className= 'dashboard-right-side')
    ], className='dashboard')