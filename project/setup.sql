select *
from users;

select *
from categories;

select *
from MonthlyBudgets;

select *
from CategoricalBudgets;

select *
from transactions;

DROP TABLE Transactions;
DROP TABLE MonthlyBudgets;
DROP TABLE CategoricalBudgets;
drop TABLE Categories;
drop TABLE Users;

CREATE TABLE Users
(
    UserID SERIAL PRIMARY KEY,
    Name VARCHAR(255),
    Email VARCHAR(255),
    Password VARCHAR(255)
);

CREATE TABLE Categories
(
    Name VARCHAR(255) PRIMARY KEY
);

CREATE TABLE MonthlyBudgets
(
    BudgetID SERIAL PRIMARY KEY,
    UserID INT NOT NULL,
    TotalBudget DECIMAL(10,2),
    BudgetMonth DATE,  -- Storing only the first day of the month to represent the whole month
    FOREIGN KEY (UserID) REFERENCES Users (UserID)
);

CREATE TABLE CategoricalBudgets
(
    CatBudgetID SERIAL PRIMARY KEY,
    UserID INT NOT NULL,
    CategoryName VARCHAR(255) NOT NULL,
    CategoryBudget DECIMAL(10,2),
    FOREIGN KEY (UserID) REFERENCES Users (UserID),
    FOREIGN KEY (CategoryName) REFERENCES Categories (Name)
);

CREATE TABLE Transactions
(
    TransactionID SERIAL PRIMARY KEY,
    UserID INT NOT NULL,
    Date DATE,
    CategoryName VARCHAR(255) NOT NULL,
    Amount DECIMAL(10,2),
    Description TEXT,
    FOREIGN KEY (UserID) REFERENCES Users (UserID),
    FOREIGN KEY (CategoryName) REFERENCES Categories (Name)
);

-- Insert a user
INSERT INTO Users (Name, Email, Password) VALUES
    ('Masa Kagami', 'masa.kagami@gmail.com', 'test123');

-- Insert categories
INSERT INTO Categories (Name) VALUES
                                  ('Housing'),
                                  ('Transportation'),
                                  ('Food'),
                                  ('Healthcare'),
                                  ('Debt Payments'),
                                  ('Investments'),
                                  ('Entertainment & Leisure'),
                                  ('Personal Care'),
                                  ('Education'),
                                  ('Miscellaneous');

-- Insert Monthly Budgets
INSERT INTO MonthlyBudgets (UserID, TotalBudget, BudgetMonth) VALUES
                                                                  (1, 2000.00, '2023-01-01'),
                                                                  (1, 2000.00, '2023-02-01'),
                                                                  (1, 2000.00, '2023-03-01'),
                                                                  (1, 2000.00, '2023-04-01'),
                                                                  (1, 2000.00, '2023-05-01'),
                                                                  (1, 2000.00, '2023-06-01'),
                                                                  (1, 2000.00, '2023-07-01'),
                                                                  (1, 2000.00, '2023-08-01'),
                                                                  (1, 2000.00, '2023-09-01'),
                                                                  (1, 2000.00, '2023-10-01'),
                                                                  (1, 2000.00, '2023-11-01'),
                                                                  (1, 2000.00, '2023-12-01');

-- Insert Categorical Budgets
INSERT INTO CategoricalBudgets (UserID, CategoryName, CategoryBudget) VALUES
                                                                          (1, 'Housing', 1000.00),
                                                                          (1, 'Transportation', 100.00),
                                                                          (1, 'Food', 100.00),
                                                                          (1, 'Healthcare', 100.00),
                                                                          (1, 'Debt Payments', 300.00),
                                                                          (1, 'Investments', 100.00),
                                                                          (1, 'Entertainment & Leisure', 100.00),
                                                                          (1, 'Personal Care', 60.00),
                                                                          (1, 'Education', 100.00),
                                                                          (1, 'Miscellaneous', 40.00);

-- Insert transactions
INSERT INTO Transactions (UserID, Date, CategoryName, Amount, Description) VALUES
                                                                               (1, '2023-01-01', 'Housing', 1000, 'Rent for Jan'),
                                                                               (1, '2023-02-01', 'Housing', 1000, 'Rent for Feb'),
                                                                               (1, '2023-03-01', 'Housing', 1000, 'Rent for Mar'),
                                                                               (1, '2023-04-01', 'Housing', 1000, 'Rent for Apr'),
                                                                               (1, '2023-05-01', 'Housing', 1000, 'Rent for May'),
                                                                               (1, '2023-06-01', 'Housing', 1000, 'Rent for Jun'),
                                                                               (1, '2023-07-01', 'Housing', 1000, 'Rent for Jul'),
                                                                               (1, '2023-08-01', 'Housing', 1000, 'Rent for Aug'),
                                                                               (1, '2023-09-01', 'Housing', 1000, 'Rent for Sep'),
                                                                               (1, '2023-10-01', 'Housing', 1000, 'Rent for Oct'),
                                                                               (1, '2023-11-01', 'Housing', 1000, 'Rent for Nov'),
                                                                               (1, '2023-12-01', 'Housing', 1000, 'Rent for Dec'),

                                                                               (1, '2023-01-01', 'Transportation', 50, 'Pass'),
                                                                               (1, '2023-02-01', 'Transportation', 50, 'Pass'),
                                                                               (1, '2023-03-01', 'Transportation', 50, 'Pass'),
                                                                               (1, '2023-04-01', 'Transportation', 50, 'Pass'),
                                                                               (1, '2023-05-01', 'Transportation', 50, 'Pass'),
                                                                               (1, '2023-06-01', 'Transportation', 50, 'Pass'),
                                                                               (1, '2023-07-01', 'Transportation', 50, 'Pass'),
                                                                               (1, '2023-08-01', 'Transportation', 50, 'Pass'),
                                                                               (1, '2023-09-01', 'Transportation', 50, 'Pass'),
                                                                               (1, '2023-10-01', 'Transportation', 50, 'Pass'),
                                                                               (1, '2023-11-01', 'Transportation', 50, 'Pass'),
                                                                               (1, '2023-12-01', 'Transportation', 50, 'Pass'),

                                                                               (1, '2023-01-03', 'Food', 45.00, 'Grocery shopping'),
                                                                               (1, '2023-01-05', 'Healthcare', 150.00, 'Doctor visit'),
                                                                               (1, '2023-01-08', 'Debt Payments', 200.00, 'Credit card payment'),
                                                                               (1, '2023-01-10', 'Investments', 500.00, 'Stock purchase'),
                                                                               (1, '2023-01-12', 'Entertainment & Leisure', 60.00, 'Concert tickets'),
                                                                               (1, '2023-01-15', 'Personal Care', 30.00, 'Haircut'),
                                                                               (1, '2023-01-18', 'Education', 100.00, 'Textbooks'),
                                                                               (1, '2023-01-20', 'Miscellaneous', 25.00, 'Gift for friend'),
                                                                               (1, '2023-01-22', 'Food', 75.00, 'Dining out'),
                                                                               (1, '2023-01-24', 'Healthcare', 20.00, 'Prescription medicine'),
                                                                               (1, '2023-01-26', 'Debt Payments', 150.00, 'Student loan payment'),
                                                                               (1, '2023-01-28', 'Investments', 300.00, 'Mutual fund contribution'),
                                                                               (1, '2023-01-30', 'Entertainment & Leisure', 40.00, 'Movie tickets'),
                                                                               (1, '2023-02-02', 'Personal Care', 50.00, 'New clothes'),
                                                                               (1, '2023-02-04', 'Education', 200.00, 'Online course'),
                                                                               (1, '2023-02-06', 'Miscellaneous', 15.00, 'Charity donation'),
                                                                               (1, '2023-02-08', 'Food', 60.00, 'Grocery shopping'),
                                                                               (1, '2023-02-10', 'Healthcare', 100.00, 'Dentist appointment'),
                                                                               (1, '2023-02-12', 'Debt Payments', 175.00, 'Car loan payment'),
                                                                               (1, '2023-02-14', 'Investments', 250.00, 'Savings account deposit'),
                                                                               (1, '2023-02-16', 'Entertainment & Leisure', 30.00, 'Bowling night'),
                                                                               (1, '2023-02-18', 'Personal Care', 40.00, 'Spa treatment'),
                                                                               (1, '2023-02-20', 'Education', 150.00, 'Workshop fee'),
                                                                               (1, '2023-02-22', 'Miscellaneous', 35.00, 'Pet supplies'),
                                                                               (1, '2023-02-24', 'Food', 80.00, 'Dining out'),
                                                                               (1, '2023-02-26', 'Healthcare', 25.00, 'Over-the-counter medicine'),
                                                                               (1, '2023-02-28', 'Debt Payments', 300.00, 'Personal loan payment'),
                                                                               (1, '2023-03-02', 'Investments', 400.00, 'ETF purchase'),
                                                                               (1, '2023-03-04', 'Entertainment & Leisure', 20.00, 'Streaming service'),
                                                                               (1, '2023-03-06', 'Personal Care', 25.00, 'Manicure'),
                                                                               (1, '2023-03-08', 'Education', 75.00, 'Online seminar'),
                                                                               (1, '2023-03-10', 'Miscellaneous', 10.00, 'Lottery tickets'),
                                                                               (1, '2023-03-12', 'Food', 55.00, 'Grocery shopping'),
                                                                               (1, '2023-03-14', 'Healthcare', 80.00, 'Optometrist visit'),
                                                                               (1, '2023-03-16', 'Debt Payments', 250.00, 'Credit card payment'),
                                                                               (1, '2023-03-18', 'Investments', 350.00, 'IRA contribution'),
                                                                               (1, '2023-03-20', 'Entertainment & Leisure', 50.00, 'Theater tickets'),
                                                                               (1, '2023-03-22', 'Personal Care', 35.00, 'Haircut'),
                                                                               (1, '2023-03-24', 'Education', 100.00, 'Course materials'),
                                                                               (1, '2023-03-26', 'Miscellaneous', 20.00, 'Parking fees'),
                                                                               (1, '2023-03-28', 'Food', 90.00, 'Dining out'),
                                                                               (1, '2023-03-30', 'Healthcare', 50.00, 'Chiropractor visit'),
                                                                               (1, '2023-04-02', 'Debt Payments', 100.00, 'Credit card payment'),
                                                                               (1, '2023-04-04', 'Investments', 150.00, 'Stock purchase'),
                                                                               (1, '2023-04-06', 'Entertainment & Leisure', 70.00, 'Amusement park tickets'),
                                                                               (1, '2023-04-08', 'Personal Care', 45.00, 'Gym membership'),
                                                                               (1, '2023-04-10', 'Education', 90.00, 'Webinar fee'),
                                                                               (1, '2023-04-12', 'Miscellaneous', 30.00, 'Pet grooming'),
                                                                               (1, '2023-04-14', 'Food', 65.00, 'Grocery shopping'),
                                                                               (1, '2023-04-16', 'Healthcare', 120.00, 'Specialist consultation'),
                                                                               (1, '2023-04-18', 'Debt Payments', 200.00, 'Student loan payment'),
                                                                               (1, '2023-04-20', 'Investments', 500.00, 'Cryptocurrency investment'),
                                                                               (1, '2023-04-22', 'Entertainment & Leisure', 60.00, 'Sporting event tickets'),
                                                                               (1, '2023-04-24', 'Personal Care', 35.00, 'Hair products'),
                                                                               (1, '2023-04-26', 'Education', 110.00, 'Conference registration'),
                                                                               (1, '2023-04-28', 'Miscellaneous', 25.00, 'Office supplies'),
                                                                               (1, '2023-04-30', 'Food', 75.00, 'Dining out'),
                                                                               (1, '2023-05-02', 'Healthcare', 130.00, 'Physical therapy'),
                                                                               (1, '2023-05-04', 'Debt Payments', 150.00, 'Credit card payment'),
                                                                               (1, '2023-05-06', 'Investments', 250.00, 'Real estate crowdfunding'),
                                                                               (1, '2023-05-08', 'Entertainment & Leisure', 45.00, 'Concert tickets'),
                                                                               (1, '2023-05-10', 'Personal Care', 40.00, 'Facial treatment'),
                                                                               (1, '2023-05-12', 'Education', 120.00, 'Certification exam fee'),
                                                                               (1, '2023-05-14', 'Miscellaneous', 50.00, 'Home improvement supplies'),
                                                                               (1, '2023-05-16', 'Food', 60.00, 'Grocery shopping'),
                                                                               (1, '2023-05-18', 'Healthcare', 70.00, 'Therapist session'),
                                                                               (1, '2023-05-20', 'Debt Payments', 100.00, 'Credit card payment'),
                                                                               (1, '2023-05-22', 'Investments', 400.00, 'Index fund purchase'),
                                                                               (1, '2023-05-24', 'Entertainment & Leisure', 35.00, 'Bowling night'),
                                                                               (1, '2023-05-26', 'Personal Care', 45.00, 'New clothes'),
                                                                               (1, '2023-05-28', 'Education', 95.00, 'Online course materials'),
                                                                               (1, '2023-05-30', 'Miscellaneous', 20.00, 'Pet toys'),
                                                                               (1, '2023-06-02', 'Food', 55.00, 'Dining out'),
                                                                               (1, '2023-06-04', 'Healthcare', 85.00, 'Optometrist visit'),
                                                                               (1, '2023-06-06', 'Debt Payments', 200.00, 'Car loan payment'),
                                                                               (1, '2023-06-08', 'Investments', 150.00, 'Savings bond purchase'),
                                                                               (1, '2023-06-10', 'Entertainment & Leisure', 50.00, 'Theater tickets'),
                                                                               (1, '2023-06-12', 'Personal Care', 30.00, 'Haircut'),
                                                                               (1, '2023-06-14', 'Education', 80.00, 'Online seminar'),
                                                                               (1, '2023-06-16', 'Miscellaneous', 25.00, 'Gift for friend'),
                                                                               (1, '2023-06-18', 'Food', 70.00, 'Grocery shopping'),
                                                                               (1, '2023-06-20', 'Healthcare', 120.00, 'Doctor visit'),
                                                                               (1, '2023-06-22', 'Debt Payments', 175.00, 'Student loan payment'),
                                                                               (1, '2023-06-24', 'Investments', 300.00, 'Mutual fund contribution'),
                                                                               (1, '2023-06-26', 'Entertainment & Leisure', 40.00, 'Movie tickets'),
                                                                               (1, '2023-06-28', 'Personal Care', 35.00, 'Spa treatment'),
                                                                               (1, '2023-06-30', 'Education', 100.00, 'Course materials'),
                                                                               (1, '2023-07-02', 'Miscellaneous', 20.00, 'Parking fees'),
                                                                               (1, '2023-07-04', 'Food', 80.00, 'Dining out'),
                                                                               (1, '2023-07-06', 'Healthcare', 50.00, 'Chiropractor visit'),
                                                                               (1, '2023-07-08', 'Debt Payments', 100.00, 'Credit card payment'),
                                                                               (1, '2023-07-10', 'Investments', 150.00, 'Stock purchase'),
                                                                               (1, '2023-07-12', 'Entertainment & Leisure', 70.00, 'Amusement park tickets'),
                                                                               (1, '2023-07-14', 'Personal Care', 45.00, 'Gym membership'),
                                                                               (1, '2023-07-16', 'Education', 90.00, 'Webinar fee'),
                                                                               (1, '2023-07-18', 'Miscellaneous', 30.00, 'Pet grooming'),
                                                                               (1, '2023-07-20', 'Food', 65.00, 'Grocery shopping'),
                                                                               (1, '2023-07-22', 'Healthcare', 120.00, 'Specialist consultation'),
                                                                               (1, '2023-07-24', 'Debt Payments', 200.00, 'Student loan payment'),
                                                                               (1, '2023-07-26', 'Investments', 500.00, 'Cryptocurrency investment'),
                                                                               (1, '2023-07-28', 'Entertainment & Leisure', 60.00, 'Sporting event tickets'),
                                                                               (1, '2023-07-30', 'Personal Care', 35.00, 'Hair products'),
                                                                               (1, '2023-08-02', 'Education', 110.00, 'Conference registration'),
                                                                               (1, '2023-08-04', 'Miscellaneous', 25.00, 'Office supplies'),
                                                                               (1, '2023-08-06', 'Food', 75.00, 'Dining out'),
                                                                               (1, '2023-08-08', 'Healthcare', 130.00, 'Physical therapy'),
                                                                               (1, '2023-08-10', 'Debt Payments', 150.00, 'Credit card payment'),
                                                                               (1, '2023-08-12', 'Investments', 250.00, 'Real estate crowdfunding'),
                                                                               (1, '2023-08-14', 'Entertainment & Leisure', 45.00, 'Concert tickets'),
                                                                               (1, '2023-08-16', 'Personal Care', 40.00, 'Facial treatment'),
                                                                               (1, '2023-08-18', 'Education', 120.00, 'Certification exam fee'),
                                                                               (1, '2023-08-20', 'Miscellaneous', 50.00, 'Home improvement supplies'),
                                                                               (1, '2023-08-22', 'Food', 60.00, 'Grocery shopping'),
                                                                               (1, '2023-08-24', 'Healthcare', 70.00, 'Therapist session'),
                                                                               (1, '2023-08-26', 'Debt Payments', 100.00, 'Credit card payment'),
                                                                               (1, '2023-08-28', 'Investments', 400.00, 'Index fund purchase'),
                                                                               (1, '2023-08-30', 'Entertainment & Leisure', 35.00, 'Bowling night'),
                                                                               (1, '2023-09-02', 'Personal Care', 45.00, 'New clothes'),
                                                                               (1, '2023-09-04', 'Education', 95.00, 'Online course materials'),
                                                                               (1, '2023-09-06', 'Miscellaneous', 20.00, 'Pet toys'),
                                                                               (1, '2023-09-08', 'Food', 55.00, 'Dining out'),
                                                                               (1, '2023-09-10', 'Healthcare', 85.00, 'Optometrist visit'),
                                                                               (1, '2023-09-12', 'Debt Payments', 200.00, 'Car loan payment'),
                                                                               (1, '2023-09-14', 'Investments', 150.00, 'Savings bond purchase'),
                                                                               (1, '2023-09-16', 'Entertainment & Leisure', 50.00, 'Theater tickets'),
                                                                               (1, '2023-09-18', 'Personal Care', 30.00, 'Haircut'),
                                                                               (1, '2023-09-20', 'Education', 80.00, 'Online seminar'),
                                                                               (1, '2023-09-22', 'Miscellaneous', 25.00, 'Gift for friend'),
                                                                               (1, '2023-09-24', 'Food', 70.00, 'Grocery shopping'),
                                                                               (1, '2023-09-26', 'Healthcare', 120.00, 'Doctor visit'),
                                                                               (1, '2023-09-28', 'Debt Payments', 175.00, 'Student loan payment'),
                                                                               (1, '2023-09-30', 'Investments', 300.00, 'Mutual fund contribution'),
                                                                               (1, '2023-10-02', 'Entertainment & Leisure', 40.00, 'Movie tickets'),
                                                                               (1, '2023-10-04', 'Personal Care', 35.00, 'Spa treatment'),
                                                                               (1, '2023-10-06', 'Education', 100.00, 'Course materials'),
                                                                               (1, '2023-10-08', 'Miscellaneous', 20.00, 'Parking fees'),
                                                                               (1, '2023-10-10', 'Food', 80.00, 'Dining out'),
                                                                               (1, '2023-10-12', 'Healthcare', 50.00, 'Chiropractor visit'),
                                                                               (1, '2023-10-14', 'Debt Payments', 100.00, 'Credit card payment'),
                                                                               (1, '2023-10-16', 'Investments', 150.00, 'Stock purchase'),
                                                                               (1, '2023-10-18', 'Entertainment & Leisure', 70.00, 'Amusement park tickets'),
                                                                               (1, '2023-10-20', 'Personal Care', 45.00, 'Gym membership'),
                                                                               (1, '2023-10-22', 'Education', 90.00, 'Webinar fee'),
                                                                               (1, '2023-10-24', 'Miscellaneous', 30.00, 'Pet grooming'),
                                                                               (1, '2023-10-26', 'Food', 65.00, 'Grocery shopping'),
                                                                               (1, '2023-10-28', 'Healthcare', 120.00, 'Specialist consultation'),
                                                                               (1, '2023-10-30', 'Debt Payments', 200.00, 'Student loan payment'),
                                                                               (1, '2023-11-02', 'Investments', 500.00, 'Cryptocurrency investment'),
                                                                               (1, '2023-11-04', 'Entertainment & Leisure', 60.00, 'Sporting event tickets'),
                                                                               (1, '2023-11-06', 'Personal Care', 35.00, 'Hair products'),
                                                                               (1, '2023-11-08', 'Education', 110.00, 'Conference registration'),
                                                                               (1, '2023-11-10', 'Miscellaneous', 25.00, 'Office supplies'),
                                                                               (1, '2023-11-12', 'Food', 75.00, 'Dining out'),
                                                                               (1, '2023-11-14', 'Healthcare', 130.00, 'Physical therapy'),
                                                                               (1, '2023-11-16', 'Debt Payments', 150.00, 'Credit card payment'),
                                                                               (1, '2023-11-18', 'Investments', 250.00, 'Real estate crowdfunding'),
                                                                               (1, '2023-11-20', 'Entertainment & Leisure', 45.00, 'Concert tickets'),
                                                                               (1, '2023-11-22', 'Personal Care', 40.00, 'Facial treatment'),
                                                                               (1, '2023-11-24', 'Education', 120.00, 'Certification exam fee'),
                                                                               (1, '2023-11-26', 'Miscellaneous', 50.00, 'Home improvement supplies'),
                                                                               (1, '2023-11-28', 'Food', 60.00, 'Grocery shopping'),
                                                                               (1, '2023-11-30', 'Healthcare', 70.00, 'Therapist session'),
                                                                               (1, '2023-12-02', 'Debt Payments', 100.00, 'Credit card payment'),
                                                                               (1, '2023-12-04', 'Investments', 400.00, 'Index fund purchase'),
                                                                               (1, '2023-12-06', 'Entertainment & Leisure', 35.00, 'Bowling night'),
                                                                               (1, '2023-12-08', 'Personal Care', 45.00, 'New clothes'),
                                                                               (1, '2023-12-10', 'Education', 95.00, 'Online course materials'),
                                                                               (1, '2023-12-12', 'Miscellaneous', 20.00, 'Pet toys'),
                                                                               (1, '2023-12-14', 'Food', 55.00, 'Dining out'),
                                                                               (1, '2023-12-16', 'Healthcare', 85.00, 'Optometrist visit'),
                                                                               (1, '2023-12-18', 'Debt Payments', 200.00, 'Car loan payment'),
                                                                               (1, '2023-12-20', 'Investments', 150.00, 'Savings bond purchase'),
                                                                               (1, '2023-12-22', 'Entertainment & Leisure', 50.00, 'Theater tickets'),
                                                                               (1, '2023-12-24', 'Personal Care', 30.00, 'Haircut'),
                                                                               (1, '2023-12-26', 'Education', 80.00, 'Online seminar'),
                                                                               (1, '2023-12-28', 'Miscellaneous', 25.00, 'Gift for friend'),
                                                                               (1, '2023-12-30', 'Food', 70.00, 'Grocery shopping'),
                                                                               (1, '2023-12-31', 'Healthcare', 120.00, 'Doctor visit');