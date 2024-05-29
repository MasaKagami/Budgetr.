import hashlib
import csv
import os
from sqlalchemy import text
from load_data import create_engine_instance, local_database_url

# Encrypts the password using SHA256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Creates a new user in the local DB
def create_local_user(name, email, password):
    hashed_password = hash_password(password)
    
    # Create the file if it doesn't exist
    if not os.path.isfile(local_database_url()):
        with open(local_database_url(), mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['userid', 'name', 'email', 'password'])
            writer.writerow([1, name, email, hashed_password])
    else:
        # Append the new user to the end of the file
        with open(local_database_url(), mode='a', newline='') as file:
            writer = csv.writer(file)
            user_id = sum(1 for _ in open(local_database_url()))  # Get next user ID
            writer.writerow([user_id, name, email, hashed_password]) # Write the new user to the file

# Validates the user credentials in the local DB
def validate_local_user(email, password):
    hashed_password = hash_password(password)
    
    # Check if the file exists
    if not os.path.isfile(local_database_url()):
        return False
    
    # Check if the user exists in the file
    with open(local_database_url(), mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['email'] == email and row['password'] == hashed_password:
                return True
    return False

# Creates a new user in the remote PostgreSQL database
def create_remote_user(name, email, password):
    engine = create_engine_instance()
    with engine.connect() as conn:
        conn.execute(text('INSERT INTO users (name, email, password) VALUES (:name, :email, :password)'), {'name': name, 'email': email, 'password': hash_password(password)})

# Validates the user credentials in the remote PostgreSQL database
def validate_remote_user(email, password):
    engine = create_engine_instance()
    with engine.connect() as conn:
        result = conn.execute(text('SELECT password FROM users WHERE email=:email'), {'email': email}).fetchone()
        if result and result[0] == hash_password(password):
            return True
    return False