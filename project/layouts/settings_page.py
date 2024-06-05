from dash import html, dcc

def settings_page():
    return html.Div([
        # Hidden divs to store the redirect url
        html.Div(id='login_status', style={'display': 'none'}),
        html.Div(id='signup_status', style={'display': 'none'}),
        html.Div(id='signout_status', style={'display': 'none'}),
        
        html.Div([
            html.H1("Settings"),
            html.Div([
                html.H2("Profile"),
                html.Div([
                    html.Label("Name:"),
                    dcc.Input(type='text', id='profile_name', required=True),
                ], className='settings-profile-input'),
                html.Div([
                    html.Label("Email:"),
                    dcc.Input(type='email', id='profile_email', required=True),
                ], className='settings-profile-input'),
                html.Button("Update Profile", id='update_profile_button'),

                html.Div(id='update_profile_status')
            ], className= 'settings-profile'),
            html.Div([
                html.H2("Change Password"),
                html.Div([
                    html.Label("New Password"),
                    dcc.Input(type='password', id='new_password', required=True),
                    html.Label("Confirm New Password"),
                    dcc.Input(type='password', id='confirm_new_password', required=True),
                    html.Button("Update Password", id='update_password_button')
                ]),
                html.Div(id='update_password_status')
            ]),
            html.Div([
                html.H2("Delete Account"),
                html.Button("Delete Account", id='delete_account_button'),
                html.Div(id='confirm_delete_section', style={'display': 'none'}, children=[
                    html.Label("Enter Password to Confirm"),
                    dcc.Input(type='password', id='confirm_password', required=True),
                    html.Button("Confirm Delete", id='confirm_delete_button')
                ]),
                html.Div(id='delete_status')
            ])            
        ], className='settings')

    ], className='settings-page')