from dash import html, dcc, dash_table
import pandas as pd
from load_data import current_month, current_year, monthsToInt

def spendings_page(categories_df, categorical_budgets_df):
    return html.Div(id='spendings_page', children=[
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
                        options=[{'label': key, 'value': value} for key, value in monthsToInt().items()],
                        multi=False,
                        value=current_month(), # Initial value
                        style={'width': "150px", 'margin': '10px auto'}
                        ),
            dcc.Dropdown(id="slct_budget_year",
                        options=[{'label': year, 'value': year} for year in range(2000, current_year() + 1)],
                        multi=False,
                        value=current_year(), # Initial value
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
    ], className='spendingsContainer') # spendingsContainer doesn't exist in the CSS file yet