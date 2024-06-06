from dash import html, dcc

def settings_page():
    return html.Div([
        # Hidden divs to store the redirect url
        html.Div(id='login_status', style={'display': 'none'}),
        html.Div(id='signup_status', style={'display': 'none'}),
        html.Div(id='signout_status', style={'display': 'none'}),
        html.Div([
            html.H1("Settings"),
            html.P("Adjust your preferences and manage your account settings here. Don't forget to save your changes"),
            html.Div([
                html.Div([
                    html.H2("Profile"),
                    html.H3("Name"),
                    dcc.Input(type='text', id='profile_name', placeholder='your name' ,required=True),
                    html.H3("Email"),
                    dcc.Input(type='email', id='profile_email', placeholder='your email', required=True),
                    html.Button("UPDATE PROFILE", id='update_profile_button'),

                    html.Div(id='update_profile_status')
                ], className= 'settings-profile'),
                
                html.Div(className='settings-border-lines'),

                html.Div([
                    html.H2("Change Password"),
                    html.H3("New Password"),
                    dcc.Input(type='password', id='new_password', placeholder='your new password', required=True),
                    html.H3("Confirm New Password"),
                    dcc.Input(type='password', id='confirm_new_password', placeholder='re-type password', required=True),
                    html.Button("UPDATE PASSWORD", id='update_password_button'),

                    html.Div(id='update_password_status')
                ], className='settings-password'),

                html.Div(className='settings-border-lines'),

                html.Div([
                    html.H2("Delete Account"),
                    html.Button("Delete Account", id='delete_account_button'),
                    html.Div(id='confirm_delete_section', style={'display': 'none'}, children=[
                        html.H3("Enter Password to Confirm"),
                        dcc.Input(type='password', id='confirm_password', required=True),
                        html.Button("Confirm Delete", id='confirm_delete_button')
                    ]),
                    html.Div(id='delete_status'),
                    html.Img(src="/assets/exclamation.png", alt='exclamation mark', className='settings-art')
                ], className='settings-delete')
            ],className='settings-container')
        ], className='settings')

    ], className='settings-page')