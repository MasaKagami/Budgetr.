from dash import Input, Output, State, no_update
from flask import session
from user_management import create_local_user, validate_local_user, create_remote_user, validate_remote_user, delete_local_user, delete_remote_user

# use-remote-db is a flag to determine whether to use the remote database or the local database
def authentication_callback(app, use_remote_db=False):
    @app.callback(
        Output('login_status', 'children'),
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
                    session['user_email'] = email
                    return 'Login successful'
                else:
                    return 'Invalid email or password'
            return 'Please enter your email and password'
        return ''
    
    # ------------------------------------------------------------------------------
    # Callback to create a new user

    @app.callback(
        Output('signup_status', 'children'),
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
                    return 'Passwords do not match'
            
                # Create the new user
                if use_remote_db:
                    userid = create_remote_user(name, email, password)
                else:
                    userid = create_local_user(name, email, password)
                print('UserID:', userid)
                
                # Login the user automatically after signing up
                login_user(1, email, password)
                return "Account created successfully"
            return 'Please fill out all fields'
        return ''
    
    # ------------------------------------------------------------------------------
    # Callback to handle logout and clear session

    @app.callback(
        Output('signout_status', 'children'),
        [Input('logout_button', 'n_clicks')]
    )
    
    def logout_user(n_clicks):
        if n_clicks and n_clicks > 0:
            session.clear()
            print("User logged out")
            return 'Logout successful'
        
        return no_update  # No redirection if no logout action
    
    # ------------------------------------------------------------------------------
    # Callback to redirect the user after login, signup, or logout

    @app.callback(
        Output('url', 'pathname'),
        Output('local-store', 'data'),
        [Input('login_status', 'children'),
         Input('signup_status', 'children'),
         Input('signout_status', 'children'),
         Input('delete_status', 'children')]
    )
    
    def redirect_user(login_status, signup_status, signout_status, delete_status):
        print(login_status, signup_status, signout_status)
        if login_status == 'Login successful':
            session_data = {
                'logged_in': True, 
                'user_id': session.get('user_id'),
                'user_email': session.get('user_email')
            }
            return '/dashboard', session_data

        elif signup_status == 'Account created successfully':
            session_data = {
                'logged_in': True, 
                'user_id': session.get('user_id'),
                'user_email': session.get('user_email')
            }
            return '/dashboard', session_data

        elif signout_status == 'Logout successful' or delete_status == 'Account deleted successfully':
            session_data = {
                'logged_in': False, 
                'user_id': None,
                'user_email': None
            }
            return '/', session_data
        
        return no_update, no_update  # Don't redirect if the user is not logging in or signing up