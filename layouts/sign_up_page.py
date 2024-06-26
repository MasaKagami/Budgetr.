from dash import html, dcc

def sign_up_page():
    return html.Div([
        # Hidden div to store the redirect url
        html.Div(id='login_status', style={'display': 'none'}),
        html.Div(id='signout_status', style={'display': 'none'}),
        html.Div(id='delete_status', style={'display': 'none'}),

        html.Div([
            html.Div([
                dcc.Link(
                    html.H1("Budgetr.", className='welcome-logo'),
                    href='/',
                    className='logo-link'
                ),
                html.Div([
                    dcc.Link("Sign In", href='/sign-in', className='sign-in-btn', id='tab-signin'),
                    dcc.Link("Create Your Account", href='/sign-up', className='sign-up-btn', id='tab-signup')
                ], className='navbar-tabs')
            ], className= 'welcome-nav')
        ], className= 'welcome-nav-background'),


        html.Div([
            html.Div([
                html.Img(src="/assets/images/heart.png", className='sign-up-illustration', alt='illustration'),
                html.H1("Sign Up", className='sign-up-title'),
                html.Div([
                    dcc.Input(id='signup_name', type='text', placeholder='Your name'),
                    dcc.Input(id='signup_email', type='text', placeholder='Your email'),
                    dcc.Input(id='signup_password', type='password', placeholder='Password'),
                    dcc.Input(id='signup_confirm_password', type='password', placeholder='Re-enter your password'),
                    html.Div(id='signup_status',style={'text-align': 'center', 'color': 'red'}),
                ], className='sign-up-top'),

                html.Div([
                    html.Button('Register', id='signup_button', className='text'),
                    dcc.Link('already a budgetr? ', href='/sign-in', className='sign-up-bottom-text')
                ], className='sign-up-bottom')
            ], className='sign-up')
        ], className='sign-up-container'),
    ], className='sign-up-page')