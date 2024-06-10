from dash import Dash, dcc, html
from flask import Flask
from datetime import timedelta

from load_data import setup_logging
from register_callbacks import register_callbacks

# Initialize Flask server
server = Flask(__name__)
server.secret_key = 'b5a28e9627732aec641eaddb2f9e3cb954b14748d037232c441f95b5642dc9b9' # Randomly generated secret key; Don't use os.urandom(24) since it changes on every server restart

# Session configurations
server.config['SESSION_PERMANENT'] = True  # Make sessions permanent
server.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Set session lifetime

# Initialize Dash app
app = Dash(__name__, server=server, suppress_callback_exceptions=True) # Suppress callback exceptions ensures callbacks not initially in the app layout are not raised as errors
app.title = 'Budgetr.'

# Flags for testing
USE_REMOTE_DB = True # Choose database type
LOGGING = False # Logging for database records and user sessions

setup_logging(server, LOGGING)

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

register_callbacks(app, USE_REMOTE_DB)

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)