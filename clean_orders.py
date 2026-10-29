from pathlib import Path
import pandas as pd
# Define input and output directories
RAW = Path("data/raw")
CLEAN = Path("data/clean")
# Create the clean directory if it doesn't exist
CLEAN.mkdir(parents=True, exist_ok=True)
# Load the original order data
orders = pd.read_csv(RAW / "orders.csv")
print("--- ORIGINAL ORDER DATA ---")
print("Dataset shape:", orders.shape)
# 1. Remove duplicate rows
orders = orders.drop_duplicates()
# 2. Clean column names
orders.columns = orders.columns.str.strip()
# 3. Clean text columns
for column in ["status"]:
   if column in orders.columns:
       orders[column] = orders[column].astype("string").str.strip().str.lower()
# 4. Clean order amount
if "order_amount" in orders.columns:
   orders["order_amount"] = pd.to_numeric(
       orders["order_amount"], errors="coerce"
   )
# 5. Clean quantity
if "quantity" in orders.columns:
   orders["quantity"] = pd.to_numeric(
       orders["quantity"], errors="coerce"
   )
# 6. Clean discount percentage
if "discount_pct" in orders.columns:
   orders["discount_pct"] = pd.to_numeric(
       orders["discount_pct"], errors="coerce"
   )
# 7. Clean delivery time
if "delivery_minutes" in orders.columns:
   orders["delivery_minutes"] = pd.to_numeric(
       orders["delivery_minutes"], errors="coerce"
   )
# 8. Handle missing values
# Keep missing order amounts as NaN because the actual amount is unknown.
# Remove records with missing essential identifiers
essential_columns = [
   column
   for column in ["order_id", "customer_id", "product_id"]
   if column in orders.columns
]
if essential_columns:
   orders = orders.dropna(subset=essential_columns)
# 9. Validate order amounts
if "order_amount" in orders.columns:
   invalid_amounts = orders["order_amount"].lt(0)
   orders.loc[invalid_amounts, "order_amount"] = pd.NA
# 10. Validate quantities
if "quantity" in orders.columns:
   invalid_quantities = orders["quantity"].le(0)
   orders.loc[invalid_quantities, "quantity"] = pd.NA
# 11. Validate discount percentages
if "discount_pct" in orders.columns:
   invalid_discounts = ~orders["discount_pct"].between(0, 100)
   orders.loc[invalid_discounts, "discount_pct"] = pd.NA
# 12. Validate delivery minutes
if "delivery_minutes" in orders.columns:
   invalid_delivery = orders["delivery_minutes"].lt(0)
   orders.loc[invalid_delivery, "delivery_minutes"] = pd.NA
# 13. Validate order status
valid_statuses = ["completed", "cancelled", "pending"]
if "status" in orders.columns:
   invalid_status = ~orders["status"].isin(valid_statuses)
   orders.loc[invalid_status, "status"] = pd.NA
# 14. Save cleaned data
output_file = CLEAN / "orders_clean.csv"
orders.to_csv(output_file, index=False)
# 15. Display cleaning results
print("\n--- CLEANING RESULTS ---")
print("Original records after cleaning:", len(orders))
print("Remaining missing values:")
print(orders.isna().sum().to_string())
print("\nCleaned sample:")
print(orders.head().to_string(index=False))
print("\nCleaned dataset saved to:", output_file)
print("Order cleaning completed.")