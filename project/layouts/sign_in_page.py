from dash import html, dcc

def sign_in_page():
        return html.Div([
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
                        # html.Div([
                                html.Div([
                                        html.Img(src="/assets/login-illustration.png", className='sign-in-illustration', alt='illustration'),
                                        html.H1("Sign In", className='sign-in-title'),
                                        html.Div([
                                                dcc.Input(type='text', placeholder='USERNAME'),
                                                dcc.Input(type='password', placeholder='PASSWORD'),
                                                html.Button('SUBMIT', className='opacity')
                                        ], className='sign-in-top'),

                                        html.Div([
                                                dcc.Link('sign up', href='/sign-up', className='bottom-text'),
                                                dcc.Link('forgot password', href='', className='bottom-text')
                                        ], className='sign-in-bottom')
                                ], className='sign-in')

                        # ], className='sign-in-form'),
                ], className='sign-in-container'),
        
        ], className='sign-in-page')