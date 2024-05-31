from dash import html, dcc

def sign_up_page():
    return html.Div([
        # Hidden div to store the redirect url
        html.Div(id='login_redirect_url', style={'display': 'none'}),
        html.Div(id='signup_redirect_url', style={'display': 'none'}),

        html.H2(
            "Sign Up", 
            style={'text-align': 'center'}),
        dcc.Input(
            id='signup_name', 
            type='text', 
            placeholder='Name',
            style={'width': '200px', 'margin': '10px auto', 'display': 'block'}),
        dcc.Input(
            id='signup_email', 
            type='text', 
            placeholder='Email Address', 
            style={'width': '200px', 'margin': '10px auto', 'display': 'block'}),
        dcc.Input(
            id='signup_password', 
            type='password', 
            placeholder='Password', 
            style={'width': '200px', 'margin': '10px auto', 'display': 'block'}),
        dcc.Input(
            id='signup_confirm_password', 
            type='password', 
            placeholder='Confirm Password', 
            style={'width': '200px', 'margin': '10px auto', 'display': 'block'}),
        html.Button(
            'Sign Up', 
            id='signup_button', 
            n_clicks=0, 
            style={'width': '100px', 'margin': '10px auto', 'display': 'block'}),
        html.Div(
            id='signup_status', 
            style={'text-align': 'center', 'color': 'red'}),
        dcc.Link(
            'Login', 
            href='/sign-in', 
            style={'text-align': 'center', 'display': 'block'})
    ])
