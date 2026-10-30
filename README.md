Instamart Customer Intelligence Copilot
1. Project Overview
The Instamart Customer Intelligence Copilot project focuses on auditing, cleaning, and preparing raw customer, order, and product datasets using Python and Pandas.
The objective is to improve data quality, handle missing and invalid values, standardise inconsistent data, and prepare reliable datasets for downstream customer intelligence and analytics.
2. Technologies Used
● Python
● Pandas
● Git and GitHub
● Visual Studio Code
● CSV datasets
3.  Environment Setup
Step 1: Clone the repository
git clone https://github.com/jaya169/instamart-customer-intelligence-copilot.git
Step 2: Navigate to the project directory
cd instamart-customer-intelligence-copilot
Step 3: Create a virtual environment
python -m venv .venv
Step 4: Activate the virtual environment
Windows PowerShell:
.\.venv\Scripts\Activate.ps1
macOS/Linux:
source .venv/bin/activate
Step 5: Install dependencies
pip install -r requirements.txt
4. Data Audit
The audit_data.py script loads the three raw datasets using Pandas and performs an initial data-quality audit.
Audit activities
● Report the shape of each dataset.
● Display the data type of every column.
● Calculate missing-value counts and percentages for every column.
● Identify exact duplicate order rows.
● Count pending orders and distinct order IDs.
● Identify non-numeric order amounts.
● Identify negative and blank delivery times.
● Identify blank ages and ages outside the valid range.
● Count distinct raw city and gender spellings.
Important data-loading rule
The raw tickets.csv file must be loaded using:
pd.read_csv(path, keep_default_na=False)
wherever that file is used later, so empty ticket texts remain empty strings rather than being automatically converted to missing values.
Reference audit results
|Audit metric                           |Expected value|
|---------------------------------------|-------------:|
|Raw order rows                         |13,084        |
|Exact duplicate order rows             |119           |
|Pending order rows                     |656           |
|Distinct order IDs                     |12,309        |
|Non-numeric order amounts              |120           |
|Negative delivery minutes              |106           |
|Blank delivery minutes                 |2,541         |
|Blank customer ages                    |61            |
|Ages outside 10–100                    |6             |
|Distinct raw city spellings            |24            |
|Distinct non-blank raw gender spellings|10            |
|Blank customer genders                 |30            |
Run the audit using:
python audit_data.py
5. Customer Data Cleaning
The clean_customers.py script prepares the customer dataset for analysis.
Cleaning rules
1. City standardisation: Remove leading and trailing spaces and apply title case to city names so that exactly six standardised cities remain.
2. Gender standardisation: Map all gender spellings to male, female, or unknown. Blank gender values are mapped to unknown.
3. Age validation: Treat ages outside the range of 10–100 as missing.
4. Age imputation: Fill missing ages using the median age of the customer’s city, calculated using groupby() and transform().
5. Signup date conversion: Convert signup_date to a datetime data type.
Expected validation results
|City     |Expected customer count|
|---------|----------------------:|
|Pune     |227                    |
|Delhi    |210                    |
|Bengaluru|197                    |
|Chennai  |191                    |
|Hyderabad|191                    |
|Mumbai   |184                    |
|Gender |Expected customer count|
|-------|----------------------:|
|female |610                    |
|male   |560                    |
|unknown|30                     |
Additional checks:
● No missing ages remain.
● Every cleaned age is between 18 and 60.
Run the customer-cleaning script using:
python clean_customers.py
6. Order Data Cleaning
The clean_orders.py script cleans the order dataset and produces one final record per order ID.
Cleaning rules
Rule 1: Convert order timestamps
Convert order_ts to a datetime data type.
Rule 2: Remove exact duplicate rows
Remove exact duplicate rows before applying the remaining order-cleaning rules.
Rule 3: Retain the latest record for each order
Some orders have multiple records with different statuses, such as an earlier pending record followed by a final completed or cancelled record.
For each order_id, retain only the record with the latest order_ts.
Rule 4: Convert and impute order amounts
Convert order_amount to numeric, turning unparseable values into missing values.
Fill each missing amount using the product price, quantity, and discount:
order_amount = round(price_inr × quantity × (1 - discount_pct / 100), 2)
The product price is obtained from products.csv using the appropriate product identifier.
Rule 5: Clean delivery minutes
● Convert negative delivery_minutes values to missing values.
● For completed orders, fill missing delivery times using the median delivery time for the corresponding product category among completed orders.
● Use groupby() and transform() for category-level median imputation.
● Leave delivery times missing for cancelled orders because cancelled orders were never delivered.
Expected validation results
|Validation metric                              |Expected value  |
|-----------------------------------------------|---------------:|
|Final order rows                               |12,309          |
|Distinct order IDs                             |12,309          |
|Completed orders                               |11,110          |
|Cancelled orders                               |1,199           |
|Pending orders                                 |0               |
|Missing order amounts                          |0               |
|Missing delivery minutes among completed orders|0               |
|Missing delivery minutes among cancelled orders|1,199           |
|Total order amount for completed orders        |INR 2,998,668.80|
Run the order-cleaning script using:
python clean_orders.py
The cleaned order dataset is saved to:
data/clean/orders_clean.csv
7. Product Data Cleaning
The clean_products.py script is responsible for preparing the product dataset for analysis.
Product information is also used to support order cleaning, particularly when calculating missing order amounts and identifying product categories.
The raw product dataset contains the following columns:
● product_id
● product_name
● category
● price_inr
Use price_inr as the product price column when calculating missing order amounts.
Run the product-cleaning script using:
python clean_products.py
Verify the output path and the actual cleaning rules implemented in clean_products.py before final submission.
8. Output Datasets
The cleaned datasets are intended to be stored in the data/clean/ directory.
|Dataset              |Purpose                      |
|---------------------|-----------------------------|
|`orders_clean.csv`   |Cleaned order records        |
|`customers_clean.csv`|Standardised customer records|
|`products_clean.csv` |Cleaned product records      |
These datasets provide a consistent foundation for downstream analytics.
9. Running the Project
Activate the virtual environment and install the required dependencies before running the scripts.
Execute the scripts individually:
python audit_data.py
python clean_customers.py
python clean_products.py
python clean_orders.py
Check that each script finishes successfully and writes its expected output file.
Run the audit before cleaning to establish the original data quality. Run the cleaning scripts to generate the cleaned datasets, then verify the required reference results.
10. Final Validation Checklist
Before submitting the project, verify the following:
All three raw tables are loaded successfully.
Dataset shapes, data types, and missing-value summaries are reported.
Raw audit figures match the reference values.
Customer city names are standardised to six cities.
Gender values are mapped to male, female, or unknown.
Missing and invalid customer ages are handled correctly.
signup_date is converted to datetime.
Order timestamps are converted to datetime.
Exact duplicate order rows are removed.
The latest record is retained for each order ID.
Missing order amounts are calculated using product prices, quantities, and discounts.
Negative delivery times are set to missing.
Missing delivery times are imputed only for completed orders.
Cancelled orders retain missing delivery times.
All cleaned datasets are saved in the expected output directory.
All reference validation results match.
README documents the implemented cleaning rules.
Project files are committed and pushed to GitHub.
11. GitHub Submission
After validating the scripts and output datasets, commit and push the final project changes.
Check the repository status:
git status
Stage the relevant project files:
git add README.md audit_data.py clean_orders.py clean_customers.py clean_products.py requirements.txt data/
Commit the changes:
git commit -m "Complete data audit and cleaning"
Push the changes to the GitHub repository:
git push origin main
If your working branch has a different name, replace main with the correct branch name.
Finally, open the GitHub repository in your browser and verify that the README, Python scripts, and required output files are available.
12. Conclusion
The project establishes a repeatable data-quality workflow for auditing and cleaning customer, order, and product datasets using Python and Pandas.
The workflow addresses missing values, duplicate records, inconsistent categorical values, invalid numeric data, date conversion, and business-rule-based imputation.
The resulting datasets can be used as a foundation for further customer intelligence and analytics.
13. Data Storage and Validation
Data Storage
The three cleaned datasets are stored as CSV files in the data/clean/ directory:
● customers_clean.csv
● products_clean.csv
● orders_clean.csv
The datasets are also stored in a SQLite database at data/instamart.db.
The database contains the following tables:
|Table      |Description          |
|-----------|---------------------|
|`customers`|Cleaned customer data|
|`products` |Cleaned product data |
|`orders`   |Cleaned order data   |
The order_ts column is stored as text in the format YYYY-MM-DD HH:MM:SS.
Validation
The validate_data.py script checks the cleaned datasets against the expected reference values.
Validation includes customer city and gender distributions, age validity, order counts, order status distributions, missing values, completed order totals, CSV file availability, SQLite table existence, database row counts, and timestamp storage.
Run the storage script:
python store_data.py
Run the validation script:
python validate_data.py
When all validation assertions pass, the script prints:
ALL CHECKPOINTS PASSED
The validation process helps confirm that the cleaned datasets are stored correctly and meet the required reference checkpoints.
14. SQL Analysis
Overview

Seven SQL queries were created and executed against the SQLite database data/instamart.db using Python and Pandas. The SQL queries are stored in sql/queries.sql, and their results are retrieved using pd.read_sql_query().

Unless otherwise specified, only orders with the status completed are considered when calculating revenue and customer spending.
Q1 — WHERE and HAVING
Objective: Identify customers whose completed orders have an individual order amount greater than INR 500 and whose combined value of those orders exceeds INR 8,000.
Approach:

Use WHERE to filter completed orders with order_amount > 500.

Group the filtered records by customer.

Use HAVING to retain customers whose total qualifying order amount exceeds INR 8,000.
Expected result: 30 customers.
Q2 — Three-Table JOIN
Objective: Calculate revenue by customer city and product category.
Approach:

Join the orders, customers, and products tables.

Filter for completed orders.

Group the results by city and product category.

Calculate revenue as the sum of order_amount.
Expected results:

Total rows: 30.

Total revenue: INR 2,998,668.80.

Highest-revenue city and category combination: Bengaluru / Electronics.

Revenue for Bengaluru / Electronics: INR 233,909.45.
Q3 — Scalar Subquery
Objective: Identify products priced above the average catalogue price.
Approach:

Calculate the average product price using a scalar subquery.

Return products whose prices exceed that average.
Expected result: 11 products.
Q4 — LEFT JOIN
Objective: Identify customers who have never placed a completed order.
Approach:

Use a LEFT JOIN between customers and orders.

Restrict the matching orders to completed orders in the join condition.

Identify customers for whom no completed order exists.
Expected result: 25 customers.
Q5 — Common Table Expression (CTE)
Objective: Identify customers whose total completed spending is above the average total spending per customer.
Approach:

The first CTE calculates each customer’s total completed spending.

The second CTE calculates the average of those customer spending totals.

The main query returns customers whose total completed spending exceeds that average.

Customers without completed orders are excluded from the spending calculation.
Expected results:

Customers above average spending: 550.

Average completed spending per customer: INR 2,552.06, rounded to two decimal places.
Q6 — Ranking Window Functions
Objective: Rank customers by total completed spending within each city.
Approach:

Calculate each customer’s total completed spending.

Use PARTITION BY city to rank customers independently within each city.

Use ORDER BY total_spend DESC to rank customers from highest to lowest spending.

Apply RANK(), DENSE_RANK(), and ROW_NUMBER().
Expected top customer in each city:
City
Customer ID
Total Spend (INR)
Bengaluru

C0082

12,856.20

Chennai

C0930

10,151.40

Delhi

C0291

13,742.60

Hyderabad

C0743

12,730.05

Mumbai

C0693

14,766.55

Pune

C0426

10,377.10
Expected validation: Exactly 8 rows have different RANK() and ROW_NUMBER() values.
Explanation of ties: When customers have equal spending, RANK() assigns them the same rank and skips subsequent rank numbers, whereas ROW_NUMBER() assigns each row a unique sequential number. Therefore, ties can cause the two ranking functions to return different values.
Q7 — Running Total
Objective: Calculate daily completed revenue and its cumulative total over time.
Approach:

Extract the date from the first ten characters of order_ts.

Calculate total completed revenue for each day.

Use SUM(revenue) OVER (ORDER BY day) to calculate cumulative revenue.
Expected results:

Daily rows: 183.

Final cumulative revenue: INR 2,998,668.80.
SQL Execution and Validation

All seven SQL queries are stored in sql/queries.sql.

The queries are executed from Python using pd.read_sql_query() against data/instamart.db. The results are checked against the reference values specified in the project requirements.

The analysis demonstrates the use of:

WHERE and HAVING clauses.

Multi-table joins, including LEFT JOIN.

Scalar subqueries.

Common Table Expressions (CTEs).

Window functions: RANK(), DENSE_RANK(), and ROW_NUMBER().

Running totals using SUM() OVER().
Conclusion: The SQL analysis validates customer spending, city-level revenue, product pricing, customers without completed orders, spending patterns, customer rankings, and cumulative daily revenue.
15. Pandas Cross-Check and Exploratory Data Analysis
Revenue Cross-Check
The pandas_analysis.py script rebuilds the SQL city-and-category revenue analysis using pd.pivot_table() with margins=True.
The grand total from the Pandas pivot table is compared against the completed-order revenue calculated in SQLite. Both should equal INR 2,998,668.80.
City-Level Aggregation
The script uses Pandas groupby() and named aggregation to calculate the sum, mean, and count of completed order amounts for each city.
Reference checks:
Bengaluru: sum INR 523,643.40, mean INR 276.47, count 1,894.
Mumbai: sum INR 479,058.50, mean INR 297.00, count 1,613.
Order Amount Distribution
The analysis reports the mean, median, skewness, quartiles, interquartile range, 1.5 × IQR fences, and the number of outliers beyond each fence.
Reference statistics:
Mean: INR 269.91.
Median: INR 135.00.
Skewness: approximately 4.61.
Q1: INR 64.80.
Q3: INR 297.00.
Lower fence: -INR 283.50.
Upper fence: INR 645.30.
Outliers below the lower fence: 0.
Outliers above the upper fence: 897.
Correlation Analysis
A correlation matrix is calculated for order_amount, discount_pct, quantity, and delivery_minutes among completed orders.
The largest absolute correlation is expected between order_amount and discount_pct, at approximately -0.095. This indicates a very weak negative linear association. Correlation of this size does not establish causation.
Running the Analysis
Execute the script from the project root:
python pandas_analysis.py
The script saves the revenue pivot, city summary, order amount statistics, and correlation matrix as CSV files in data/clean/.
 