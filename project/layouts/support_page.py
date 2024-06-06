from dash import html, dcc

def support_page():
    return html.Div([
        html.Div([
            html.H1('Contact Form'),
            html.Div([    
                html.Div([
                    html.H2('Name'),
                    dcc.Input(
                        id='name-input',
                        type='text',
                        placeholder='your name'
                    ),
                    html.H2('Email'),
                    dcc.Input(
                        id='email-input',
                        type='email',
                        placeholder='your email'
                    ),
                ], className='support-user'),
                html.H2('Message to Creators'),
                html.Textarea(
                    id='message-input',
                    placeholder='Enter your message here...',
                ),
                html.Button('SEND', id='support-send-button', n_clicks=0),
                html.Div(id='support-status')
            ], className='support-page-container')
        ], className='support-page')
    ], className='support')