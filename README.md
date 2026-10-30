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