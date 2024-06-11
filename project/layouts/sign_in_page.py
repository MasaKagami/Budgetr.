from dash import html, dcc

def sign_in_page():
        return html.Div([
                # Hidden divs to store the redirect url
                html.Div(id='signup_status', style={'display': 'none'}),
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
                                html.Img(src="/assets/rocket.png", className='sign-in-illustration', alt='illustration'),
                                html.H1("Sign In", className='sign-in-title'),
                                html.Div([
                                        dcc.Input(id='login_email', type='text', placeholder='Username'),
                                        dcc.Input(id='login_password', type='password', placeholder='Password'),
                                        html.Button('Submit', id='login_button', className='opacity'),
                                        html.Div(id='login_status')
                                ], className='sign-in-top'),

                                html.Div([
                                        dcc.Link('sign up', href='/sign-up', className='sign-in-bottom-text'),
                                        dcc.Link('forgot password?', href='', className='sign-in-bottom-text')
                                ], className='sign-in-bottom')
                        ], className='sign-in')
                ], className='sign-in-container'),
        
        ], className='sign-in-page')