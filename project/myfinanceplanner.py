from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px
from datetime import datetime
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
from turtle import width

from layouts.dashboard_page import dashboard_page
from layouts.spendings_page import spendings_page
from callbacks.dashboard_callback import dashboard_callback
from callbacks.spendings_callback import spendings_callback

app = Dash(__name__)
app.title = 'myfinanceplanner'

# -- Import and clean data (importing csv into pandas)
def load_data():
    # Connection setup
    DATABASE_URL = "postgresql://postgresql_finance_user:Xda6CRIftQmupM1vnXit1fnbKIfcfLhc@dpg-cp1p0hud3nmc73b8v0qg-a.ohio-postgres.render.com:5432/postgresql_finance"

    # Creating an SQLAlchemy engine
    engine = create_engine(DATABASE_URL)

    # Load transactions
    transactions_query = "SELECT * FROM Transactions;"
    transactions_df = pd.read_sql(transactions_query, engine, parse_dates=['date'])

    # Load monthly budgets
    monthly_budgets_query = "SELECT * FROM MonthlyBudgets;"
    monthly_budgets_df = pd.read_sql(monthly_budgets_query, engine)

    # Load categorical budgets
    categorical_budgets_query = "SELECT * FROM CategoricalBudgets;"
    categorical_budgets_df = pd.read_sql(categorical_budgets_query, engine)

    # Load categories
    categories_df_query = "SELECT * FROM Categories;"
    categories_df = pd.read_sql(categories_df_query, engine)
    
    # Load users
    users_df_query = "SELECT * FROM Users;"
    users_df = pd.read_sql(users_df_query, engine)
    
    # Close the connection
    engine.dispose()

    return transactions_df, categories_df, users_df, monthly_budgets_df, categorical_budgets_df

def load_local_database():
    transactions_df = pd.read_csv('../localdb/transactions.csv', parse_dates=['date'])
    categories_df = pd.read_csv('../localdb/categories.csv')
    users_df = pd.read_csv('../localdb/users.csv')
    monthly_budgets_df = pd.read_csv('../localdb/monthlybudgets.csv', parse_dates=['budgetmonth'])
    categorical_budgets_df = pd.read_csv('../localdb/categoricalbudgets.csv')

    return transactions_df, categories_df, users_df, monthly_budgets_df, categorical_budgets_df

# Loading data
# transactions_df, categories_df, users_df, monthly_budgets_df, categorical_budgets_df = load_local_database()
transactions_df, categories_df, users_df, monthly_budgets_df, categorical_budgets_df = load_data()

print('\nTRANSACTIONS DB\n', transactions_df[:5])
print('CATEGORIES DB\n', categories_df[:5])
print('USERS DB\n', users_df[:5])
print('MONTHLY BUDGETS DB\n', monthly_budgets_df[:5])
print('CATEGORICAL BUDGETS DB\n', categorical_budgets_df[:5])

# Prepare the transactions DataFrame for the dashboard, convert date to datetime object
transactions_df['date'] = pd.to_datetime(transactions_df['date'])
transactions_df['date_display'] = transactions_df['date'].dt.strftime('%Y-%m-%d')
transactions_df.sort_values('date', ascending=False, inplace=True)  # Sort by date descending

# Dictionary to convert month names to integer values
monthsToInt = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}

# Reverse the dictionary to convert the integers to month names
IntToMonths = {v: k for k, v in monthsToInt.items()} 

# Get the current month and year
current_month = datetime.now().month
current_year = datetime.now().year

# ------------------------------------------------------------------------------
# Main App layout with Sidebar

app.layout = html.Div([
    html.Link(
        href='https://fonts.googleapis.com/css2?family=Lexend:wght@100..900&display=swap',
        rel='stylesheet'
    ),
    html.Link(
        href='https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap',
        rel='stylesheet'
    ),

    dcc.Location(id='url', refresh=False), 
    html.Div([
        html.H1("Budgetr", className='logo'),
        # html.Img(src='/assets/Solid_white.png', className='logo'),
        dcc.Link('Dashboard', href='/dashboard', className='tab', id='tab-dashboard'),
        dcc.Link('Record Spendings', href='/record', className='tab', id='tab-record'),
        dcc.Link('Settings', href='/settings', className='tab', id='tab-settings'),
        dcc.Link('Support', href='/support', className='tab', id='tab-support'),
        dcc.Link('Logout', href='/logout', className='tab', id='tab-logout')
    ], className='sidebar'),

    html.Div(id='page-content') # Placeholder to display the page content

], className='background'),

# ------------------------------------------------------------------------------
# Callback to toggle between pages from the sidebar
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)

def display_page(pathname):
    if pathname == '/dashboard':
        return dashboard_page(transactions_df, monthsToInt)
    elif pathname == '/record':
        return spendings_page(categories_df, categorical_budgets_df, monthsToInt)
    else:
        return "404 Page Not Found"

# ------------------------------------------------------------------------------
# Callback for active state of tabs
@app.callback(
    [Output('tab-dashboard', 'className'),
     Output('tab-record', 'className'),
     Output('tab-settings', 'className'),
     Output('tab-support', 'className'),
     Output('tab-logout', 'className')],    
    [Input('url', 'pathname')]
)

def update_tab_active(pathname):
    # Default class for all tabs
    default_class = 'tab'

    # Active class for the currently selected tab
    active_class = 'tab active'
    return [
        active_class if pathname == '/dashboard' else default_class,
        active_class if pathname == '/record' else default_class,
        active_class if pathname == '/settings' else default_class,
        active_class if pathname == '/support' else default_class,
        active_class if pathname == '/logout' else default_class,
    ]

dashboard_callback(app, transactions_df, monthly_budgets_df, categorical_budgets_df)
spendings_callback(app, transactions_df, categories_df, monthly_budgets_df, categorical_budgets_df)


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)