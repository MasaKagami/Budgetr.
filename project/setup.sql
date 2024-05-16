CREATE TABLE Users
(
    UserID SERIAL PRIMARY KEY,
    Name VARCHAR(255),
    Email VARCHAR(255)
);

CREATE TABLE Categories
(
    Name VARCHAR(255) PRIMARY KEY
);

CREATE TABLE Budgets
(
    BudgetID SERIAL PRIMARY KEY,
    UserID INT NOT NULL,
    TotalBudget DECIMAL(10,2),
    StartDate DATE,
    EndDate DATE,
    CategoryName VARCHAR(255) NOT NULL,
    CategoryBudget DECIMAL(10,2),
    FOREIGN KEY (UserID) REFERENCES Users (UserID)
    FOREIGN KEY (CateogryName) REFERENCES Categories (Name)
);

CREATE TABLE Transactions
(
    TransactionID SERIAL PRIMARY KEY,
    UserID INT NOT NULL,
    BudgetID INT NOT NULL,
    CategoryName VARCHAR(255) NOT NULL,
    Amount DECIMAL(10,2),
    Date DATE,
    Description TEXT,
    FOREIGN KEY (UserID) REFERENCES Users (UserID),
    FOREIGN KEY (BudgetID) REFERENCES Budgets (BudgetID),
    FOREIGN KEY (CategoryName) REFERENCES Categories (Name)
);

-- Insert a user
INSERT INTO Users (Name, Email) VALUES ('John Doe', 'john.doe@example.com');

-- Insert categories
INSERT INTO Categories (Name) VALUES
('Rent'),
('Utilities'),
('Dining'),
('Transportation'),
('Groceries'),
('Health'),
('Clothing'),
('Entertainment'),
('Education'),
('Home'),
('Pets'),
('Technology'),
('Travel'),
('Gifts'),
('Donations'),
('Services'),
('Hobbies'),
('Shopping');

-- Insert a budget
-- Insert budgets for each category
INSERT INTO Budgets (UserID, TotalBudget, StartDate, EndDate, CategoryName, CategoryBudget) VALUES
(1, 1200.00, '2023-01-01', '2023-12-31', 'Rent', 400.00),
(1, 1200.00, '2023-01-01', '2023-12-31', 'Utilities', 100.00),
(1, 1200.00, '2023-01-01', '2023-12-31', 'Dining', 150.00),
(1, 1200.00, '2023-01-01', '2023-12-31', 'Transportation', 80.00),
(1, 1200.00, '2023-01-01', '2023-12-31', 'Groceries', 200.00),
(1, 1200.00, '2023-01-01', '2023-12-31', 'Health', 70.00),
(1, 1200.00, '2023-01-01', '2023-12-31', 'Clothing', 50.00),
(1, 1200.00, '2023-01-01', '2023-12-31', 'Entertainment', 50.00),
(1, 1200.00, '2023-01-01', '2023-12-31', 'Education', 40.00),
(1, 1200.00, '2023-01-01', '2023-12-31', 'Home', 60.00),
(1, 1200.00, '2023-01-01', '2023-12-31', 'Pets', 30.00),
(1, 1200.00, '2023-01-01', '2023-12-31', 'Technology', 20.00),
(1, 1200.00, '2023-01-01', '2023-12-31', 'Travel', 60.00),
(1, 1200.00, '2023-01-01', '2023-12-31', 'Gifts', 20.00),
(1, 1200.00, '2023-01-01', '2023-12-31', 'Donations', 10.00),
(1, 1200.00, '2023-01-01', '2023-12-31', 'Services', 30.00),
(1, 1200.00, '2023-01-01', '2023-12-31', 'Hobbies', 20.00),
(1, 1200.00, '2023-01-01', '2023-12-31', 'Shopping', 60.00);

-- Insert transactions
INSERT INTO Transactions (UserID, BudgetID, Amount, Date, Description, CategoryName) VALUES
(1, 1, 1200.00, '2023-01-05', 'Monthly Rent', 'Rent'),
(1, 1, 150.00, '2023-01-10', 'Electricity Bill', 'Utilities'),
(1, 1, 70.00, '2023-01-15', 'Dining at Italian Restaurant', 'Dining'),
(1, 1, 45.00, '2023-01-20', 'Gasoline', 'Transportation'),
(1, 1, 20.00, '2023-01-22', 'Coffee Shop', 'Dining'),
(1, 1, 30.00, '2023-01-24', 'Internet Bill', 'Utilities'),
(1, 1, 80.00, '2023-01-26', 'Grocery Shopping', 'Groceries'),
(1, 1, 60.00, '2023-01-28', 'Pharmacy', 'Health'),
(1, 1, 250.00, '2023-01-30', 'Car Repair', 'Transportation'),
(1, 1, 200.00, '2023-02-01', 'New Shoes', 'Clothing'),
(1, 1, 15.00, '2023-02-03', 'Snacks', 'Dining'),
(1, 1, 120.00, '2023-02-05', 'Electricity Bill', 'Utilities'),
(1, 1, 45.00, '2023-02-07', 'Streaming Service', 'Entertainment'),
(1, 1, 5.00, '2023-02-09', 'App Purchase', 'Entertainment'),
(1, 1, 110.00, '2023-02-11', 'Train Ticket', 'Transportation'),
(1, 1, 90.00, '2023-02-13', 'Gasoline', 'Transportation'),
(1, 1, 85.00, '2023-02-15', 'Water Bill', 'Utilities'),
(1, 1, 50.00, '2023-02-17', 'Movie Night', 'Entertainment'),
(1, 1, 75.00, '2023-02-19', 'Concert Tickets', 'Entertainment'),
(1, 1, 25.00, '2023-02-21', 'Books', 'Education'),
(1, 1, 45.00, '2023-02-23', 'Hardware Supplies', 'Home'),
(1, 1, 40.00, '2023-02-25', 'Pet Food', 'Pets'),
(1, 1, 180.00, '2023-02-27', 'Dental Checkup', 'Health'),
(1, 1, 95.00, '2023-03-01', 'Home Decor', 'Home'),
(1, 1, 60.00, '2023-03-03', 'Gym Membership', 'Health'),
(1, 1, 30.00, '2023-03-05', 'Public Transport Card', 'Transportation'),
(1, 1, 20.00, '2023-03-07', 'Bar Drinks', 'Dining'),
(1, 1, 10.00, '2023-03-09', 'Magazine Subscription', 'Entertainment'),
(1, 1, 100.00, '2023-03-11', 'Annual Software License', 'Technology'),
(1, 1, 200.00, '2023-03-13', 'Weekend Getaway', 'Travel'),
(1, 1, 300.00, '2023-03-15', 'Flight Ticket', 'Travel'),
(1, 1, 40.00, '2023-03-17', 'Uber Ride', 'Transportation'),
(1, 1, 120.00, '2023-03-19', 'Health Insurance', 'Health'),
(1, 1, 15.00, '2023-03-21', 'Fast Food', 'Dining'),
(1, 1, 50.00, '2023-03-23', 'Gardening Supplies', 'Home'),
(1, 1, 250.00, '2023-03-25', 'New Smartphone', 'Technology'),
(1, 1, 90.00, '2023-03-27', 'Therapy Session', 'Health'),
(1, 1, 110.00, '2023-03-29', 'Hotel Booking', 'Travel'),
(1, 1, 70.00, '2023-04-01', 'Easter Gifts', 'Gifts'),
(1, 1, 50.00, '2023-04-03', 'Charity Donation', 'Donations'),
(1, 1, 25.00, '2023-04-05', 'Plant Nursery', 'Home'),
(1, 1, 60.00, '2023-04-07', 'Specialty Coffee Beans', 'Groceries'),
(1, 1, 55.00, '2023-04-09', 'Vintage Market', 'Shopping'),
(1, 1, 40.00, '2023-04-11', 'Dry Cleaning', 'Services'),
(1, 1, 120.00, '2023-04-13', 'New Curtains', 'Home'),
(1, 1, 15.00, '2023-04-15', 'Laundry Detergent', 'Groceries'),
(1, 1, 100.00, '2023-04-17', 'Annual Book Fair', 'Education'),
(1, 1, 220.00, '2023-04-19', 'Kitchen Mixer', 'Home'),
(1, 1, 35.00, '2023-04-21', 'Local Bakery', 'Groceries'),
(1, 1, 180.00, '2023-04-23', 'Crafting Materials', 'Hobbies'),
(1, 1, 200.00, '2023-04-25', 'Art Class', 'Education'),
(1, 1, 90.00, '2023-04-27', 'Massage Therapy', 'Health'),
(1, 1, 50.00, '2023-04-29', 'Bicycle Repair', 'Transportation');