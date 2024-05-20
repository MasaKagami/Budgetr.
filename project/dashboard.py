from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px
from datetime import datetime
from dash import Dash, dcc, html, Input, Output, State, ALL

app = Dash(__name__)
app.title = 'myfinanceplanner'

# -- Import and clean data (importing csv into pandas)
def load_data():
    # Connection setup   
    # Database URL  
    DATABASE_URL = "postgresql://postgresql_finance_user:Xda6CRIftQmupM1vnXit1fnbKIfcfLhc@dpg-cp1p0hud3nmc73b8v0qg-a.ohio-postgres.render.com:5432/postgresql_finance"

    # Creating an SQLAlchemy engine
    engine = create_engine(DATABASE_URL)
    
    # Use the engine to execute a query and load into DataFrame
    transactions_df = pd.read_sql("SELECT * FROM Transactions;", engine, parse_dates=['date'])
    categories_df = pd.read_sql("SELECT * FROM Categories;", engine)
    users_df = pd.read_sql("SELECT * FROM Users;", engine)
    monthly_budgets_df = pd.read_sql("SELECT * FROM MonthlyBudgets;", engine, parse_dates=['budgetmonth'])
    categorical_budgets_df = pd.read_sql("SELECT * FROM CategoricalBudgets;", engine)
    engine.dispose()  # Close the connection safely

    return transactions_df, categories_df, users_df, monthly_budgets_df, categorical_budgets_df

def load_local_database():
    # Load data from CSV files
    transactions_df = pd.read_csv('../localdb/transactions.csv', parse_dates=['date'])
    categories_df = pd.read_csv('../localdb/categories.csv')
    users_df = pd.read_csv('../localdb/users.csv')
    monthly_budgets_df = pd.read_csv('../localdb/monthlybudgets.csv', parse_dates=['budgetmonth'])
    categorical_budgets_df = pd.read_csv('../localdb/categoricalbudgets.csv')

    return transactions_df, categories_df, users_df, monthly_budgets_df, categorical_budgets_df

# Loading data
transactions_df, categories_df, users_df, monthly_budgets_df, categorical_budgets_df = load_local_database()
# transactions_df, categories_df, users_df, budgets_df = load_data()
print('\nTRANSACTIONS DB\n', transactions_df[:5])
print('CATEGORIES DB\n', categories_df[:5])
print('USERS DB\n', users_df[:5])
print('MONTHLY BUDGETS DB\n', monthly_budgets_df[:5])
print('CATEGORICAL BUDGETS DB\n', categorical_budgets_df[:5])

# Dictionary to convert month names to integer values
monthsToInt = {
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

# Reverse the dictionary to convert the integers to month names
IntToMonths = {v: k for k, v in monthsToInt.items()} 

current_month = datetime.now().month
current_year = datetime.now().year

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("My Financial Dashboard", style={'text-align': 'center'}),

    dcc.RadioItems(id='chart_type',
                   options=[
                       {'label': 'Line Chart', 'value': 'line'},
                       {'label': 'Bar Chart', 'value': 'bar'},
                       {'label': 'Stacked Bar Chart', 'value': 'stacked_bar'}
                   ],
                   value='line',
                   style={'margin-top': '20px'}
                   ),

    # Put month selector in a container so it can be hidden when not needed
    html.Div(id='month_selector_container', children=[
        html.H4("Select Month", style = {'text-align': 'left'}),
        dcc.Dropdown(id="slct_month",
                    options= [{'label': key, 'value': value} for key, value in monthsToInt.items()], # Convert the python dictionary to a list of dictionaries in HTML
                    multi=False,
                    value=1, # Initial value
                    style={'width': "40%"}
                    ),
    ]),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_spending_map', figure={}),

    html.H2("Add a New Transaction", style={'text-align': 'center'}),
        dcc.DatePickerSingle(
            id='input_date',
            date=pd.Timestamp.now().strftime('%Y-%m-%d'),
            display_format='YYYY-MM-DD',
            style={'width': '10%', 'margin': '10px auto', 'display': 'block'}
        ),
        dcc.Input(
            id='input_amount',
            type='number',
            min=0,
            placeholder='Amount',
            style={'width': '10%', 'margin': '10px auto', 'display': 'block'}
        ),
        dcc.Dropdown(
            id='input_category',
            options=[{'label': category, 'value': category} for category in categories_df['name']],
            placeholder='Select Category',
            style={'width': '40%', 'margin': '10px auto', 'display': 'block'}
        ),
        dcc.Input(
            id='input_description',
            type='text',
            placeholder='Description',
            style={'width': '40%', 'margin': '10px auto', 'display': 'block'}
        ),
        html.Button('Add Transaction', id='submit_transaction', n_clicks=0, style={'width': '20%', 'margin': '10px auto', 'display': 'block'}),
    html.Div(id='transaction_status', style={'text-align': 'center'}), # Display the status of the transaction   

    html.H2("Manage Budget", style={'text-align': 'center'}),
    html.Div(id='budget_month_selector', children=[
    html.H4("Select Month and Year for Budget", style = {'text-align': 'left'}),
        dcc.Dropdown(id="slct_budget_month",
                    options= [{'label': key, 'value': value} for key, value in monthsToInt.items()],
                    multi=False,
                    value=current_month, # Initial value
                    style={'width': "40%", 'display': 'inline-block'}
                    ),
        dcc.Dropdown(id="slct_budget_year",
                    options= [{'label': year, 'value': year} for year in range(2020, 2026)], # Temporary range of years
                    multi=False,
                    value=current_year, # Initial value
                    style={'width': "30%", 'display': 'inline-block', 'margin-left': '10px'}
                    ),
    ], style={'text-align': 'center'}),
    html.Div([
        html.Label("Total Budget:"),
        dcc.Input(
            id='input_total_budget',
            type='number',
            min=0,
            style={'margin-left': '10px', 'margin-bottom': '20px'}
        )
    ], style={'text-align': 'center'}),
    html.Div(id='budget_overview', style={'text-align': 'center', 'margin-bottom': '20px'}), # Display the total budget
    html.Div(id='budget_inputs'), # Display the allocated budget for each category
    html.Div(id='unallocated_budget', style={'text-align': 'center', 'margin-bottom': '20px'}), # Display the unallocated budget
    html.Button('Update Budget', id='submit_budget', n_clicks=0, style={'width': '20%', 'margin': '10px auto', 'display': 'block'}),
    html.Div(id='budget_status', style={'text-align': 'center'}) # Display the status of the budget update
])

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output('my_spending_map', 'figure')],
    [Input('chart_type', 'value'),
     Input('slct_month', 'value')]
)

def update_graph(chart_type, selected_month):
    # Filter the DataFrame to the selected month
    filtered_df = transactions_df[transactions_df['date'].dt.month == selected_month]

    if chart_type == 'line':
        # Group by day of the month and sum the amounts
        daily_spending = filtered_df.groupby(filtered_df['date'].dt.day)['amount'].sum().reset_index()
        daily_spending.columns = ['Day', 'Total Spent']

        # Create a line chart with Plotly Express
        fig = px.line(
            daily_spending, x='Day', y='Total Spent',
            title=f'Spending Trend for {IntToMonths[selected_month]}',
            labels={'Day': 'Day of the Month', 'Total Spent': 'Amount Spent ($)'},
            markers=True, # Makes it easier to see individual data points
            range_x=[1, 31] # Show all days of the month
            )
        
        # Show the x-axis ticks for each day of the month
        fig.update_layout(
            xaxis = dict(
                tickmode = 'linear'
            )
        )
    
    elif chart_type == 'bar':
        # Group by category and sum the amounts
        category_spending = filtered_df.groupby('categoryname')['amount'].sum().reset_index()
        category_spending.columns = ['Category', 'Total Spent']

        # Create a bar chart with Plotly Express
        fig = px.bar(
            category_spending, x='Category', y='Total Spent',
            title=f'Spending by Category for {IntToMonths[selected_month]}',
            labels={'category': 'Category', 'amount': 'Amount Spent ($)'},
            color='Category'
            )
    
    elif chart_type == 'stacked_bar':
        # Group by category and sum the amounts
        daily_category_spending = filtered_df.groupby([filtered_df['date'].dt.day, 'categoryname'])['amount'].sum().reset_index()
        daily_category_spending.columns = ['Day', 'Category', 'Total Spent']
        # print("\nSTACKED BAR CHART\n", daily_category_spending)

        # Create a stacked bar chart with Plotly Express
        fig = px.bar(
            daily_category_spending, x='Day', y='Total Spent', color='Category',
            title=f'Spending by Category for {IntToMonths[selected_month]}',
            labels={'Day': 'Day of the Month', 'Total Spent': 'Amount Spent ($)'}
            )
        
        # Show the x-axis ticks for each day of the month
        fig.update_layout(
            xaxis = dict(
                tickmode = 'linear'
            )
        )

    return [fig]

# ------------------------------------------------------------------------------
@app.callback(
    Output('transaction_status', 'children'),
    [Input('submit_transaction', 'n_clicks')],
    [State('input_date', 'date'), State('input_amount', 'value'), State('input_category', 'value'), State('input_description', 'value')]
)

def add_transaction(n_clicks, date, amount, category, description):
    # If button has been clicked and all fields have been filled out
    if n_clicks > 0 and date and amount and category:
        # Load the latest transactions DB
        transactions_df = pd.read_csv('../localdb/transactions.csv', parse_dates=['date'])

        # Add the new transaction to the DataFrame
        new_transaction = {
            'transactionid': transactions_df['transactionid'].max() + 1, # Increment the transaction ID
            'userid': 1, # Hardcoded for now
            'date': date,
            'categoryname': category,
            'amount': amount, 
            'description': description
            }
        
        # Append the new transaction to the end of the DataFrame
        transactions_df.loc[len(transactions_df)] = new_transaction
        
        # Save the updated DataFrame to the CSV file
        transactions_df.to_csv('../localdb/transactions.csv', index=False)

        return f"Transaction added: {date}, {amount}, {category}"
    elif n_clicks > 0:
        if not date:
            return "Please select a date"
        elif not amount:
            return "Please enter an amount"
        elif not category:
            return "Please select a category"
    return "" # If the button has not been clicked

# ------------------------------------------------------------------------------
@app.callback(
    [Output('budget_overview', 'children'),
     Output('input_total_budget', 'value'),
     Output('budget_inputs', 'children'),
     Output('unallocated_budget', 'children')],
    [Input('slct_budget_month', 'value'), Input('slct_budget_year', 'value'),
     Input('submit_budget', 'n_clicks')], # Updating the budget triggers this callback to update the budget overview
    [State('slct_budget_month', 'value'), State('slct_budget_year', 'value')])

def display_budget_overview(selected_month, selected_year, placeholder1, placeholder2, placeholder3):
    # Convert the selected month and year to a datetime object
    selected_date = pd.to_datetime(f'{selected_year}-{selected_month:02d}-01')

    # Load the latest budgets DB
    monthly_budgets_df = pd.read_csv('../localdb/monthlybudgets.csv', parse_dates=['budgetmonth'])
    categorical_budgets_df = pd.read_csv('../localdb/categoricalbudgets.csv')
    
    monthly_budget_row = monthly_budgets_df[monthly_budgets_df['budgetmonth'] == selected_date]
    if monthly_budget_row.empty:
        total_budget = 0
    else:
        total_budget = int(monthly_budget_row['totalbudget'].values[0])

    budget_overview = f"Total Budget for {selected_date.strftime('%Y-%m')}: ${total_budget}"

    # Display the allocated budget for each category
    budget_inputs = [] # List to store the budgets for each category
    allocated_budget = 0
    for index, row in categorical_budgets_df.iterrows():
        category_name = row['categoryname']
        category_budget = row['categorybudget']
        allocated_budget += category_budget # Calculate the total allocated budget
        budget_inputs.append(
            html.Div([
                html.Label(f"{category_name}:"),
                dcc.Input(
                    id={'type': 'budget_input', 'index': index},
                    type="number",
                    value=category_budget,
                    min=0,
                    style={'margin-left': '10px'}
                )
            ], style={'margin-bottom': '10px'})
        )

    unallocated_budget = int(total_budget - allocated_budget)
    if unallocated_budget < 0:
        unallocated_budget_display = f"Exceeding Monthly Budget by ${-unallocated_budget}"
    elif unallocated_budget > 0:
        unallocated_budget_display = f"Remaining Monthly Budget of ${unallocated_budget}"
    else:
        unallocated_budget_display = f"${total_budget} Budget Fully Allocated"

    return budget_overview, total_budget, budget_inputs, unallocated_budget_display

# ------------------------------------------------------------------------------
@app.callback(
    [Output('budget_status', 'children'),
     Output('slct_budget_month', 'value'),
     Output('slct_budget_year', 'value')],
    [Input('submit_budget', 'n_clicks')],
    [State('slct_budget_month', 'value'), State('slct_budget_year', 'value'), State('input_total_budget', 'value'), State({'type': 'budget_input', 'index': ALL}, 'value')]
)

def update_budget(n_clicks, selected_month, selected_year, total_budget, budget_values):
    if n_clicks > 0:
        if total_budget is None or total_budget == '':
            return "Please enter a total budget", selected_month, selected_year
        if not all(budget_values):
            return "Please enter a budget for each category", selected_month, selected_year

        # Convert the selected month and year to a datetime object
        selected_date = pd.to_datetime(f'{selected_year}-{selected_month:02d}-01')
        
        # Load the latest budgets DB before updating
        monthly_budgets_df = pd.read_csv('../localdb/monthlybudgets.csv', parse_dates=['budgetmonth'])
        categorical_budgets_df = pd.read_csv('../localdb/categoricalbudgets.csv')
        
        # Update or insert the monthly budget
        if selected_date in monthly_budgets_df['budgetmonth'].values:
            monthly_budgets_df.loc[monthly_budgets_df['budgetmonth'] == selected_date, 'totalbudget'] = total_budget
        else:
            new_monthly_budget = {
                'budgetid': monthly_budgets_df['budgetid'].max() + 1,
                'userid': 1,  # Hardcoded for now
                'totalbudget': total_budget,
                'budgetmonth': selected_date
            }
            monthly_budgets_df.loc[len(monthly_budgets_df)] = new_monthly_budget
        
        # Update the categorical budgets
        for index, value in enumerate(budget_values):
            categorical_budgets_df.at[index, 'categorybudget'] = value

        # Save the updated DataFrames to the CSV files
        monthly_budgets_df.to_csv('../localdb/monthlybudgets.csv', index=False)
        categorical_budgets_df.to_csv('../localdb/categoricalbudgets.csv', index=False)

        return "Budget updated successfully!", selected_month, selected_year
    return "", selected_month, selected_year

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)