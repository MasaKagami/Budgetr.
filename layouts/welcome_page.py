from dash import html, dcc

def welcome_page():
    return html.Div([
        html.Div([
            html.Div([
                html.H1("Budgetr.", className='welcome-logo'),
                html.Div([
                    dcc.Link("Sign In", href='/sign-in', className='sign-in-btn', id='tab-signin'),
                    dcc.Link("Create Your Account", href='/sign-up', className='sign-up-btn', id='tab-signup')
                ], className='navbar-tabs')
            ], className= 'welcome-nav')
        ], className= 'welcome-nav-background'),
        
        html.Div([
            html.Div(className='welcome-circle'),

            html.Div(className='wavy-line'),
            html.Div([
                html.Div([
                    html.H1("Visualize Your Finances"),
                    html.P("Gain control over your expenses. Discover clear, visual insights into your spending to help you budget smarter and save more."),
                    dcc.Link("Start Today", href='/sign-up', className='sign-up-btn-big')                          
                ], className='welcome-text'),
                html.Img(src= '/assets/images/lightbulb.png', className='welcome-image')
            ], className= "welcome-content")
        ], className='welcome-content-background'),

        html.Div([  
            html.Div([
                html.Img(src='/assets/images/display.png', className='welcome-display-image'),
                html.Div([
                    html.H1("How Budgetr. works"),
                    html.Div([
                        html.Img(src='/assets/images/rocket.png'),
                        html.Div([
                            html.H2('Get Started Easily'),
                            html.P('Sign up quickly with no credit card required and start managing your finances immediately.')
                        ], className= 'instruction-text-container')
                    ], className='instruction-text-list'),
                    html.Div([
                        html.Img(src='/assets/pencil.png'),
                        html.Div([
                            html.H2('Monitor Your Spending'),
                            html.P('Enter your expenses and view an updated dashboard to help plan and save effectively.')
                        ], className= 'instruction-text-container')
                    ], className='instruction-text-list'),
                    html.Div([
                        html.Img(src='/assets/images/heart.png'),
                        html.Div([
                            html.H2('Achieve Financial Peace'),
                            html.P('Stay informed with real-time updates and visual data, reducing stress and boosting confidence.')
                        ], className= 'instruction-text-container')
                    ], className='instruction-text-list'),

                ], className='instruction-text')
            ], className='welcome-content'),
            html.Div(className='wavy-line-2')
        ], className='welcome-instruction-background'),

        html.Div([
            html.Div(className='wavy-line-5'),
            html.Div([
                html.H2("About The Creators"),
                # html.P("After meeting in Software Engineering Practice, a pivotal course at McGill University, Masa and Shyam quickly discovered their shared passion for technology and innovation. This connection sparked not only a dynamic classroom collaboration but also inspired them to tackle summer projects together, blending their skills to create impactful solutions."),
                html.Div([
                    html.Img(src='/assets/images/masa-border.png', alt='masa picture', className='welcome-creator-image'),
                    
                    html.Div([
                        html.H3('Nagamasa (Masa) Kagami'),
                        html.P('Electrical Engineering Student @ McGill University'),
                        html.Div([
                            dcc.Link('LinkedIn', href='https://www.linkedin.com/in/nagamasa', className='social-link', target='_blank'),
                            dcc.Link('Personal Website', href='https://www.masakagami.com', className='social-link', target='_blank')
                        ], className='links-container')
                    ], className='creator-profile'),
                ], className='creators-container'),
                
                html.Div([
                    html.Div([
                        html.H3('Shyam Desai'),
                        html.P('Software Engineering Student @ McGill University'),
                        html.Div([
                            dcc.Link('LinkedIn', href='https://www.linkedin.com/in/shyamddesai/', className='social-link', target='_blank'),
                            dcc.Link('Personal Website', href='https://github.com/shyamdesai03/', className='social-link', target='_blank')
                        ], className='links-container')
                    ], className='creator-profile'),

                    html.Img(src='/assets/images/shyam-border.png', alt='masa picture', className='welcome-creator-image'),
                ], className='creators-container'),
            ], className='welcome-about'),  
            html.Div(className='wavy-line-3'),
            html.Div(className='wavy-line-4'),
        ], className='welcome-about-background'),

        html.Div([
            html.Div([
                html.Div([
                    html.H1('Budgetr.'),
                    html.H2('Copyright © 2024, Budgetr. All Rights Reserved.')
                ]),
                html.Div([
                    html.P('Masa & Shyam')
                ])
            ], className='welcome-footer')
        ], className='welcome-footer-container')
    ],className='welcome')