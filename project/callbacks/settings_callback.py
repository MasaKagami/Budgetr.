from dash import Output, Input, State
from flask import session
from sqlalchemy import text
from user_management import hash_password, validate_local_user, validate_remote_user, local_users_url
from load_data import global_engine, load_local_users

def settings_callback(app, use_remote_db=False):
    @app.callback(
        Output('update_profile_status', 'children'),
        [Input('update_profile_button', 'n_clicks')],
        [State('profile_name', 'value'), 
         State('profile_email', 'value')]
    )

    def update_profile(n_clicks, name, email):
        if n_clicks and n_clicks > 0:
            if name and email:
                userid = session.get('user_id')
                
                if userid:
                    # Update the user profile
                    if use_remote_db:
                        update_remote_user_profile(userid, name, email)
                    else:
                        update_local_user_profile(userid, name, email)
                    return 'Profile updated successfully'
                else:
                    return 'User not logged in'
            return 'Please fill out all fields'
        return ''

    # ------------------------------------------------------------------------------
    # Callback to update user password

    @app.callback(
        Output('update_password_status', 'children'),
        [Input('update_password_button', 'n_clicks')],
        [State('new_password', 'value'), 
         State('confirm_new_password', 'value')]
    )

    def update_password(n_clicks, new_password, confirm_new_password):
        if n_clicks and n_clicks > 0:
            if new_password and confirm_new_password:
                if new_password != confirm_new_password:
                    return 'Passwords do not match'
                userid = session.get('user_id')
                if userid:
                    # Update the user password
                    if use_remote_db:
                        update_remote_user_password(userid, new_password)
                    else:
                        update_local_user_password(userid, new_password)
                    return 'Password updated successfully'
                else:
                    return 'User not logged in'
            return 'Please fill out all fields'
        return ''

    # ------------------------------------------------------------------------------
    # Callback to show confirm delete account section

    @app.callback(
        Output('confirm_delete_section', 'style'),
        [Input('delete_account_button', 'n_clicks')]
    )

    def show_confirm_delete(n_clicks):
        if n_clicks and n_clicks > 0:
            return {'display': 'block'}
        return {'display': 'none'}

    # ------------------------------------------------------------------------------
    # Callback to delete user account

    @app.callback(
        Output('delete_status', 'children'),
        [Input('confirm_delete_button', 'n_clicks')],
        [State('confirm_password', 'value')]
    )
    
    def delete_account(n_clicks, password):
        if n_clicks and n_clicks > 0:
            if password:
                userid = session.get('user_id')
                email = session.get('user_email')

                if userid:
                    # Validate the user password
                    if use_remote_db:
                        valid_user = validate_remote_user(email, password)
                    else:
                        valid_user = validate_local_user(email, password)

                    # If the password is valid, delete the account
                    if valid_user is not None:
                        if use_remote_db:
                            delete_remote_user(userid)
                        else:
                            delete_local_user(userid)

                        session.clear()
                        return 'Account deleted successfully'
                    else:
                        return 'Invalid password'
                return 'User not logged in'
            return 'Please enter your password'
        return ''

    # ------------------------------------------------------------------------------
    # Update User Profile Functions

    def update_local_user_profile(userid, name, email):
        users_df = load_local_users()
        users_df.loc[users_df['userid'] == userid, ['name', 'email']] = [name, email]
        users_df.to_csv(local_users_url(), index=False)

    def update_remote_user_profile(userid, name, email):
        with global_engine.begin() as conn:
            conn.execute(text('UPDATE users SET name=:name, email=:email WHERE userid=:userid'), {'name': name, 'email': email, 'userid': userid})

    # ------------------------------------------------------------------------------
    # Update User Password Functions

    def update_local_user_password(userid, password):
        users_df = load_local_users()
        users_df.loc[users_df['userid'] == userid, 'password'] = hash_password(password)
        users_df.to_csv(local_users_url(), index=False)

    def update_remote_user_password(userid, password):
        with global_engine.begin() as conn:
            conn.execute(text('UPDATE users SET password=:password WHERE userid=:userid'), {'password': hash_password(password), 'userid': userid})

    # ------------------------------------------------------------------------------
    # Delete User Functions

    def delete_local_user(userid):
        users_df = load_local_users()
        users_df = users_df[users_df['userid'] != userid]
        users_df.to_csv(local_users_url(), index=False)

    def delete_remote_user(userid):
        with global_engine.begin() as conn:
            conn.execute(text('DELETE FROM users WHERE userid=:userid'), {'userid': userid})