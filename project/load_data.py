import logging
import pandas as pd
from sqlalchemy import MetaData, Table, create_engine, update
from datetime import datetime
from flask import session
import numpy as np

def userid():
    return session.get('user_id')

# ------------------------------------------------------------------------------
# Database URLs

# Path to the remote database
def database_url():
    return "postgresql://postgresql_finance_user:Xda6CRIftQmupM1vnXit1fnbKIfcfLhc@dpg-cp1p0hud3nmc73b8v0qg-a.ohio-postgres.render.com:5432/postgresql_finance"

# Path to the local database
def local_users_url():
    return '../localdb/users.csv'

# ------------------------------------------------------------------------------
# Load all the data from the databases

# Create an SQLAlchemy engine instance
def create_engine_instance():
    return create_engine(database_url())

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

def load_transactions():
    engine = create_engine_instance()
    df = pd.read_sql("SELECT * FROM Transactions;", engine, parse_dates=['date'])
    engine.dispose()
    return df

def load_monthly_budgets():
    engine = create_engine_instance()
    df = pd.read_sql("SELECT * FROM MonthlyBudgets;", engine, parse_dates=['budgetmonth'])
    engine.dispose()
    return df

def load_categorical_budgets():
    engine = create_engine_instance()
    df = pd.read_sql("SELECT * FROM CategoricalBudgets;", engine)
    engine.dispose()
    return df

def load_categories():
    engine = create_engine_instance()
    df = pd.read_sql("SELECT * FROM Categories;", engine)
    engine.dispose()
    return df

def load_users():
    engine = create_engine_instance()
    df = pd.read_sql("SELECT * FROM Users;", engine)
    engine.dispose()
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
# Save data to the remote database

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
    engine = create_engine_instance()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    transactions_table = Table('transactions', metadata, autoload_with=engine) # Load the table schema from the database
    
    new_transaction = convert_to_native_types(new_transaction) # Ensure all values are native Python types
    stmt = transactions_table.insert().values(new_transaction) # Create an insert statement
    
    try:
        with engine.connect() as conn:
            conn.begin()
            conn.execute(stmt)
            conn.commit()
            print("Transaction inserted successfully.")
    except Exception as e:
        print("Error inserting transaction:", e)
    
    engine.dispose()

def save_monthly_budgets(new_monthly_budget):
    engine = create_engine_instance()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    monthly_budgets_table = Table('monthlybudgets', metadata, autoload_with=engine) # Load the table schema from the database

    # Create an insert statement
    new_monthly_budget = convert_to_native_types(new_monthly_budget)
    stmt = monthly_budgets_table.insert().values(new_monthly_budget)

    try:
        with engine.connect() as conn:
            conn.begin()
            conn.execute(stmt)
            conn.commit()
            print("Monthly budget inserted successfully.")
    except Exception as e:
        print("Error inserting monthly budget:", e)
    
    engine.dispose()

def update_monthly_budget(userid, budgetmonth, totalbudget):
    engine = create_engine_instance()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    monthly_budgets_table = Table('monthlybudgets', metadata, autoload_with=engine)
    
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
        with engine.connect() as conn:
            conn.begin()
            conn.execute(stmt)
            conn.commit()
            print("Total budget updated successfully!")
    except Exception as e:
        print("Error updating total budget:", e)
    
    engine.dispose()

def save_categorical_budgets(new_category_budget_row):
    engine = create_engine_instance()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    categorical_budgets_table = Table('categoricalbudgets', metadata, autoload_with=engine) # Load the table schema from the database

    # Create an insert statement
    new_category_budget_row = convert_to_native_types(new_category_budget_row)
    stmt = categorical_budgets_table.insert().values(new_category_budget_row)

    try:
        with engine.connect() as conn:
            conn.begin()
            conn.execute(stmt)
            conn.commit()
            print("Categorical budgets inserted successfully.")
    except Exception as e:
        print("Error inserting categorical budgets:", e)
    
    engine.dispose()

def update_categorical_budget(userid, categoryname, new_category_budget):
    engine = create_engine_instance()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    categorical_budgets_table = Table('categoricalbudgets', metadata, autoload_with=engine)
    
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
        with engine.connect() as conn:
            conn.begin()
            conn.execute(stmt)
            conn.commit()
            print("Category budget updated successfully!")
    except Exception as e:
        print("Error updating category budget:", e)
    
    engine.dispose()

def save_categories(categories_df):
    engine = create_engine_instance()
    categories_df.to_sql('categories', engine, if_exists='replace', index=False)
    engine.dispose()

def save_users(users_df):
    engine = create_engine_instance()
    users_df.to_sql('users', engine, if_exists='replace', index=False)
    engine.dispose()

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