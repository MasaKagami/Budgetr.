from dash import html, dcc

def support_page():
    return html.Div([
        html.Div([
            html.H1('Contact Form'),
            html.P('Please fill out the form below to contact us. We will get back to you as soon as possible'),
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
                html.H2('Message to Creator'),
                html.Textarea(
                    id='message-input',
                    placeholder='Enter your message here'
                ),
                html.Img(src="/assets/question.png", alt='question mark', className='suppport-art'),
                html.Button('SEND', id='send-button', n_clicks=0),
                html.Div(id='support-status')
            ], className='support-page-container')
        ], className='support-page')
    ], className='support')