from dash import html, dcc, dash_table
from load_data import current_year, monthsToInt

def spendings_page(categories_df, categorical_budgets_df):
    return html.Div(id='spendings_page', children=[
        html.Div([
            html.H1("Financial Management"),
            html.P('Enter your expenses and customize your budget categories on this page to keep your finances organized and under control.'),
            html.Div([
                html.Div([
                    html.H2("Add Transaction"),
                    html.Div([    
                        html.H3('Select date'),
                        dcc.DatePickerSingle(
                            id='input_date',
                            placeholder='YYYY-MM-DD',
                            display_format='YYYY-MM-DD',
                        ),
                    ],className='spendings-input'),
                    html.Div([    
                        html.H3('Amount'),
                        dcc.Input(
                            id='input_amount',
                            type='number',
                            min=0,
                            placeholder='enter amount',
                        ),
                    ],className='spendings-input'),
                    html.Div([    
                        html.H3('Category'),
                        dcc.Dropdown(
                            id='input_category',
                            options=[{'label': category, 'value': category} for category in categories_df['name']],
                            placeholder='select category',
                        ),
                    ],className='spendings-input'),
                    html.Div([    
                        html.H3('Description'),
                        dcc.Input(
                            id='input_description',
                            type='text',
                            placeholder='enter description',
                        ),
                    ],className='spendings-input'),

                    html.Button('ADD', id='submit_transaction', n_clicks=0),
                    html.Div(id='transaction_status', className='spendings-transaction-status-message'),  # Display the status of the transaction   
                ], className= 'spendings-add-transaction'),
                
                html.Div(className= 'settings-border-lines'),
                html.Div([
                    html.H2("Manage Monthly Budget"),
                
                    html.Div([
                        html.H3("Month"),
                        dcc.Dropdown(id="slct_budget_month",
                                    options=[{'label': key, 'value': value} for key, value in monthsToInt().items()],
                                    multi=False,
                                    placeholder='select month'
                                    )
                    ], className='spendings-manage-option'),

                    html.Div([
                        html.H3("Year"),
                        dcc.Dropdown(id="slct_budget_year",
                                    options=[{'label': year, 'value': year} for year in range(2023 , (current_year()+1)+1)],
                                    multi=False,
                                    placeholder='select year'
                                    )
                    ], className='spendings-manage-option'),
                    
                    html.Div([
                        html.H3("Budget"),
                        dcc.Input(
                            id='input_total_budget',
                            type='number',
                            min=0,
                            placeholder='enter budget'
                        )
                    ], className='spendings-manage-option'),                    
                    html.Div(id='total_budget_status', className='spendings-budget-status-message'),
                    html.Div([
                        html.Button('UPDATE', id='submit_total_budget', n_clicks=0),
                    ], className='spendings-manage-confirm'),
                    html.Div(id='monthly_budget_status'),
                ], className= 'spendings-manage-budget'),

                html.Div(className= 'settings-border-lines'),
                
                html.Div([
                    html.H2('Manage Category Budget'),
                    html.Div([
                        html.H3('category'),
                        dcc.Dropdown(
                            id='budget_category_dropdown',
                            options=[{'label': category, 'value': category} for category in categorical_budgets_df['categoryname']],
                            placeholder='select category'
                        ),
                    ], className='spendings-input-category'), 
                    html.Div([    
                            html.H3('budget'),
                            dcc.Input(
                                id='budget_category_input',
                                type='number',
                                min=0,
                                placeholder='enter Budget',
                            ),                    
                    ], className='spendings-input-category'),

                    html.Div([
                        html.Button('SET', id='submit_category_budget', n_clicks=0)
                    ], className='spendings-buttom-bottom-btn'),
                    html.Div(id='category_budget_status', className= 'spendings-category-message')
                ], className='spendings-bottom-right'),
                
                html.Div(className= 'settings-border-lines'),
                
                html.Div([
                    html.H2('Budget Overview'),
                    dash_table.DataTable(
                        id='budget_table',
                        columns=[
                            {'name': 'Category', 'id': 'categoryname', 'type': 'text'},
                            {'name': 'Budget', 'id': 'categorybudget', 'type': 'numeric', 'editable': True}
                        ],
                        data=[]
                    ),
                    html.Div(id='budget_overview_status', className='spendings-budget-allocation')
                ], className='spendings-budget-overview'),

            # Hidden div to store update triggers
                html.Div(id='update_trigger', style={'display': 'none'}),
                html.Img(src="/assets/pencil.png", alt='question mark', className='spendings-art'),
            ], className= 'spendings-container'),    

        ], className='spendings')

    ], className='spendings-page')