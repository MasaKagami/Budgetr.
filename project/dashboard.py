from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)

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
    budgets_df = pd.read_sql("SELECT * FROM Budgets;", engine, parse_dates=['start_date', 'end_date'])
    engine.dispose()  # Close the connection safely

    return transactions_df, categories_df, users_df, budgets_df

# Loading data
transactions_df, categories_df, users_df, budgets_df = load_data()
print('\nTRANSACTIONS DB\n', transactions_df[:5])
print('CATEGORIES DB\n', categories_df[:5])
print('USERS DB\n', users_df[:5])
print('BUDGETS DB\n', budgets_df[:5])

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

    dcc.Graph(id='my_spending_map', figure={})

])

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output('my_spending_map', 'figure')],
    [Input('chart_type', 'value'),
     Input('slct_month', 'value')]
)

def update_graph(chart_type, selected_month):
    # Hide the month selector
    #month_selector_style = {'display': 'none'}

    # Initially show the month selector
    month_selector_style = {'display': 'block'}

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
        print("\nSTACKED BAR CHART\n", daily_category_spending)

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
if __name__ == '__main__':
    app.run_server(debug=True)