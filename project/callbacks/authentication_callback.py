from dash import Input, Output, State
from user_management import create_local_user, validate_local_user, create_remote_user, validate_remote_user

# use-remote-db is a flag to determine whether to use the remote database or the local database
def authentication_callback(app, use_remote_db=False):
    @app.callback(
        Output('login_status', 'children'),
        Output('login_result', 'data'), # Store the result in an intermediate data store used in another callback to redirect the user
        [Input('login_button', 'n_clicks')],
        [State('login_email', 'value'), 
         State('login_password', 'value')]
    )
    
    def login_user(n_clicks, email, password):
        if n_clicks > 0:
            if email and password:
                if use_remote_db:
                    if validate_remote_user(email, password):
                        return 'Login successful', 'success'
                    else:
                        return 'Invalid email or password', 'failure'
                else:
                    if validate_local_user(email, password):
                        return 'Login successful', 'success'
                    else:
                        return 'Invalid email or password', 'failure'
            return 'Please enter your email and password', 'failure'
        return '', None
    
    # ------------------------------------------------------------------------------
    # Callback to create a new user

    @app.callback(
        Output('signup_status', 'children'),
        Output('signup_result', 'data'), # Store the result in an intermediate data store used in another callback to redirect the user
        [Input('signup_button', 'n_clicks')],
        [State('signup_name', 'value'), 
         State('signup_email', 'value'), 
         State('signup_password', 'value'), 
         State('signup_confirm_password', 'value')]
    )
    
    def signup_user(n_clicks, name, email, password, confirm_password):
        if n_clicks > 0:
            print(f"Signup attempt with values: name={name}, email={email}, password={password}, confirm_password={confirm_password}")
            if password != confirm_password:
                return 'Passwords do not match', 'failure'
            
            if name and email and password:
                if use_remote_db:
                    create_remote_user(name, email, password)
                else:
                    create_local_user(name, email, password)
                return 'User created successfully', 'success'
            print(f"Signup values missing: name={name}, email={email}, password={password}")
            return 'Please fill out all fields', 'failure'
        return '', None
    
    # ------------------------------------------------------------------------------
    # Callback to redirect the user after login or signup
    
    @app.callback(
        Output('url', 'pathname'),
        [Input('login_result', 'data'), 
         Input('signup_result', 'data')]
    )
    
    def redirect_user(login_result, signup_result):
        if login_result == 'success' or signup_result == 'success':
            return '/dashboard'
        elif login_result == 'failure':
            return '/sign-in'
        elif signup_result == 'failure':
            return '/sign-up'
    # ------------------------------------------------------------------------------
    