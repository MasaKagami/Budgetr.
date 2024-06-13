import os
from dotenv import load_dotenv
import logging
import pandas as pd
from sqlalchemy import MetaData, Table, create_engine, func, select, update
from datetime import datetime
from flask import session
import numpy as np
from flask_caching import Cache

# Load environment variables from .env file
load_dotenv()

# Set up caching for the Flask server
cache = Cache(config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300})

# ------------------------------------------------------------------------------

def userid():
    return session.get('user_id')

# ------------------------------------------------------------------------------
# Database URLs

# Path to the remote database
def database_url():
    return os.getenv('DATABASE_URL')

# Path to the local database
def local_users_url():
    return '../localdb/users.csv'

# ------------------------------------------------------------------------------
# Create a global engine instance

global_engine = create_engine(database_url())

# ------------------------------------------------------------------------------
# Load all the data from the databases

def load_database(use_remote_db):
    if use_remote_db:
        transactions_df, monthly_budgets_df, categorical_budgets_df = load_remote_database()
    else:
        transactions_df, monthly_budgets_df, categorical_budgets_df = load_local_database()

    return transactions_df, monthly_budgets_df, categorical_budgets_df

def load_remote_database():
    transactions_df = load_transactions()
    monthly_budgets_df = load_monthly_budgets()
    categorical_budgets_df = load_categorical_budgets()

    return transactions_df, monthly_budgets_df, categorical_budgets_df

def load_local_database():
    transactions_df = load_local_transactions()
    monthly_budgets_df = load_local_monthly_budgets()
    categorical_budgets_df = load_local_categorical_budgets()

    return transactions_df, monthly_budgets_df, categorical_budgets_df

# ------------------------------------------------------------------------------
# Load specific data from the remote database

@cache.memoize()
def load_transactions():
    query = f"SELECT * FROM Transactions WHERE userid = {userid()};"
    df = pd.read_sql(query, global_engine, parse_dates=['date'])
    return df

@cache.memoize()
def load_monthly_budgets():
    query = f"SELECT * FROM MonthlyBudgets WHERE userid = {userid()};"
    df = pd.read_sql(query, global_engine, parse_dates=['budgetmonth'])
    return df

@cache.memoize()
def load_categorical_budgets():
    query = f"SELECT * FROM CategoricalBudgets WHERE userid = {userid()};"
    df = pd.read_sql(query, global_engine)
    return df

@cache.memoize()
def load_categories():
    df = pd.read_sql("SELECT * FROM Categories;", global_engine)
    return df

def load_users():
    df = pd.read_sql("SELECT * FROM Users;", global_engine)
    return df

# ------------------------------------------------------------------------------
# Load specific data from the local database

def load_local_transactions():
    return pd.read_csv('../localdb/transactions.csv', parse_dates=['date'])

def load_local_monthly_budgets():
    return pd.read_csv('../localdb/monthlybudgets.csv', parse_dates=['budgetmonth'])

def load_local_categorical_budgets():
    return pd.read_csv('../localdb/categoricalbudgets.csv')

def load_local_categories():
    return pd.read_csv('../localdb/categories.csv')

def load_local_users():
    return pd.read_csv('../localdb/users.csv')

# ------------------------------------------------------------------------------
# Save data to the local database

def save_local_transactions(transactions_df):
    transactions_df.to_csv('../localdb/transactions.csv', index=False)

def save_local_monthly_budgets(monthly_budgets_df):
    monthly_budgets_df.to_csv('../localdb/monthlybudgets.csv', index=False)

def save_local_categorical_budgets(categorical_budgets_df):
    categorical_budgets_df.to_csv('../localdb/categoricalbudgets.csv', index=False)

def save_local_categories(categories_df):
    categories_df.to_csv('../localdb/categories.csv', index=False)

def save_local_users(users_df):
    users_df.to_csv('../localdb/users.csv', index=False)

# ------------------------------------------------------------------------------
# Save and update data to the remote database

def get_max_id(table_name, id_column):
    metadata = MetaData()
    metadata.reflect(bind=global_engine)
    table = Table(table_name, metadata, autoload_with=global_engine)

    stmt = select(func.max(table.c[id_column]))
    max_id = 0

    try:
        with global_engine.connect() as conn:
            result = conn.execute(stmt).scalar()
            if result is not None:
                max_id = result
    except Exception as e:
        print(f"Error fetching max {id_column}:", e)

    return max_id

# Ensure all values are native Python types for insertion into the database
def convert_to_native_types(data):
    for key, value in data.items():
        if key == 'date':
            # Ensure date is in the correct format
            if isinstance(value, pd.Timestamp) or isinstance(value, datetime):
                data[key] = value.strftime('%Y-%m-%d')
        elif key == 'amount':
            # Ensure amount is a float with two decimal places
            if isinstance(value, (float, np.float64, int, np.int64)):
                data[key] = round(float(value), 2)
        elif isinstance(value, (np.integer, np.int64)):
            data[key] = int(value)
        elif isinstance(value, (np.float64, float)):
            data[key] = float(value)
    return data

def save_transactions(new_transaction):
    metadata = MetaData()
    metadata.reflect(bind=global_engine)
    transactions_table = Table('transactions', metadata, autoload_with=global_engine) # Load the table schema from the database
    
    new_transaction = convert_to_native_types(new_transaction) # Ensure all values are native Python types
    stmt = transactions_table.insert().values(new_transaction) # Create an insert statement
    
    try:
        with global_engine.connect() as conn:
            conn.begin()
            conn.execute(stmt)
            conn.commit()
            print("Transaction inserted successfully.")
    except Exception as e:
        print("Error inserting transaction:", e)

def save_monthly_budgets(new_monthly_budget):
    metadata = MetaData()
    metadata.reflect(bind=global_engine)
    monthly_budgets_table = Table('monthlybudgets', metadata, autoload_with=global_engine) # Load the table schema from the database

    # Create an insert statement
    new_monthly_budget = convert_to_native_types(new_monthly_budget)
    stmt = monthly_budgets_table.insert().values(new_monthly_budget)

    try:
        with global_engine.connect() as conn:
            conn.begin()
            conn.execute(stmt)
            conn.commit()

            cache.clear()
            print("Monthly budget inserted successfully.")
    except Exception as e:
        print("Error inserting monthly budget:", e)

def update_monthly_budget(userid, budgetmonth, totalbudget):
    metadata = MetaData()
    metadata.reflect(bind=global_engine)
    monthly_budgets_table = Table('monthlybudgets', metadata, autoload_with=global_engine)
    
    # Create an update statement
    stmt = (
        update(monthly_budgets_table)
        .where(
            monthly_budgets_table.c.userid == userid,
            monthly_budgets_table.c.budgetmonth == budgetmonth
        )
        .values(totalbudget=totalbudget)
    )

    try:
        with global_engine.connect() as conn:
            conn.begin()
            conn.execute(stmt)
            conn.commit()

            cache.clear()
            print("Total budget updated successfully!")
    except Exception as e:
        print("Error updating total budget:", e)

def save_categorical_budgets(new_category_budget_row):
    metadata = MetaData()
    metadata.reflect(bind=global_engine)
    categorical_budgets_table = Table('categoricalbudgets', metadata, autoload_with=global_engine) # Load the table schema from the database

    # Create an insert statement
    new_category_budget_row = convert_to_native_types(new_category_budget_row)
    stmt = categorical_budgets_table.insert().values(new_category_budget_row)

    try:
        with global_engine.connect() as conn:
            conn.begin()
            conn.execute(stmt)
            conn.commit()

            cache.clear()
            print("Categorical budgets inserted successfully.")
    except Exception as e:
        print("Error inserting categorical budgets:", e)

def update_categorical_budget(userid, categoryname, new_category_budget):
    metadata = MetaData()
    metadata.reflect(bind=global_engine)
    categorical_budgets_table = Table('categoricalbudgets', metadata, autoload_with=global_engine)
    
    # Create an update statement using SQLAlchemy's expression language
    stmt = (
        update(categorical_budgets_table)
        .where(
            categorical_budgets_table.c.userid == userid,
            categorical_budgets_table.c.categoryname == categoryname
        )
        .values(categorybudget=new_category_budget)
    )

    try:
        with global_engine.connect() as conn:
            conn.begin()
            conn.execute(stmt)
            conn.commit()

            cache.clear()
            print("Category budget updated successfully!")
    except Exception as e:
        print("Error updating category budget:", e)

# ------------------------------------------------------------------------------
# Print the dataframes

def print_dataframes(enable_logging, use_remote_db):
    if enable_logging:
        transactions_df, categories_df, users_df, monthly_budgets_df, categorical_budgets_df = load_database(use_remote_db)

        print('\nTRANSACTIONS DB\n', transactions_df[-5:])
        print('CATEGORIES DB\n', categories_df[-3:])
        print('USERS DB\n', users_df[-3:])
        print('MONTHLY BUDGETS DB\n', monthly_budgets_df[-5:])
        print('CATEGORICAL BUDGETS DB\n', categorical_budgets_df[-5:])

# ------------------------------------------------------------------------------
# Get the current month and year

def current_year():
    return datetime.now().year

def current_month():
    return datetime.now().month

# ------------------------------------------------------------------------------
# Dictionary to convert month names to integer values, and vice versa

def monthsToInt():
    return {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }

def IntToMonths():
    return {v: k for k, v in monthsToInt.items()}

# ------------------------------------------------------------------------------
# Set up user sessions logging

def setup_logging(server, enable_logging):
    if enable_logging:
        logging.basicConfig(level=logging.DEBUG)

        @server.after_request
        def after_request(response):
            logging.debug(f"Session data after request: {dict(session)}")
            return response
    
    else:
        logging.basicConfig(level=logging.CRITICAL)