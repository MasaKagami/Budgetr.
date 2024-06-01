from dash import Input, Output, State, no_update
from flask import session
from user_management import create_local_user, validate_local_user, create_remote_user, validate_remote_user

# use-remote-db is a flag to determine whether to use the remote database or the local database
def authentication_callback(app, use_remote_db=False):
    @app.callback(
        Output('login_status', 'children'),
        Output('login_redirect_url', 'children'), # Store the redirect url in a hidden div
        [Input('login_button', 'n_clicks')],
        [State('login_email', 'value'), 
         State('login_password', 'value')]
    )
    
    def login_user(n_clicks, email, password):
        if n_clicks and n_clicks > 0:
            print('Logging in...', email)

            if email and password:
                # Validate the user credentials
                if use_remote_db:
                    userid = validate_remote_user(email, password)
                else:
                    userid = validate_local_user(email, password)

                print('UserID:', userid)
                
                # If the user is valid, log them in
                if userid is not None:
                    session['logged_in'] = True
                    session['user_id'] = userid
                    return 'Login successful', '/dashboard'
                else:
                    return 'Invalid email or password', no_update
            return 'Please enter your email and password', no_update
        return '', None
    
    # ------------------------------------------------------------------------------
    # Callback to create a new user

    @app.callback(
        Output('signup_status', 'children'),
        Output('signup_redirect_url', 'children'), # Store the redirect url in a hidden div
        [Input('signup_button', 'n_clicks')],
        [State('signup_name', 'value'), 
         State('signup_email', 'value'), 
         State('signup_password', 'value'), 
         State('signup_confirm_password', 'value')]
    )
    
    def signup_user(n_clicks, name, email, password, confirm_password):
        if n_clicks and n_clicks > 0:
            print("Signing up...", name, email)
            
            if name and email and password and confirm_password:
                if password != confirm_password:
                    return 'Passwords do not match', None
            
                # Create the new user
                if use_remote_db:
                    userid = create_remote_user(name, email, password)
                else:
                    userid = create_local_user(name, email, password)

                print('UserID:', userid)
                
                # Log in the user automatically after successful signup
                if userid is not None:
                    session['logged_in'] = True
                    session['user_id'] = userid
                    return 'User created successfully', '/dashboard'
                else:
                    return 'Error during account creation', no_update
            return 'Please fill out all fields', no_update
        return '', None
    
    # ------------------------------------------------------------------------------
    # Callback to redirect the user after login or signup using the intermediate data stores
    
    @app.callback(
        Output('url', 'pathname'),
        [Input('login_redirect_url', 'children'),
         Input('signup_redirect_url', 'children')]
    )
    
    def redirect_user(temp_login_url, temp_signup_url):
        if temp_login_url:
            return temp_login_url
        elif temp_signup_url:
            return temp_signup_url
        
        return no_update  # Don't redirect if the intermediate data stores are empty