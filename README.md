Instamart Customer Intelligence Copilot
1. Project Overview
The Instamart Customer Intelligence Copilot project aims to organize, clean, and analyze customer, order, and product data to support business insights and customer intelligence.
The project uses Python and Pandas for data processing and data quality validation. The cleaned datasets provide a foundation for further analysis, reporting, and the development of an AI-powered customer intelligence copilot.
2. Project Objectives
Clean and prepare customer, order, and product datasets.
Handle missing values and duplicate records.
Validate data types and business rules.
Identify invalid values in order and product data.
Generate cleaned CSV files for downstream analysis.
Prepare structured data for customer intelligence and business insights.
3. Technologies Used
Python
Pandas
CSV datasets
Visual Studio Code
Git and GitHub
4. Project Structure
instamart-customer-intelligence-copilot/
│
├── data/
│   ├── raw/
│   └── clean/
│       ├── customers_clean.csv
│       ├── orders_clean.csv
│       └── products_clean.csv
│
├── clean_customers.py
├── clean_orders.py
├── clean_products.py
├── generate_data.py
├── audit_data.py
├── mock_llm.py
├── requirements.txt
└── README.md
5. Data Cleaning Process
Customer Data
The customer data-cleaning process prepares customer records for analysis by checking data quality, handling missing values, and identifying duplicate records.
Output:
data/clean/customers_clean.csv
Order Data
The order data-cleaning process includes:
Converting order amounts, quantities, discount percentages, and delivery times to numeric data types.
Handling missing values.
Removing records with missing essential identifiers where applicable.
Validating order amounts and quantities.
Validating discount percentages against the 0–100 range.
Validating delivery times.
Checking order statuses against the accepted values: completed, cancelled, and pending.
Output:
data/clean/orders_clean.csv
Missing order amounts and delivery times are retained as missing values when the actual values are unknown or unavailable.
Product Data
The product data-cleaning process prepares product records and checks for missing values and duplicate rows.
Output:
data/clean/products_clean.csv
6. Data Quality Validation
The cleaned datasets were checked for:
Total record counts.
Duplicate rows.
Missing values.
Expected column names.
The latest validation results observed during development were:
Dataset
Records
Columns
Duplicate Rows
Customers
1,200
5
0
Orders
12,965
9
0
Products
40
4
0
These figures reflect the validation output observed during development and may change if the datasets or cleaning rules are updated.
7. How to Run the Project
Prerequisites
Install Python and Git. Visual Studio Code is recommended for development.
Install Dependencies
Open a terminal in the project root directory and run:
pip install -r requirements.txt
Run the Data Generation Script
If your workflow requires generating the input datasets first, run:
python generate_data.py
Run the Cleaning Scripts
Run the scripts individually:
python clean_customers.py
python clean_orders.py
python clean_products.py
The commands assume the scripts are executed from the project root directory and that the required input data and dependencies are available.
8. Expected Outputs
The cleaning scripts generate the following cleaned datasets:
data/clean/customers_clean.csv
data/clean/orders_clean.csv
data/clean/products_clean.csv
These files can be used for further data exploration, business analysis, and customer intelligence workflows.
9. Future Enhancements
Potential enhancements include:
Customer segmentation and behavioral analysis.
Order and sales trend analysis.
Product performance analysis.
Customer intelligence metrics and dashboards.
Integration with a large language model for natural-language questions.
Automated data quality checks.
AI-powered insights and recommendations.
These are potential extensions and should not be considered implemented features unless they are available in the project.
10. Author and Repository
Project: Instamart Customer Intelligence Copilot
Repository: GitHub Repository
This project demonstrates data preparation, data quality validation, and the development of a foundation for customer intelligence.