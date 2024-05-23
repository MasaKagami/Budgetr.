from turtle import width
from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
from dash import dash_table, Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
from datetime import datetime

app = Dash(__name__)

# -- Import and clean data (importing csv into pandas)
def prepare_transactions_data(transactions_df):
    transactions_df['date'] = pd.to_datetime(transactions_df['date'])
    transactions_df['date_display'] = transactions_df['date'].dt.strftime('%Y-%m-%d')
    transactions_df.sort_values('date', ascending=False, inplace=True)  # Sort by date descending
    return transactions_df

def load_data():
    DATABASE_URL = "postgresql://postgresql_finance_user:Xda6CRIftQmupM1vnXit1fnbKIfcfLhc@dpg-cp1p0hud3nmc73b8v0qg-a.ohio-postgres.render.com:5432/postgresql_finance"
    #creating an SQLAlchemy engine
    engine = create_engine(DATABASE_URL)
    
    #load transactions
    transactions_query = "SELECT * FROM Transactions;"
    transactions_df = pd.read_sql(transactions_query, engine, parse_dates=['date'])

    #load monthly budgets
    monthly_budgets_query = "SELECT * FROM MonthlyBudgets;"
    monthly_budgets_df = pd.read_sql(monthly_budgets_query, engine)

    #load categorical budgets
    categorical_budgets_query = "SELECT * FROM CategoricalBudgets;"
    categorical_budgets_df = pd.read_sql(categorical_budgets_query, engine)

    #close connection
    engine.dispose()

    transactions_df = prepare_transactions_data(transactions_df)

    return transactions_df, monthly_budgets_df, categorical_budgets_df

transactions_df, monthly_budgets_df, categorical_budgets_df = load_data()
print("transactions_df: ")
print(transactions_df[:5])
print("monthly_budgets_df: ")
print(monthly_budgets_df[:5])
print("categorical_budgets_df: ")


print(categorical_budgets_df[:5])

# ------------------------------------------------------------------------------
# App layout

app.layout = html.Div([
    html.Link(
        href='https://fonts.googleapis.com/css2?family=Lexend:wght@100..900&display=swap',
        rel='stylesheet'
    ),
    html.Div([
        html.Button("☰")
    ]),

    html.Div([
        html.H1("MyFINANCE DASHBOARD", className = 'header'),
        html.Div([
            html.H4("Select Year and Month: "),
            dcc.Dropdown(
                id="slct_year",
                options=[
                    {'label': str(year), 'value': year} for year in range(2000, datetime.now().year + 1)
                ],
                multi=False,
                value=datetime.now().year-1,  # Default to current year
            className='dropdownYear'),
            
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
                value=1,
                className='dropdownMonth'),
        ], className='selectYearandMonth'),
        
        html.Div([
            html.Button('INPUT SPENDINGS', id='input_spendings'),
            html.Button('VIEW DASHBOARD', id='view_dashboard')
        ], className= 'button'),

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
                ], className= 'financial-overview'),

                html.Div([
                    html.H3("Expense Cateogrization", className='dataTitle'),
                    dcc.Graph(id='expense_categorization_graph', figure={}),
                ], className= 'expense-categorization')
            ], className= 'section3'),

            html.Div([
                html.Div([
                    html.Div([
                        html.H3("Daily Spending Trend", className='dataTitle'),
                        dcc.Graph(id='daily_spending_trend_graph', figure={}),
                    ], className= 'daily-spending-trend'),

                    html.Div([
                        html.H3("Budget vs. Actual Spending Per Category", className='dataTitle'),
                        dcc.Graph(id='budget_vs_actual_spending_graph', figure={}),
                    ], className= 'budget-vs-actual-spending'),

                ], className= 'section4'),
                html.Div([
                    html.H3("Recent Transactions", className = 'dataTitle'),
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
                ], className= 'section5'), 
            ], className= 'dataContainer2')

        ], className= 'dataContainer') #it contains all the data
    ], className= 'dashboard')
], className= 'background')


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [
        Output('net-balance-output', 'children'), 
        Output('status-output', 'children'),
        Output('expense_categorization_graph', 'figure'), 
        Output('daily_spending_trend_graph', 'figure'),
        Output('budget_vs_actual_spending_graph', 'figure'),
        Output('transactions_table', 'data')
    ],
    [
        Input('slct_year', 'value'),
        Input('slct_month', 'value')
    ]
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

    #same order as in the output call-back
    return net_balance_output, status_output, expense_categorization_fig, daily_spending_trend_fig, budget_vs_actual_spending_fig, transactions_table_data


def format_net_balance(net_balance):
    if net_balance < 0:
        formatted_balance = f"({-net_balance})"
    else:
        formatted_balance = str(net_balance)
    print("Formatted Balance:", formatted_balance)  # Debugging statement
    return formatted_balance


def determine_status(monthly_budget, total_spent, selected_year, selected_month):
    
    #key-value pairs
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

    category_colors = {
        "Housing": "#FF5733",           # Vibrant Red
        "Investments": "#1F77B4",       # Bright Blue
        "Debt Payments": "#2CA02C",     # Bold Green
        "Healthcare": "#9467BD",        # Medium Purple
        "Food": "#FF69B4",              # Hot Pink
        "Entertainment & Leisure": "#17BECF",  # Vibrant Teal
        "Education": "#7F7F7F",         # Neutral Gray
        "Transportation": "#C0C0C0",    # Light Silver
        "Personal Care": "#FFA500",     # Bright Orange
        "Miscellaneous": "#FF4500"      # Orange Red
    }


    fig = px.pie(
        filtered_df, 
        values='amount', 
        names='categoryname', 
        color='categoryname',
        hole=0.3,
        color_discrete_map=category_colors
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

    # is creating a new dataFrame, budget_line
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
        # 1 for ov
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
        markers=True,
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

    #add budget line to function
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
if __name__ == '__main__':
    app.run_server(debug=True)