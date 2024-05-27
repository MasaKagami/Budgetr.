from dash import html, dcc

def welcome_page():
    return html.Div([
        html.Div([
            html.Div([
                html.H1("Budgetr.", className='welcome-logo'),
                dcc.Link("Sign In", href='/sign_in', className='sign-in-btn'),
                dcc.Link("Create Your Account", href='/sign_up', className='sign-up-btn')    
            ], className= 'welcome-nav')
        ], className= 'welcome-nav-background'),
        html.Div([
            html.Div([
                html.Div([
                    html.H1("Visualize Your Finances"),
                    html.P("Gain control over your expenses. Discover clear, visual insights into your spending to help you budget smarter and save more. - Yuh"),
                    dcc.Link("Start Today", href='/sign_up', className='sign-up-btn')                          
                ], className='welcome-text'),

                html.Div([
                    html.Img(src= '/assets/Solid_white.png')
                ], className='welcome-image')
            ], className= "welcome-content")
        ], className='welcome-content-background')
            

    ],className='welcome')