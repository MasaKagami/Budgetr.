from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime

# Path to the remote database
def database_url():
    return "postgresql://postgresql_finance_user:Xda6CRIftQmupM1vnXit1fnbKIfcfLhc@dpg-cp1p0hud3nmc73b8v0qg-a.ohio-postgres.render.com:5432/postgresql_finance"

# Path to the local database
def local_database_url():
    return '../localdb/users.csv'

# Create an SQLAlchemy engine instance
def create_engine_instance():
    return create_engine(database_url())

def load_remote_database():
    engine = create_engine_instance()

    transactions_df = load_transactions(engine)
    monthly_budgets_df = load_monthly_budgets(engine)
    categorical_budgets_df = load_categorical_budgets(engine)
    categories_df = load_categories(engine)
    users_df = load_users(engine)
    
    engine.dispose() # Close the connection

    return transactions_df, categories_df, users_df, monthly_budgets_df, categorical_budgets_df

def load_local_database():
    transactions_df = load_local_transactions()
    categories_df = load_local_categories()
    users_df = load_local_users()
    monthly_budgets_df = load_local_monthly_budgets()
    categorical_budgets_df = load_local_categorical_budgets()

    return transactions_df, categories_df, users_df, monthly_budgets_df, categorical_budgets_df

# ------------------------------------------------------------------------------
# Load the data from the remote database

def load_transactions(engine):
    return pd.read_sql("SELECT * FROM Transactions;", engine, parse_dates=['date'])

def load_monthly_budgets(engine):
    return pd.read_sql("SELECT * FROM MonthlyBudgets;", engine, parse_dates=['budgetmonth'])

def load_categorical_budgets(engine):
    return pd.read_sql("SELECT * FROM CategoricalBudgets;", engine)

def load_categories(engine):
    return pd.read_sql("SELECT * FROM Categories;", engine)

def load_users(engine):
    return pd.read_sql("SELECT * FROM Users;", engine)

# ------------------------------------------------------------------------------
# Load the data from the local database

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
# Print the dataframes

def print_dataframes(transactions_df, categories_df, users_df, monthly_budgets_df, categorical_budgets_df):
    # print('\nTRANSACTIONS DB\n', transactions_df[:5])
    # print('CATEGORIES DB\n', categories_df[:5])
    print('USERS DB\n', users_df[:5])
    # print('MONTHLY BUDGETS DB\n', monthly_budgets_df[:5])
    # print('CATEGORICAL BUDGETS DB\n', categorical_budgets_df[:5])

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