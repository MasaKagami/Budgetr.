from dash import html, dcc

def sign_up_page():
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

        # html.Div([
        #     html.Div([
        #         html.H2(
        #             "Sign Up", 
        #             ),
        #         dcc.Input(
        #             id='signup_name', 
        #             type='text', 
        #             placeholder='Name',
        #             ),
        #         dcc.Input(
        #             id='signup_email', 
        #             type='text', 
        #             placeholder='Email Address', 
        #             ),
        #         dcc.Input(
        #             id='signup_password', 
        #             type='password', 
        #             placeholder='Password', 
        #             ),
        #         dcc.Input(
        #             id='signup_confirm_password', 
        #             type='password', 
        #             placeholder='Confirm Password', 
        #             ),
        #         html.Button(
        #             'Sign Up', 
        #             id='signup_button', 
        #             n_clicks=0, 
        #             ),
        #         html.Div(
        #             id='signup_status', 
        #             ),
        #         dcc.Link(
        #             'Login', 
        #             href='/sign-in', 
        #             )
        #     ], className='sign-up-text')
        # ], className='sign-up-form'),

        # html.Section(className='container', children=[
        #     html.Div(className='login-container', children=[
        #         html.Div(className='circle circle-one'),
        #         html.Div(className='form-container', children=[
        #             html.Img(src="https://raw.githubusercontent.com/hicodersofficial/glassmorphism-login-form/master/assets/illustration.png", className='illustration', alt="illustration"),
        #             html.H1("LOGIN", className='opacity'),
        #             html.Div(children=[
        #                 dcc.Input(type='text', placeholder='USERNAME'),
        #                 dcc.Input(type='password', placeholder='PASSWORD'),
        #                 html.Button('SUBMIT', className='opacity')
        #             ], style={'display': 'flex', 'flexDirection': 'column'}),
        #             html.Div(className='register-forget opacity', children=[
        #                 dcc.Link('REGISTER', href=''),
        #                 dcc.Link('FORGOT PASSWORD', href='')
        #             ])
        #         ]),
        #         html.Div(className='circle circle-two')
        #     ]),
        #     html.Div(className='theme-btn-container')
        # ])

        # html.Div([
        #     html.Div([
        #         html.Div([
        #             dcc.Input(type='text', placeholder='USERNAME'),
        #             dcc.Input(type='password', placeholder='PASSWORD'),
        #             html.Button('SUBMIT', className='opacity')
        #         ], className='sign-up-top'),

        #         html.Div([
        #             dcc.Link('sign up', href='/sign-up'),
        #             dcc.Link('forgot password', href='')
        #         ], className='sign-up-bottom')

        #     ], className='sign-up')
        # ], className='sign-up-form')


    ], className='sign-up-page')
