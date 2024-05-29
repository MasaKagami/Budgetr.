from dash import Dash, dcc, html, Input, Output

# Layouts
from layouts.dashboard_page import dashboard_page
from layouts.spendings_page import spendings_page
from layouts.welcome_page import welcome_page
from layouts.sign_in_page import sign_in_page
from layouts.sign_up_page import sign_up_page

# Callbacks
from callbacks.dashboard_callback import dashboard_callback
from callbacks.spendings_callback import spendings_callback
from callbacks.sidebar_callback import sidebar_callback
from callbacks.authentication_callback import authentication_callback
from load_data import load_remote_database, load_local_database, print_dataframes

app = Dash(__name__, suppress_callback_exceptions=True)
app.title = 'Budgetr.'

# Use remote database or local database for user authentication and input forms
USE_REMOTE_DB = False

# Load data from the database
if USE_REMOTE_DB:
    transactions_df, categories_df, users_df, monthly_budgets_df, categorical_budgets_df = load_remote_database()
else:
    transactions_df, categories_df, users_df, monthly_budgets_df, categorical_budgets_df = load_local_database()
print_dataframes(transactions_df, categories_df, users_df, monthly_budgets_df, categorical_budgets_df)

# ------------------------------------------------------------------------------
# Main App layout with Sidebar

app.layout = html.Div([
    # Ensures the store is always present in the layout to redirect the user after login or signup
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='login_result'),
    dcc.Store(id='signup_result'),
    
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
        html.H1("Budgetr.", className='logo'),
        dcc.Link('Dashboard', href='/dashboard', className='tab', id='tab-dashboard'),
        dcc.Link('Record Spendings', href='/record', className='tab', id='tab-record'),
        dcc.Link('Settings', href='/settings', className='tab', id='tab-settings'),
        dcc.Link('Support', href='/support', className='tab', id='tab-support'),
        dcc.Link('Logout', href='/logout', className='tab', id='tab-logout')
    ], className='sidebar', id='sidebar'),

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
        return dashboard_page(transactions_df)
    elif pathname == '/record':
        return spendings_page(categories_df, categorical_budgets_df)
    elif pathname == '/':
        return welcome_page()
    elif pathname == '/sign-in':
        return sign_in_page()
    elif pathname == '/sign-up':
        return sign_up_page()
    elif pathname == '/logout':
        return welcome_page()
    else:
        return "404 Page Not Found"
    

# ------------------------------------------------------------------------------
# Callback for sidebar

@app.callback(
    Output('sidebar', 'style'),
    [Input('url', 'pathname')]
)
def toggle_sidebar_visibility(pathname):
    if pathname == '/' or pathname == '/sign_in' or pathname == '/sign_up':
        return {'display': 'none'}  # Hide sidebar on welcome, sign-in, and sign-up pages
    else:
        return {'display': 'flex'}  # Show sidebar as a flexbox on all other pages

# ------------------------------------------------------------------------------
# Callbacks for every page

authentication_callback(app, use_remote_db=USE_REMOTE_DB)
sidebar_callback(app)
dashboard_callback(app, transactions_df, monthly_budgets_df, categorical_budgets_df)
spendings_callback(app)

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)