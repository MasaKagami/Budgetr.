import logging
import pandas as pd
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.dialects.postgresql import insert as pg_insert
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

def convert_to_native_types(transaction):
    for key, value in transaction.items():
        if isinstance(value, (pd.Timestamp,)):
            transaction[key] = str(value)
        elif isinstance(value, (np.integer, np.int64)):
            transaction[key] = int(value)
    return transaction

def save_transactions(new_transaction):
    engine = create_engine_instance()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    transactions_table = Table('Transactions', metadata, autoload_with=engine)
    
    new_transaction = convert_to_native_types(new_transaction)
    
    stmt = pg_insert(transactions_table).values(new_transaction)
    upsert_stmt = stmt.on_conflict_do_update(
        index_elements=['transactionid'],
        set_={c.key: c for c in stmt.excluded if c.key not in ['transactionid']}
    )
    
    with engine.begin() as conn:
        conn.execute(upsert_stmt)
    
    engine.dispose()

def save_monthly_budgets(monthly_budgets_df):
    engine = create_engine_instance()
    monthly_budgets_df.to_sql('MonthlyBudgets', engine, if_exists='replace', index=False)
    engine.dispose()

def save_categorical_budgets(categorical_budgets_df):
    engine = create_engine_instance()
    categorical_budgets_df.to_sql('CategoricalBudgets', engine, if_exists='replace', index=False)
    engine.dispose()

def save_categories(categories_df):
    engine = create_engine_instance()
    categories_df.to_sql('Categories', engine, if_exists='replace', index=False)
    engine.dispose()

def save_users(users_df):
    engine = create_engine_instance()
    users_df.to_sql('Users', engine, if_exists='replace', index=False)
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