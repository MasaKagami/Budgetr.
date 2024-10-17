import os
from dash import Dash, dcc, html
from flask import Flask
from datetime import timedelta
from dotenv import load_dotenv
from utils.load_data import setup_logging, cache
from utils.register_callbacks import register_callbacks

# Load environment variables from .env file
load_dotenv()

# Initialize Flask server and set session configurations
server = Flask(__name__)
server.secret_key = os.getenv('SECRET_KEY')
server.config['SESSION_PERMANENT'] = True  # Make sessions permanent
server.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Set session lifetime

# Initialize caching for the server
cache.init_app(server)

# Initialize Dash app
app = Dash(__name__, server=server, suppress_callback_exceptions=True) # Suppress callback exceptions ensures callbacks not initially in the app layout are not raised as errors
app.title = 'Budgetr.'

# Export the Flask server for WSGI server compatibility
application = app.server

# Flags for testing
USE_REMOTE_DB = False # Choose database type
LOGGING = False # Logging for database records and user sessions

setup_logging(server, LOGGING)

# ------------------------------------------------------------------------------
# Main App layout with Sidebar

app.layout = html.Div([
    html.Link(
        href='https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap',
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
        dcc.Link('Manage Finance', href='/record', className='tab', id='tab-record'),
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