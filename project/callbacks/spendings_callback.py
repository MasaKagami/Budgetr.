from dash import Output, Input, State
import pandas as pd

def spendings_callback(app, transactions_df, categories_df, categorical_budgets_df, monthsToInt):
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