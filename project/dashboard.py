from email import header
from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)

app = Dash(__name__)

# -- Import and clean data (importing csv into pandas)

def load_data():
    # Connection setup   
    # Database URL  
    DATABASE_URL = "postgresql://postgresql_finance_user:Xda6CRIftQmupM1vnXit1fnbKIfcfLhc@dpg-cp1p0hud3nmc73b8v0qg-a.ohio-postgres.render.com:5432/postgresql_finance"

    #creating an SQLAlchemy engine
    engine = create_engine(DATABASE_URL)
    
    # Use the engine to execute a query and load into DataFrame
    transactions_df = pd.read_sql("SELECT * FROM Transactions;", engine, parse_dates=['date'])
    engine.dispose()  # Close the connection safely

    return transactions_df

# Using the function
transactions_df = load_data()
print(transactions_df[:5])

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    html.Div([
        html.H1("My Financial Dashboard", className = 'header'),
        html.H4("Select Month", className= 'subheader'),
        dcc.Dropdown(id="slct_month",
                 options=[
                     {"label": "January", "value": 1},
                     {"label": "Febuary", "value": 2},
                     {"label": "March", "value": 3},
                     {"label": "April", "value": 4},
                     {"label": "May", "value": 5},
                     {"label": "June", "value": 6},
                     {"label": "July", "value": 7},
                     {"label": "August", "value": 8},
                     {"label": "September", "value": 9},
                     {"label": "October", "value": 10},
                     {"label": "November", "value": 11},
                     {"label": "December", "value": 12}],
                     
                 multi=False,
                 value=1, #THE VALUE
                 className='dropdown'
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_spending_map', figure={})
    ], className= 'dashboard')
], className= 'background')

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    Output('my_spending_map', 'figure'),
    [Input('slct_month', 'value')]
)
def update_graph(selected_month):

    # Filter the DataFrame to the selected month
    filtered_df = transactions_df[transactions_df['date'].dt.month == selected_month]
        
    # Group by day of the month and sum the amounts
    daily_spending = filtered_df.groupby(filtered_df['date'].dt.day)['amount'].sum().reset_index()
    daily_spending.columns = ['Day', 'Total Spent']

        # Create a line chart with Plotly Express
    fig = px.line(
        daily_spending, x='Day', y='Total Spent',
        title=f'Spending Trend for Month {selected_month}',
        labels={'Day': 'Day of the Month', 'Total Spent': 'Amount Spent ($)'},
        markers=True
        )  # markers=True makes it easier to see individual data points

    return fig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)