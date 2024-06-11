from dash import dcc, Input, Output
from flask import session
from layouts import dashboard_page, spendings_page, welcome_page, sign_in_page, sign_up_page, settings_page, support_page
from utils.load_data import cache

def sidebar_callback(app, use_remote_db=False):
    # Callback to toggle between pages from the sidebar
    @app.callback(
        Output('page-content', 'children'),
        [Input('url', 'pathname')],
    )

    @cache.memoize()
    def display_page(pathname):
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
                return dashboard_page(use_remote_db)
            else:
                return dcc.Location(href='/sign-in', id='redirect')
            
        elif pathname == '/record':
            if session and session['logged_in']:
                return spendings_page(use_remote_db)
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