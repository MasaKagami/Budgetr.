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
                    html.H2('amount'),
                    dcc.Input(
                        id='input_amount',
                        type='number',
                        min=0,
                        placeholder='enter amount',
                    ),
                ],className='spendings-input'),
                html.Div([    
                    html.H2('category'),
                    dcc.Dropdown(
                        id='input_category',
                        options=[{'label': category, 'value': category} for category in categories_df['name']],
                        placeholder='select category',
                    ),
                ],className='spendings-input'),
                html.Div([    
                    html.H2('description'),
                    dcc.Input(
                        id='input_description',
                        type='text',
                        placeholder='enter description',
                    ),
                ],className='spendings-input'),


                html.Button('ADD', id='submit_transaction', n_clicks=0),
                html.Div(id='transaction_status', className='spendings-transaction-status-message'),  # Display the status of the transaction   
            ], className= 'spendings-add-transaction'),

            html.Div([
                html.H1("Manage Monthly Budget"),
            
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
                    html.H2("enter budget:"),
                    dcc.Input(
                        id='input_total_budget',
                        type='number',
                        min=0,
                        placeholder='enter budget',
                    )
                ], className='spendings-manage-option'),                    


                html.Div([
                    html.Div(id='budget_overview'),
                    html.Button('UPDATE', id='submit_total_budget', n_clicks=0),
                ], className='spendings-manage-confirm'),
                html.Div(id='total_budget_status', className='spendings-budget-status-message')                


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
                    data=[]
                ),
                html.Div(id='unallocated_budget', className='spendings-budget-allocation')
            ], className='spendings-budget-overview'),
            html.Div([
                html.H1('Set Categorical Budget'),
                html.Div([
                    html.Div([
                        html.H2('select category:'),
                        dcc.Dropdown(
                            id='budget_category_dropdown',
                            options=[{'label': category, 'value': category} for category in categorical_budgets_df['categoryname']],
                            placeholder='select',
                        ),
                    ], className='spendings-bottom-top'),
                    html.Div([
                        dcc.Input(
                            id='budget_category_input',
                            type='number',
                            min=0,
                            placeholder='Enter Budget',
                        ),
                        html.Button('SET', id='submit_category_budget', n_clicks=0)
                    
                    ], className='spendings-bottom-bottom'), 

                ], className='spendings-bottom-body'),
                html.Div(id='category_budget_status', className= 'spendings-category-message')
            ], className='spendings-bottom-right')
        ], className='spendings-bottom'),


        # Hidden div to store update triggers
        html.Div(id='update_trigger', style={'display': 'none'})
    ], className='spendings-page')