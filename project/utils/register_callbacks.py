from callbacks import dashboard_callback, spendings_callback, sidebar_callback, authentication_callback, settings_callback, support_callback

def register_callbacks(app, use_remote_db):
    sidebar_callback(app, use_remote_db) # Holds all the page loading logic
    authentication_callback(app, use_remote_db)
    dashboard_callback(app, use_remote_db)
    spendings_callback(app, use_remote_db)
    settings_callback(app, use_remote_db)
    support_callback(app)