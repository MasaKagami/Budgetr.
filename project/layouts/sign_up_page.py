from dash import html, dcc, dash_table

def sign_up_page():
    return html.Div([
        html.H1("Welcome to Budgetr!"),
        html.P("Your personal finance dashboard."),
        dcc.Link("Sign In", href='/sign_in', className='button'),
        dcc.Link("Sign Up", href='/sign_up', className='button')
    ])