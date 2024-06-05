from dash import html, dcc

def support_page():
    return html.Div([
        html.H1('Contact Form'),
        html.Div([
            dcc.Input(
                id='name-input',
                type='text',
                placeholder='your name'
            ),
            dcc.Input(
                id='email-input',
                type='email',
                placeholder='your email'
            ),
        ], className='support-user'),
        html.Textarea(
            id='message-input',
            placeholder='Enter your message here...',
        ),
        html.Button('SEND', id='send-button', n_clicks=0),
        html.Div(id='support-status')
        

    ], className='support-page')