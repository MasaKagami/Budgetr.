from dash import Output, Input, State
import pandas as pd
from load_data import (userid, load_local_categories, load_local_transactions, load_local_monthly_budgets, 
                       load_local_categorical_budgets, load_transactions, load_monthly_budgets, 
                       load_categorical_budgets, save_transactions, save_local_transactions, 
                       save_monthly_budgets, save_local_monthly_budgets, save_categorical_budgets, 
                       save_local_categorical_budgets)

def spendings_callback(app, use_remote_db=False):
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
            if use_remote_db:
                transactions_df = load_transactions()
            else:
                transactions_df = load_local_transactions()

            # Add the new transaction to the DataFrame
            new_transaction = {
                'transactionid': transactions_df['transactionid'].max() + 1, # Increment the transaction ID
                'userid': userid(),
                'date': date + ' 00:00:00',
                'categoryname': category,
                'amount': amount, 
                'description': description
                }
            
            # Save the updated data to the database
            if use_remote_db:
                save_transactions(new_transaction)
            else:
                transactions_df.loc[len(transactions_df)] = new_transaction # Append the new transaction to the DataFrame
                save_local_transactions(transactions_df)

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
        [Output('monthly_budget_status', 'children'),
        Output('budget_table', 'data'),
        Output('budget_overview_status', 'children')],
        [Input('slct_budget_month', 'value'),
        Input('slct_budget_year', 'value'),
        Input('update_trigger', 'children')]
    )

    def display_budget(selected_month, selected_year, _):
        # Load the latest budgets DB for the logged in user
        if use_remote_db:
            monthly_budgets_df = load_monthly_budgets()
            categorical_budgets_df = load_categorical_budgets()
        else:
            monthly_budgets_df = load_local_monthly_budgets()
            categorical_budgets_df = load_local_categorical_budgets()

        monthly_budgets_df = monthly_budgets_df[monthly_budgets_df['userid'] == userid()]
        categorical_budgets_df = categorical_budgets_df[categorical_budgets_df['userid'] == userid()]
        
        # ------------------------------------------------------------------------------
        # Monthly Budget

        if selected_month and selected_year:
            # Convert the selected month and year to a datetime object if valid selections
            selected_date = pd.to_datetime(f'{selected_year}-{selected_month:02d}-01')

            # Filter the monthly budgets for the selected date
            monthly_budget_row = monthly_budgets_df[monthly_budgets_df['budgetmonth'] == selected_date]

            # Display the total budget for the selected month, if not found show 0
            if monthly_budget_row.empty:
                total_budget = 0
            else:
                total_budget = int(monthly_budget_row['totalbudget'].values[0])

            # Display the monhtly budget status message
            monthly_budget_status = f"Your current budget for {selected_date.strftime('%B %Y')} is ${total_budget}"
        else:
            # Display the last budget entry date if no month is selected
            last_entry_date = monthly_budgets_df['budgetmonth'].max()

            # If a budget entry is found, display the last entry month in the status message
            if last_entry_date is not pd.NaT:
                last_entry_month = last_entry_date.strftime('%B %Y')
                monthly_budget_status = f"Your last budget entry was in {last_entry_month}"
            else:
                monthly_budget_status = "No past budget entries found"    

        # ------------------------------------------------------------------------------
        # Budget Overview

        # Display the allocated budget for each category
        budget_table_data = categorical_budgets_df.to_dict('records')

        # If no data is found, load the categories and set the budget to 0
        if categorical_budgets_df.empty:
            categories_df = load_local_categories()
            for categories in categories_df['name']:
                budget_table_data.append({'categoryname': categories, 'categorybudget': 0})

        # Hide the budget overview display message if no month is selected
        if not(selected_month and selected_year):
            budget_overview_status = ""
            return monthly_budget_status, budget_table_data, budget_overview_status
        
        # Calculate the unallocated budget based on the total budget and category budgets
        unallocated_budget = int(total_budget - categorical_budgets_df['categorybudget'].sum())

        # Customize the budget overview display message based on the budget surplus/deficit
        if unallocated_budget < 0:
            budget_overview_status = f"Exceeding current monthly budget by ${-unallocated_budget}"
        elif unallocated_budget > 0:
            budget_overview_status = f"Remaining monthly budget of ${unallocated_budget}"
        else:
            budget_overview_status = f"${total_budget} Budget Fully Allocated"

        return monthly_budget_status, budget_table_data, budget_overview_status

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
            if use_remote_db:
                monthly_budgets_df = load_monthly_budgets()
            else:
                monthly_budgets_df = load_local_monthly_budgets()

            # Filter for the current user and selected date
            user_budget_df = monthly_budgets_df[(monthly_budgets_df['userid'] == userid()) 
                                                & (monthly_budgets_df['budgetmonth'] == selected_date)]

            if not user_budget_df.empty:
                if int(total_budget) == 0:
                    # Remove the total budget for the selected month if set to 0
                    monthly_budgets_df = monthly_budgets_df[monthly_budgets_df.index != user_budget_df.index[0]]
                else:
                    # Update the total budget for the selected month
                    monthly_budgets_df.loc[user_budget_df.index, 'totalbudget'] = total_budget
            else:
                new_monthly_budget = {
                    'budgetid': monthly_budgets_df['budgetid'].max() + 1,
                    'userid': userid(),
                    'totalbudget': total_budget,
                    'budgetmonth': selected_date
                }
                monthly_budgets_df.loc[len(monthly_budgets_df)] = new_monthly_budget

            # Save the updated data to the database
            if use_remote_db:
                save_monthly_budgets(monthly_budgets_df)
            else:
                save_local_monthly_budgets(monthly_budgets_df)

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
                if use_remote_db:
                    categorical_budgets_df = load_categorical_budgets()
                else:
                    categorical_budgets_df = load_local_categorical_budgets()

                # Filter for the user and selected category
                user_category_df = categorical_budgets_df[(categorical_budgets_df['userid'] == userid()) 
                                                          & (categorical_budgets_df['categoryname'] == selected_category)]

                # Update the selected category's budget for the logged in user
                if not user_category_df.empty:
                    categorical_budgets_df.loc[user_category_df.index, 'categorybudget'] = new_category_budget
                else:
                    new_category_budget_row = {
                        'catbudgetid': categorical_budgets_df['catbudgetid'].max() + 1,
                        'userid': userid(),
                        'categoryname': selected_category,
                        'categorybudget': new_category_budget
                    }
                    categorical_budgets_df.loc[len(categorical_budgets_df)] = new_category_budget_row

                # Save the updated data to the database
                if use_remote_db:
                    save_categorical_budgets(categorical_budgets_df)
                else:
                    save_local_categorical_budgets(categorical_budgets_df)

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