from dash import html, dcc

def sign_in_page():
    return html.Div([
        html.H2("Login"),
        dcc.Input(
                id='login_username', 
                type='text', 
                placeholder='Username', 
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