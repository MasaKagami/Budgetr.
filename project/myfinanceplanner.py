from dash import Dash, dcc, html, Input, Output
from flask import Flask, session
from datetime import timedelta

# Layouts
from layouts.dashboard_page import dashboard_page
from layouts.spendings_page import spendings_page
from layouts.welcome_page import welcome_page
from layouts.sign_in_page import sign_in_page
from layouts.sign_up_page import sign_up_page
from layouts.settings_page import settings_page
from layouts.support_page import support_page

# Callbacks
from callbacks.dashboard_callback import dashboard_callback
from callbacks.spendings_callback import spendings_callback
from callbacks.sidebar_callback import sidebar_callback
from callbacks.authentication_callback import authentication_callback
from callbacks.settings_callback import settings_callback
from callbacks.support_callback import support_callback
from load_data import load_database, print_dataframes, setup_logging

# Initialize Flask server
server = Flask(__name__)
server.secret_key = 'b5a28e9627732aec641eaddb2f9e3cb954b14748d037232c441f95b5642dc9b9' # Randomly generated secret key; Don't use os.urandom(24) since it changes on every server restart

# Session configurations
server.config['SESSION_PERMANENT'] = True  # Make sessions permanent
server.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Set session lifetime

# Initialize Dash app
app = Dash(__name__, server=server, suppress_callback_exceptions=True) # Suppress callback exceptions ensures callbacks not initially in the app layout are not raised as errors
app.title = 'Budgetr.'

USE_REMOTE_DB = True # Choose database for user authentication and spending records (for testing)
LOGGING = False # Logging for database records and user sessions

setup_logging(server, LOGGING)

transactions_df, categories_df, users_df, monthly_budgets_df, categorical_budgets_df = load_database(USE_REMOTE_DB)
print_dataframes(LOGGING, USE_REMOTE_DB)

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
        dcc.Link(
            html.H1("Budgetr.", className='logo'),
            href='/dashboard',
            className='logo-link'
        ),
        dcc.Link('Dashboard', href='/dashboard', className='tab', id='tab-dashboard'),
        dcc.Link('Record Spendings', href='/record', className='tab', id='tab-record'),
        dcc.Link('Settings', href='/settings', className='tab', id='tab-settings'),
        dcc.Link('Support', href='/support', className='tab', id='tab-support'),
        dcc.Link('Logout', href='/logout', className='tab', id='tab-logout')
    ], style={'display': 'none'}, className='sidebar', id='sidebar',),

    html.Div(id='page-content') # Placeholder to display the page content

], className='background'),

# ------------------------------------------------------------------------------
# Callback to toggle between pages from the sidebar
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')],
    # [State('session', 'data')]
)

def display_page(pathname):
    # print("Session Data: ", session_data)

    if pathname == '/':
        return welcome_page()
    
    elif pathname == '/sign-in':
        if session and session['logged_in']:
            return dcc.Location(href='/dashboard', id='redirect')
        else:
            return sign_in_page()
    
    elif pathname == '/sign-up':
        if session and session['logged_in']:
            return dcc.Location(href='/dashboard', id='redirect')
        else:
            return sign_up_page()
    
    elif pathname == '/dashboard':
        if session and session['logged_in']:
            return dashboard_page(transactions_df)
        else:
            return dcc.Location(href='/sign-in', id='redirect')
        
    elif pathname == '/record':
        if session and session['logged_in']:
            return spendings_page(categories_df, categorical_budgets_df)
        else:
            return dcc.Location(href='/sign-in', id='redirect')
        
    elif pathname == '/settings':
        if session and session['logged_in']:
            return settings_page()
        else:
            return dcc.Location(href='/sign-in', id='redirect')
    
    elif pathname == '/support':
        if session and session['logged_in']:
            return support_page()
        else:
            return dcc.Location(href='/sign-in', id='redirect')

    elif pathname == '/logout':
        session.clear()
        print("User logged out")
        return dcc.Location(href='/', id='redirect') # Redirect to the welcome page after logging out

    else:
        return "404 Page Not Found"
    
# ------------------------------------------------------------------------------
# Callback for sidebar

@app.callback(
    Output('sidebar', 'style'),
    [Input('url', 'pathname')]
)
def toggle_sidebar_visibility(pathname):
    if session and session['logged_in'] and pathname in ['/dashboard', '/record', '/settings', '/support', '/logout']:
        return {'display': 'flex'}  # Show sidebar in the app when logged in
    else:
        return {'display': 'none'}  # Hide sidebar when not logged in

# ------------------------------------------------------------------------------
# Callbacks for every page

authentication_callback(app, use_remote_db=USE_REMOTE_DB)
sidebar_callback(app)
dashboard_callback(app, transactions_df, monthly_budgets_df, categorical_budgets_df)
spendings_callback(app)
settings_callback(app, use_remote_db=USE_REMOTE_DB)
support_callback(app)

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)