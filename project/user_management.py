import hashlib
import pandas as pd
from sqlalchemy import text
from load_data import create_engine_instance, local_database_url

# Encrypts the password using SHA256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Creates a new user in the local DB
def create_local_user(name, email, password):
    users_df = pd.read_csv(local_database_url())
    new_user = {'userid': users_df['userid'].max() + 1, 'name': name, 'email': email, 'password': hash_password(password)}
    users_df = users_df.append(new_user, ignore_index=True)
    users_df.to_csv(local_database_url(), index=False)

# Validates the user credentials in the local DB; Returns the user ID if valid
def validate_local_user(email, password):
    users_df = pd.read_csv('../localdb/users.csv')
    user = users_df[(users_df['email'] == email) & (users_df['password'] == hash_password(password))]
    if not user.empty:
        return int(user.iloc[0]['userid'])  # Ensure this is a standard Python integer
    return None

# Creates a new user in the remote PostgreSQL database
def create_remote_user(name, email, password):
    engine = create_engine_instance()
    with engine.connect() as conn:
        conn.execute(text('INSERT INTO users (name, email, password) VALUES (:name, :email, :password)'), {'name': name, 'email': email, 'password': hash_password(password)})

# Validates the user credentials in the remote PSQL database; Returns the user ID if valid
def validate_remote_user(email, password):
    engine = create_engine_instance()
    with engine.connect() as conn:
        result = conn.execute(text('SELECT userid, password FROM users WHERE email=:email'), {'email': email}).fetchone()
        if result and result[1] == hash_password(password):
            return result[0]
    return None