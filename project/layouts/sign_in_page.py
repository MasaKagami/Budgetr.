from dash import html, dcc

def sign_in_page():
    return html.Div([
        # Hidden divs to store the redirect url
        html.Div(id='login_redirect_url', style={'display': 'none'}),
        html.Div(id='signup_redirect_url', style={'display': 'none'}),

        html.H2(
                "Login",
                style={'text-align': 'center'}),
        dcc.Input(
                id='login_email', 
                type='text', 
                placeholder='Email Address', 
                style={'width': '200px', 'margin': '10px auto', 'display': 'block'}),
        dcc.Input(
                id='login_password', 
                type='password', 
                placeholder='Password', 
                style={'width': '200px', 'margin': '10px auto', 'display': 'block'}),
        html.Button(
                'Login', 
                id='login_button', 
                n_clicks=0, 
                style={'width': '100px', 'margin': '10px auto', 'display': 'block'}),
        html.Div(
                id='login_status', 
                style={'text-align': 'center', 'color': 'red'}),
        dcc.Link(
                'Sign Up', 
                href='/sign-up',
                style={'text-align': 'center', 'display': 'block'})
    ])