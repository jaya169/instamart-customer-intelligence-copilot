from pathlib import Path
import pandas as pd
RAW = Path("data/raw")
# Load the raw datasets
customers = pd.read_csv(RAW / "customers.csv")
products = pd.read_csv(RAW / "products.csv")
orders = pd.read_csv(RAW / "orders.csv")
print("=" * 60)
print("INSTAMART RAW DATA AUDIT")
print("=" * 60)
# 1. Dataset sizes
for name, df in [
   ("Customers", customers),
   ("Products", products),
   ("Orders", orders),
]:
   print(f"\n{name}: {df.shape[0]} rows, {df.shape[1]} columns")
# 2. Exact duplicate order rows
print("\n--- ORDER AUDIT ---")
print("Exact duplicate order rows:", orders.duplicated().sum())
# 3. Pending orders
if "status" in orders.columns:
   print(
       "Pending order rows:",
       orders["status"].astype(str).str.strip().str.lower()
       .eq("pending").sum()
   )
# 4. Distinct order IDs
if "order_id" in orders.columns:
   print("Distinct order IDs:", orders["order_id"].nunique())
# 5. Missing order values
print("\nMissing values in orders:")
print(orders.isna().sum().to_string())
# 6. Order amount validation
if "order_amount" in orders.columns:
   amount = pd.to_numeric(orders["order_amount"], errors="coerce")
   print(
       "\nOrder amounts that cannot be converted to numbers:",
       amount.isna().sum() - orders["order_amount"].isna().sum()
   )
   print("Missing order amounts:", orders["order_amount"].isna().sum())
   print("Negative order amounts:", amount.lt(0).sum())
# 6.1 Quantity validation
if "quantity" in orders.columns:
   quantity = pd.to_numeric(orders["quantity"], errors="coerce")
   print("\nQuantity validation:")
   print("Missing or invalid quantities:", quantity.isna().sum())
   print("Negative quantities:", (quantity < 0).sum())
   print("Zero quantities:", (quantity == 0).sum())
# 7. Customer data quality
print("\n--- CUSTOMER AUDIT ---")
print("Missing customer values:")
print(customers.isna().sum().to_string())
if "age" in customers.columns:
   age = pd.to_numeric(customers["age"], errors="coerce")
   print("Missing or invalid ages:", age.isna().sum())
   print("Ages outside 10–100:", (~age.between(10, 100)).sum())
if "city" in customers.columns:
   city = customers["city"].astype("string")
   print(
       "City values with leading/trailing spaces:",
       city.ne(city.str.strip()).fillna(False).sum()
   )
print("\n--- PRODUCT AUDIT ---")
print("Missing product values:")
print(products.isna().sum().to_string())
print("\nAudit completed.")