
# Budgetr: Personal Finance Dashboard
**An Interactive Dashboard for Budgeting and Expense Tracking**

## Project Overview
Budgetr is a personal finance dashboard designed to empower users in managing budgets, tracking expenses, and visualizing financial data. This user-friendly platform integrates secure data handling with dynamic visualizations, allowing users to gain insights into their financial habits and progress toward their financial goals.

### Technologies and Tools
- **Frontend**: Plotly and Dash for visualizations and dynamic user interfaces.
- **Backend**: Flask for routing, server-side caching, and session management.
- **Database**: PostgreSQL for reliable and secure data storage, with SQLAlchemy for ORM.
- **Deployment**: Render with Gunicorn for continuous uptime and efficient load handling.

## Key Features
- **Dynamic Dashboard**: Built with Plotly for interactive financial data visualization, enabling users to monitor budgets and expenses through engaging charts.
- **Flexible Budget Tracking**: Supports monthly or annual budgets, with customizable categories and rollover functionality to adapt to unique spending patterns.
- **Enhanced Performance**: Flask-based server-side caching and session management accelerate page load speeds by over 1500%, improving user experience.
- **Secure Data Handling**: Provides secure user authentication and data encryption to protect sensitive financial data.
- **Deployment and Availability**: Hosted on Render with Gunicorn for 24/7 availability and seamless backend performance.

---

## User Interface
The Budgetr interface provides several key sections that help users manage and track their finances:

1. **Dashboard**:
   The main dashboard offers an overview of financial metrics, including monthly spending trends, budget vs. spending by category, and recent transactions.
   ![Budgetr Dashboard](https://github.com/user-attachments/assets/aa23d2d1-d747-43fc-9857-7bf48cd348fa)


2. **Manage Finance**:
   Users can add transactions, set monthly budgets, and customize their category budgets. This section allows users to input specific details, such as date, category, amount, and description, making it easy to keep track of expenses.
   ![Budgetr Financial Management](https://github.com/user-attachments/assets/623a3b3c-0296-4185-87a2-8336978c56d5)


3. **Support**:
   The support page allows users to reach out for assistance or provide feedback. This feature ensures that users can communicate any issues or inquiries directly through the platform.
   ![Budgetr Support](https://github.com/user-attachments/assets/b99ff550-2eb0-42c7-be9b-75eebd3272e0)
   

5. **Performance Alerts**:
   The dashboard visually indicates financial performance, with clear indicators (e.g., "CRITICAL" status) to help users understand their current financial status.
   ![Budgetr Dashboard - Critical](https://github.com/user-attachments/assets/5c5a1208-a730-46f9-9749-adf2bd3d052d)

---

## Architecture
1. **Data Visualization**:
   - Plotly is used to render a variety of interactive graphs and charts, such as line, bar, and pie charts, to track expenses and budget utilization across categories.
   - Users can gain insights from cumulative spending, average expenses, budget utilization percentage, and top spending categories.
2. **User Authentication and Security**:
   - Secure login system with password hashing and session management.
   - All sensitive data, including financial transactions, are encrypted for protection.
3. **Budget Management**:
   - Users can set, monitor, and adjust budgets by month or year, with flexibility to adjust allocations.
   - Automatic rollover of unused budget for consistent financial management.
4. **Performance Optimization**:
   - Server-side caching minimizes database load, and session management streamlines the user experience.

--- 

## Installation and Setup
1. **Create a Virtual Environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # For Windows
   source .venv/bin/activate    # For MacOS/Linux
   ```

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/shyamddesai/Budgetr..git
   cd Budgetr.
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup** (Optional):
   - To set up the  PostgreSQL database, run `setup.sql`:
     ```bash
     psql -U your_username -d budgetr_db -f setup.sql
     ```
   - If PostgreSQL is unavailable, the application will use a local database of `.csv` files in the `localdb` folder as a fallback.

5. **Run the Application**:
   ```bash
   python myfinanceplanner.py
   ```

---

## Future Enhancements
- **Automated Alerts**: Notifications to inform users when they approach their budget limits.
- **Role-Based Analytics**: Customizable dashboards with targeted insights based on user preferences.
- **Bank Integration**: Sync with banking APIs for automatic expense tracking.
