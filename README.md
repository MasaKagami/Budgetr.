
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