from dash import html, dcc, dash_table
import pandas as pd
from load_data import current_month, current_year, monthsToInt

def dashboard_page(transactions_df):
    # Prepare the transactions data by converting the date to a datetime object
    transactions_df['date'] = pd.to_datetime(transactions_df['date'])
    transactions_df['date_display'] = transactions_df['date'].dt.strftime('%Y-%m-%d')
    transactions_df.sort_values('date', ascending=False, inplace=True)  # Sort by date descending

    return html.Div([
        html.H1("MyFINANCE DASHBOARD", className = 'header'),
        html.Div([
            html.H4("Select Year and Month: "),
            dcc.Dropdown(
                id="slct_year",
                options=[
                    {'label': str(year), 'value': year} for year in range(2000, current_year() + 1)
                ],
                multi=False,
                value=current_year()-1, # Initial value (last year)
                className='dropdownYear'),

            dcc.Dropdown(
                id="slct_month",
                options=[{'label': key, 'value': value} for key, value in monthsToInt().items()],
                multi=False,
                value=current_month(), # Initial value
                className='dropdownMonth'),
        ], className='selectYearandMonth'),

        html.Div([
            html.Div([
                html.Div([
                    # html.H3("Financial Overview", className = 'dataTitle'),
                    html.H3("Net Balance", className='dataTitle'),
                    html.Div([
                        html.P(id='net-balance-output'),
                    ], className='outputBox'),
                    html.H3("Status", className='dataTitle'),
                    html.Div([
                        html.P(id='status-output'),
                    ], className='outputBox')
                ], className= 'financial-overview'),

                html.Div([
                    html.H3("Expense Cateogrization", className='dataTitle'),
                    dcc.Graph(id='expense_categorization_graph', figure={}),
                ], className= 'expense-categorization')
            ], className= 'section3'),

            html.Div([
                html.Div([
                    html.Div([
                        html.H3("Daily Spending Trend", className='dataTitle'),
                        dcc.Graph(id='daily_spending_trend_graph', figure={}),
                    ], className= 'daily-spending-trend'),

                    html.Div([
                        html.H3("Budget vs. Actual Spending Per Category", className='dataTitle'),
                        dcc.Graph(id='budget_vs_actual_spending_graph', figure={}),
                    ], className= 'budget-vs-actual-spending'),
                    
                ], className= 'section4'),
                html.Div([
                    html.H3("Recent Transactions", className = 'dataTitle'),
                    dash_table.DataTable(
                        id='transactions_table',
                        columns=[
                                    {"name": "Date", "id": "date_display"},
                                    {"name": "Category Name", "id": "categoryname"},
                                    {"name": "Amount", "id": "amount"},
                                    {"name": "Description", "id": "description"}
                        ],

                        data=transactions_df.to_dict('records'),
                        style_table={
                            'height': '300px',
                            'overflowY': 'auto'
                        },
                        style_cell={
                            'textAlign': 'left',
                            'color': 'white',
                            'backgroundColor': '#151a28',
                            'border': 'none'
                        },
                        style_header={
                            'backgroundColor': '#222222',
                            'fontWeight': 'bold'
                        }
                    )
                ], className= 'section5')
            ], className= 'dataContainer2')
        ], className='dataContainer')
    ], className='dashboard')