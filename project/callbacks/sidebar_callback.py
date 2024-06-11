from dash import Input, Output

def sidebar_callback(app):
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
