from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px
from datetime import datetime
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
from turtle import width

app = Dash(__name__)
app.title = 'myfinanceplanner'

# -- Import and clean data (importing csv into pandas)
def load_data():
    # Connection setup
    DATABASE_URL = "postgresql://postgresql_finance_user:Xda6CRIftQmupM1vnXit1fnbKIfcfLhc@dpg-cp1p0hud3nmc73b8v0qg-a.ohio-postgres.render.com:5432/postgresql_finance"

    # Creating an SQLAlchemy engine
    engine = create_engine(DATABASE_URL)
    
    # Use the engine to execute a query and load into DataFrame
    transactions_df = pd.read_sql("SELECT * FROM Transactions;", engine, parse_dates=['date'])
    categories_df = pd.read_sql("SELECT * FROM Categories;", engine)
    users_df = pd.read_sql("SELECT * FROM Users;", engine)
    monthly_budgets_df = pd.read_sql("SELECT * FROM MonthlyBudgets;", engine, parse_dates=['budgetmonth'])
    categorical_budgets_df = pd.read_sql("SELECT * FROM CategoricalBudgets;", engine)
    
    # Close the connection safely
    engine.dispose()

    return transactions_df, categories_df, users_df, monthly_budgets_df, categorical_budgets_df

def load_local_database():
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

# Prepare the transactions DataFrame for the dashboard, convert date to datetime object
transactions_df['date'] = pd.to_datetime(transactions_df['date'])
transactions_df['date_display'] = transactions_df['date'].dt.strftime('%Y-%m-%d')
transactions_df.sort_values('date', ascending=False, inplace=True)  # Sort by date descending

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

# Get the current month and year
current_month = datetime.now().month
current_year = datetime.now().year

# ------------------------------------------------------------------------------
# Main App layout
app.layout = html.Div([
    html.Link(
        href='https://fonts.googleapis.com/css2?family=Lexend:wght@100..900&display=swap',
        rel='stylesheet'
    ),
    html.Div([
        html.H1("My Financial Dashboard", style={'text-align': 'center'}),
        html.Div([
            html.Button('DASHBOARD', id='view_dashboard'),
            html.Button('SPENDINGS', id='input_spendings')
        ], className='button', style={'text-align': 'center', 'margin-bottom': '20px'}),

        html.Div(id='dashboard_page', style={'display': 'none'}, children=[
            html.Div([
                html.H4("Select Year and Month: "),
                dcc.Dropdown(
                    id="slct_year",
                    options=[
                        {'label': str(year), 'value': year} for year in range(2000, current_year + 1)
                    ],
                    multi=False,
                    value=current_year-1, # Initial value (last year)
                    className='dropdownYear',
                    style={'width': "150px", 'margin': '10px auto'}
                ),
                dcc.Dropdown(
                    id="slct_month",
                    options=[{'label': key, 'value': value} for key, value in monthsToInt.items()],
                    multi=False,
                    value=current_month, # Initial value
                    className='dropdownMonth',
                    style={'width': "150px", 'margin': '10px auto'}
                ),
            ], className='selectYearandMonth'),

            html.Div([
                html.Div([
                    html.Div([
                        # html.H3("Financial Overview", className = 'dataTitle'),
                        html.H3("Net Balance", className='dataTitle'),
                        html.Div([
                            html.P(id='net-balance-output'),
                        ], className='outputBox'),
                        html.H3("Status", className='dataTitle'),
                        html.Div([
                            html.P(id='status-output'),
                        ], className='outputBox')
                    ], className='financial-overview'),

                    html.Div([
                        html.H3("Expense Categorization", className='dataTitle'),
                        dcc.Graph(id='expense_categorization_graph', figure={}),
                    ], className='expense-categorization')
                ], className='section3'),

                html.Div([
                    html.Div([
                        html.H3("Daily Spending Trend", className='dataTitle'),
                        dcc.Graph(id='daily_spending_trend_graph', figure={}),
                    ], className='daily-spending-trend'),

                    html.Div([
                        html.H3("Budget vs. Actual Spending Per Category", className='dataTitle'),
                        dcc.Graph(id='budget_vs_actual_spending_graph', figure={}),
                    ], className='budget-vs-actual-spending'),
                ], className='section4'),

                html.Div([
                    html.H3("Recent Transactions", className='dataTitle'),
                    dash_table.DataTable(
                        id='transactions_table',
                        columns=[
                            {"name": "Date", "id": "date_display"},
                            {"name": "Category Name", "id": "categoryname"},
                            {"name": "Amount", "id": "amount"},
                            {"name": "Description", "id": "description"}
                        ],
                        data=transactions_df.to_dict('records'),
                        style_table={
                            'height': '300px',
                            'overflowY': 'auto'
                        },
                        style_cell={
                            'textAlign': 'left',
                            'color': 'white',
                            'backgroundColor': '#151a28',
                            'border': 'none'
                        },
                        style_header={
                            'backgroundColor': '#222222',
                            'fontWeight': 'bold'
                        }
                    )
                ], className='section5'),
            ], className='dataContainer2')
        ], className= 'dataContainer'), # Contains all the data components for the dashboard page

        html.Div(id='spendings_page', style={'display': 'none'}, children=[
            html.H2("Add a New Transaction", style={'text-align': 'center'}),
            dcc.DatePickerSingle(
                id='input_date',
                date=pd.Timestamp.now().strftime('%Y-%m-%d'),
                display_format='YYYY-MM-DD',
                style={'width': '150px', 'margin': '10px auto', 'display': 'block'}
            ),
            dcc.Input(
                id='input_amount',
                type='number',
                min=0,
                placeholder='Amount',
                style={'width': '150px', 'margin': '10px auto', 'display': 'block'}
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
            html.Button('Add Transaction', id='submit_transaction', n_clicks=0, style={'width': '150px', 'margin': '10px auto', 'display': 'block'}),
            html.Div(id='transaction_status', style={'text-align': 'center'}),  # Display the status of the transaction   

            html.H2("Manage Budget", style={'text-align': 'center'}),
            html.Div(id='budget_month_selector', children=[
                dcc.Dropdown(id="slct_budget_month",
                            options=[{'label': key, 'value': value} for key, value in monthsToInt.items()],
                            multi=False,
                            value=current_month, # Initial value
                            style={'width': "150px", 'margin': '10px auto'}
                            ),
                dcc.Dropdown(id="slct_budget_year",
                            options=[{'label': year, 'value': year} for year in range(2000, current_year + 1)],
                            multi=False,
                            value=current_year, # Initial value
                            style={'width': '150px', 'margin': '10px auto'}
                            ),
            ], style={'text-align': 'center'}),
            html.Div([
                html.Label("Total Budget:"),
                dcc.Input(
                    id='input_total_budget',
                    type='number',
                    min=0,
                    style={'margin-left': '10px', 'margin-bottom': '20px'}
                ),
                html.Div(id='budget_overview', style={'text-align': 'center', 'margin-bottom': '20px'}),
                html.Button('Update Total Budget', id='submit_total_budget', n_clicks=0, style={'width': '150px', 'margin': '10px auto', 'display': 'block'}),
                html.Div(id='total_budget_status', style={'text-align': 'center'})
            ], style={'text-align': 'center'}),
            html.Div([
                dash_table.DataTable(
                    id='budget_table',
                    columns=[
                        {'name': 'Category', 'id': 'categoryname', 'type': 'text'},
                        {'name': 'Budget', 'id': 'categorybudget', 'type': 'numeric', 'editable': True}
                    ],
                    data=[],
                    style_table={'width': '60%', 'margin': 'auto'},
                    style_cell={'textAlign': 'left'}
                )
            ], style={'text-align': 'center', 'margin-bottom': '20px'}),
            html.Div(id='unallocated_budget', style={'text-align': 'center', 'margin-bottom': '20px'}),  # Display the unallocated budget
            html.Div([
                dcc.Dropdown(
                    id='budget_category_dropdown',
                    options=[{'label': category, 'value': category} for category in categorical_budgets_df['categoryname']],
                    placeholder='Select Category',
                    style={'width': '40%', 'margin': '10px auto', 'display': 'inline-block'}
                ),
                dcc.Input(
                    id='budget_category_input',
                    type='number',
                    min=0,
                    placeholder='Enter Budget',
                    style={'width': '150px', 'margin': '10px auto', 'display': 'inline-block', 'margin-left': '10px'}
                ),
                html.Button('Update Category Budget', id='submit_category_budget', n_clicks=0, style={'width': '150px', 'margin': '10px auto', 'display': 'block'}),
                html.Div(id='category_budget_status', style={'text-align': 'center'})
            ], style={'text-align': 'center', 'margin-bottom': '20px'}),

            # Hidden div to store update triggers
            html.Div(id='update_trigger', style={'display': 'none'})
        ]),
    ], className='dashboard')
], className='background')

# ------------------------------------------------------------------------------
# Callback to switch between pages
@app.callback(
    [Output('dashboard_page', 'style'),
     Output('spendings_page', 'style')],
    [Input('input_spendings', 'n_clicks'),
     Input('view_dashboard', 'n_clicks')]
)

def toggle_pages(input_spendings_clicks=None, view_dashboard_clicks=None):
    ctx = callback_context
    if not ctx.triggered:
        # Set the default button ID if no button has been clicked
        button_id = 'view_dashboard'
    else:
        # Get the ID of the button that triggered the callback
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Return the display style for the dashboard and spendings pages
    if button_id == 'view_dashboard':
        return {'display': 'block'}, {'display': 'none'}
    elif button_id == 'input_spendings':
        return {'display': 'none'}, {'display': 'block'}

    return {'display': 'none'}, {'display': 'block'} # Default to the dashboard page

# ------------------------------------------------------------------------------
# Callback for updating the dashboard page
@app.callback(
    [Output('net-balance-output', 'children'), 
     Output('status-output', 'children'),
     Output('expense_categorization_graph', 'figure'), 
     Output('daily_spending_trend_graph', 'figure'),
     Output('budget_vs_actual_spending_graph', 'figure'),
     Output('transactions_table', 'data')],
    [Input('slct_year', 'value'),
     Input('slct_month', 'value')]
)

def update_graph(selected_year, selected_month):
    # Filters to only include rows where the year and month match the input year and month
    # Boolean indexing: [ ] filters rows based on a condition
    filtered_df = transactions_df[(transactions_df['date'].dt.year == selected_year) &
                                  (transactions_df['date'].dt.month == selected_month)]

    # total spent in a month
    total_spent = filtered_df['amount'].sum()

    # converting to date-time
    monthly_budgets_df['budgetmonth'] = pd.to_datetime(monthly_budgets_df['budgetmonth'])

    # .iloc[0] retrieves the first value from the resulting series
    monthly_budget = monthly_budgets_df[
        (monthly_budgets_df['budgetmonth'].dt.year == selected_year) &
        (monthly_budgets_df['budgetmonth'].dt.month == selected_month)
    ]['totalbudget'].iloc[0]

    net_balance = monthly_budget - total_spent
    print("Net Balance:", net_balance)  # Debugging statement

    net_balance_output = format_net_balance(net_balance)
    net_balance_output = html.Span(net_balance_output, className='netBalanceOutput')
    
    status_text, color = determine_status(monthly_budget, total_spent, selected_year, selected_month)
    status_output = html.Span(status_text, style={'color': color}, className='statusOutput')

    expense_categorization_fig = update_expense_categorization_graph(filtered_df)
    daily_spending_trend_fig = update_daily_spending_trend_graph(filtered_df, monthly_budget)
    budget_vs_actual_spending_fig = update_budget_vs_actual_spending_graph(filtered_df, categorical_budgets_df)
    
    transactions_table_data = filtered_df[['date_display', 'categoryname', 'amount', 'description']].to_dict('records')
    
    # same order as in the output call-back
    return net_balance_output, status_output, expense_categorization_fig, daily_spending_trend_fig, budget_vs_actual_spending_fig, transactions_table_data

def format_net_balance(net_balance, ):
    if net_balance < 0:
        formatted_balance = f"({-net_balance})"
    else:
        formatted_balance = str(net_balance)
    print("Formatted Balance:", formatted_balance)  # Debugging statement
    return formatted_balance

def determine_status(monthly_budget, total_spent, selected_year, selected_month):
    # key-value pairs
    status_colors = {
        "EXCELLENT": "#00FF00",     
        "VERY GOOD": "#7FFF00",     
        "GOOD": "#FFFF00",          
        "FAIR": "#FFD700",          
        "NEEDS IMPROVEMENT": "#FFA500",
        "POOR": "#FF8C00",          
        "VERY POOR": "#FF4500",      
        "EXTREMELY POOR": "#FF0000",
        "CRITICAL": "#DC143C",      
        "SEVERE": "#8B0000"         
    }

    daily_budget = calculated_daily_budget(monthly_budget, selected_year, selected_month)
    today = pd.Timestamp.today()
    if selected_year == today.year and selected_month == today.month:
        days_so_far = today.day
    else:
        days_so_far = pd.Period(f'{selected_year}-{selected_month}').days_in_month

    average_daily_spending = total_spent / days_so_far
    spent_percentage = (average_daily_spending/daily_budget) * 100

    if spent_percentage < 50:
        status_key = "EXCELLENT"
    elif 50 <= spent_percentage < 70:
        status_key = "VERY GOOD"
    elif 70 <= spent_percentage < 85:
        status_key = "GOOD"
    elif 85 <= spent_percentage < 95:
        status_key = "FAIR"
    elif 95 <= spent_percentage < 100:
        status_key = "NEEDS IMPROVEMENT"
    elif 100 <= spent_percentage < 110:
        status_key = "POOR"
    elif 110 <= spent_percentage < 120:
        status_key = "VERY POOR"
    elif 120 <= spent_percentage < 130:
        status_key = "EXTREMELY POOR"
    elif 130 <= spent_percentage < 150:
        status_key = "CRITICAL"
    else:
        status_key = "SEVERE"

    return status_key, status_colors[status_key]

def calculated_daily_budget(monthly_budget, year, month):
    days_in_month = pd.Period(f'{year}-{month}').days_in_month
    return monthly_budget/days_in_month

def update_expense_categorization_graph(filtered_df):
    category_Colors = {
        "housing": "red", 
        "investments": "blue", 
        "debt payments": "green",
        "healthcare": "purple", 
        "food": "pink",
        "entertainment & lesiure": "gold", 
        "education": "gray", 
        "transportation": "silver", 
        "personal care": "yellow", 
        "miscellaneous": "orange"
    }
    
    fig = px.pie(
        filtered_df, 
        values='amount', 
        names='categoryname', 
        color='categoryname',
        hole=0.3,
        color_discrete_map=category_Colors
    )

    fig.update_traces(
        # textinfo='percent',  # Show both percentage and label
        insidetextorientation='radial',  # Better orientation for text inside
        textfont=dict(
            color='#eeeee4',
            size=13
        )
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=300,
        legend=dict(
            font=dict(
                color="#eeeee4",
                size=11
            )
        )
    )

    return fig

def update_daily_spending_trend_graph(filtered_df, monthly_budget):
    # Sum daily spending and calculate cumulative total
    daily_spending = filtered_df.groupby(filtered_df['date'].dt.day)['amount'].sum().cumsum().reset_index()
    daily_spending.columns = ['Day', 'Cumulative Spending']

    # Creating a new dataFrame, budget_line
    max_day = daily_spending['Day'].max()
    budget_line = pd.DataFrame({
        # creates a column named 'day' consisting of the values '1' and 'max_day'
        'Day': [1, max_day],
        'Total Budget': [monthly_budget, monthly_budget]
    })

    # Adds a column called 'status' to the daily_spending dataFrame
    daily_spending['Status'] = daily_spending['Cumulative Spending'].apply(
        # The lambda keyword creates an anonymous (inline) function
        # x: The input value (each value in the Cumulative Spending column).
        lambda x: 'Under' if x <= monthly_budget else 'Over'
    )

    print("daily_spending: ")
    print(daily_spending[:5])

    over_index = daily_spending[daily_spending['Status'] == 'Over'].index.min()

    # If there is an 'Over' index, create two segments: 'Under' and 'Over'
    if not pd.isna(over_index):
        under_spending = daily_spending.loc[:over_index]
        # .copy ensures that modifications to over_spending doesn't affect daily_spending
        over_spending = daily_spending.loc[over_index-1:].copy()
        # ensures that the first row of the over_spending DataFrame is correctly labeled as 'Over'
        over_spending.iloc[0, daily_spending.columns.get_loc('Status')] = 'Over'
        # 1 for over_spending[1:] ensures that the first row is not duplicated  
        combined_spending = pd.concat([under_spending, over_spending[1:]])
    else:
        combined_spending = daily_spending

    fig = px.line(
        combined_spending,
        x='Day',
        y='Cumulative Spending',
        labels={
            'Cumulative Spending': 'cumulative spending ($)',
            'Day': 'day'
        },
        color='Status',
        color_discrete_map={'Under': 'green', 'Over': 'red'},
        markers=True
    )

    # Add the 'Over' segment if it exists
    if not over_spending.empty:
        fig.add_scatter(
            x=over_spending['Day'], 
            y=over_spending['Cumulative Spending'], 
            mode='lines+markers', 
            name='Over', 
            line=dict(color='red', 
            width=3), 
            showlegend= False)
        
    # Add budget line to the same figure
    fig.add_scatter(
        x=budget_line['Day'], 
        y=budget_line['Total Budget'], 
        mode='lines', 
        name='Monthly Budget', 
        line=dict(
            color='#f8d44c', 
            dash='dash',
            width=5
        )
    )

    fig.update_traces(
        line=dict(width=3)
    ) 

    # Customize the plot
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),  # Left, Right, Top, Bottom margins in pixels

        xaxis_tickangle=0,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(1, max_day + 1, 1)),  # Tick every day
            tickfont=dict(
                size=10,
                color="#eeeee4"
            ),
            title_font=dict(
                color="#eeeee4"),
            showgrid=False
        ),
        yaxis=dict(
            title_font=dict(color="#eeeee4"),
            tickfont=dict(color="#eeeee4"),
            showgrid=True,
            gridcolor='lightblue'
        ),
        legend=dict(
            title='',
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
            font=dict(
                color="#eeeee4",
                size=12
            )
        )
    )

    return fig

def update_budget_vs_actual_spending_graph(filtered_df, categorical_budgets_df):
    # Merge actual spending data with budgets data
    actual_spending = filtered_df.groupby('categoryname')['amount'].sum().reset_index()
    budget_data = categorical_budgets_df[['categoryname', 'categorybudget']].groupby('categoryname').sum().reset_index() 
    
    # Merging the actual spending with the budgets
    summary_df = pd.merge(budget_data, actual_spending, on='categoryname', how='left')
    summary_df.fillna(0, inplace=True)  # Replace NaN with 0 for categories with no spending

    summary_df.rename(columns={'categorybudget': 'Budget', 'amount': 'Spent'}, inplace=True)

    # Create the bar chart for Budget vs Actual Spending
    fig = px.bar(
        summary_df, 
        x='categoryname', 
        y=['Budget', 'Spent'],
        labels={
            'categoryname': 'category types',
            'value': 'amount ($)', #represented with 2 different y-values, so is labeled as 'value'
            'variable': '' #represented with 2 different y-values, so is labeled as 'value'
        },
        barmode='group',
        color_discrete_sequence=["#92154f", "#f19500"]  # Blue for Budget, Red for Actual Spending
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis_tickangle=45,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',

        legend = dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(
                color="#eeeee4",
                size=12
            )
        ),
        xaxis=dict(
            title_font=dict(color="#eeeee4"),  # Color for the X-axis title
            tickfont=dict(
                color="#eeeee4",
                size=11
                ),  # Color for the X-axis ticks
            showgrid=True,  # Determines whether or not grid lines are drawn
            gridcolor='rgba(0,0,0,0)'  # Color of grid lines
        ),
        yaxis=dict(
            title_font=dict(color="#eeeee4"),  # Color for the Y-axis title
            tickfont=dict(color="#eeeee4"),  # Color for the Y-axis ticks
            showgrid=True,  # Determines whether or not grid lines are drawn
            gridcolor='lightblue'  # Color of grid lines
        )
    )
                 
    return fig

# ------------------------------------------------------------------------------
# Callback for adding transactions
@app.callback(
    Output('transaction_status', 'children'),
    [Input('submit_transaction', 'n_clicks')],
    [State('input_date', 'date'), 
     State('input_amount', 'value'), 
     State('input_category', 'value'), 
     State('input_description', 'value')]
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
            'date': date + ' 00:00:00',
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
# Update the budget overview when a new month is selected
@app.callback(
    [Output('budget_overview', 'children'),
     Output('input_total_budget', 'value'),
     Output('budget_table', 'data'),
     Output('unallocated_budget', 'children')],
    [Input('slct_budget_month', 'value'),
     Input('slct_budget_year', 'value'),
     Input('update_trigger', 'children')]
)

def display_budget_overview(selected_month, selected_year, _):
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
    budget_table_data = categorical_budgets_df.to_dict('records')

    # Calculate the unallocated budget
    allocated_budget = categorical_budgets_df['categorybudget'].sum()
    unallocated_budget = int(total_budget - allocated_budget)

    # Customize the display message based on the budget surplus/deficit
    if unallocated_budget < 0:
        unallocated_budget_display = f"Exceeding Monthly Budget by ${-unallocated_budget}"
    elif unallocated_budget > 0:
        unallocated_budget_display = f"Remaining Monthly Budget of ${unallocated_budget}"
    else:
        unallocated_budget_display = f"${total_budget} Budget Fully Allocated"

    return budget_overview, total_budget, budget_table_data, unallocated_budget_display

# ------------------------------------------------------------------------------
# Update the total budget when a new total budget is submitted
@app.callback(
    Output('total_budget_status', 'children'),
    [Input('submit_total_budget', 'n_clicks')],
    [State('slct_budget_month', 'value'), 
     State('slct_budget_year', 'value'), 
     State('input_total_budget', 'value')]
)

def update_total_budget(n_clicks, selected_month, selected_year, total_budget):
    if n_clicks > 0:
        if total_budget is None or total_budget == '':
            return "Please enter a total budget"

        # Convert the selected month and year to a datetime object
        selected_date = pd.to_datetime(f'{selected_year}-{selected_month:02d}-01')

        # Load the latest budgets DB before updating
        monthly_budgets_df = pd.read_csv('../localdb/monthlybudgets.csv', parse_dates=['budgetmonth'])

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

        # Save the updated DataFrame to the CSV file
        monthly_budgets_df.to_csv('../localdb/monthlybudgets.csv', index=False)

        return "Total budget updated successfully!"
    return ""

# ------------------------------------------------------------------------------
# Update the category budget when a new category budget is submitted
@app.callback(
    Output('category_budget_status', 'children'),
    [Input('submit_category_budget', 'n_clicks')],
    [State('budget_category_dropdown', 'value'), 
     State('budget_category_input', 'value')]
)

def update_category_budget(n_clicks, selected_category, new_category_budget):
    if n_clicks > 0:
        if selected_category and new_category_budget is not None:
            # Load the latest categorical budgets DB before updating
            categorical_budgets_df = pd.read_csv('../localdb/categoricalbudgets.csv')

            # Update the selected category's budget
            categorical_budgets_df.loc[categorical_budgets_df['categoryname'] == selected_category, 'categorybudget'] = new_category_budget

            # Save the updated DataFrame to the CSV file
            categorical_budgets_df.to_csv('../localdb/categoricalbudgets.csv', index=False)

            return "Category budget updated successfully!"
        elif not selected_category:
            return "Please select a category"
        elif new_category_budget is None:
            return "Please enter a budget amount"
    return ""

# ------------------------------------------------------------------------------
# Force an update to the budget table when a new category budget is submitted
@app.callback(
    Output('update_trigger', 'children'),
    [Input('submit_total_budget', 'n_clicks'),
     Input('submit_category_budget', 'n_clicks')]
)

def trigger_update(total_budget_clicks, category_budget_clicks):
    return total_budget_clicks + category_budget_clicks

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)