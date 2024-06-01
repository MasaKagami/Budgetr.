from dash import html, dcc, dash_table
import pandas as pd
from load_data import current_month, current_year, monthsToInt

def spendings_page(categories_df, categorical_budgets_df):
    return html.Div(id='spendings_page', children=[
        html.Div([
            html.Div([
                html.H1("Add Transaction"),
                html.Div([    
                    html.H2('select date'),
                    dcc.DatePickerSingle(
                        id='input_date',
                        # date=pd.Timestamp.now().strftime('%Y-%m-%d'),
                        placeholder='YYYY-MM-DD',
                        display_format='YYYY-MM-DD',
                    ),
                ],className='spendings-input'),
                html.Div([    
                    html.H2('enter amount'),
                    dcc.Input(
                        id='input_amount',
                        type='number',
                        min=0,
                        placeholder='0000.00',
                    ),
                ],className='spendings-input'),
                html.Div([    
                    html.H2('select category'),
                    dcc.Dropdown(
                        id='input_category',
                        options=[{'label': category, 'value': category} for category in categories_df['name']],
                        placeholder='select.',
                    ),
                ],className='spendings-input'),
                html.Div([    
                    html.H2('enter description'),
                    dcc.Input(
                        id='input_description',
                        type='text',
                        placeholder='groceries',
                    ),
                ],className='spendings-input'),


                html.Button('Add Transaction', id='submit_transaction', n_clicks=0),
                html.Div(id='transaction_status'),  # Display the status of the transaction   
            ], className= 'spendings-add-transaction'),

            html.Div([
                html.H1("Manage Budget"),
            
                html.Div([
                    html.H2("select month:"),
                    dcc.Dropdown(id="slct_budget_month",
                                options=[{'label': key, 'value': value} for key, value in monthsToInt().items()],
                                multi=False,
                                value=current_month() # Initial value
                                )
                ], className='spendings-manage-option'),

                html.Div([
                    html.H2("select year:"),
                    dcc.Dropdown(id="slct_budget_year",
                                options=[{'label': year, 'value': year} for year in range(2000, current_year() + 1)],
                                multi=False,
                                value=current_year() # Initial value
                                )
                ], className='spendings-manage-option'),
                
                html.Div([
                    html.H2("set budget:"),
                    dcc.Input(
                        id='input_total_budget',
                        type='number',
                        min=0,
                        placeholder='9999',
                    )
                ], className='spendings-manage-option'),                    



                html.Div(id='budget_overview'),
                html.Button('Update Total Budget', id='submit_total_budget', n_clicks=0),
                html.Div(id='total_budget_status')

            ], className= 'spendings-manage-budget')

        ], className= 'spendings-top'),    
        


        









        html.Div([

        
            html.Div([
                html.H1('Budget Overview'),
                dash_table.DataTable(
                    id='budget_table',
                    columns=[
                        {'name': 'Category', 'id': 'categoryname', 'type': 'text'},
                        {'name': 'Budget', 'id': 'categorybudget', 'type': 'numeric', 'editable': True}
                    ],
                    data=[],
                    style_table={'width': '100%', 'margin': 'auto'},
                    style_cell={'textAlign': 'left', 'color': 'black'}
                )
            ], className='spendings-budget-overview'),

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
        ], className='spendings-bottom'),


        # Hidden div to store update triggers
        html.Div(id='update_trigger', style={'display': 'none'})
    ], className='spendings-page')