import pandas as pd
from pathlib import Path
# --------------------------------------------------
# 1. DEFINE FILE PATHS
# --------------------------------------------------
RAW_DIR = Path("data/raw")
CLEAN_DIR = Path("data/clean")
CLEAN_DIR.mkdir(parents=True, exist_ok=True)
# --------------------------------------------------
# 2. LOAD RAW ORDERS AND PRODUCTS
# --------------------------------------------------
orders = pd.read_csv(RAW_DIR / "orders.csv")
products = pd.read_csv(RAW_DIR / "products.csv")

print("Orders columns:", orders.columns.tolist())
print("Products columns:", products.columns.tolist())
# --------------------------------------------------
# 3. CONVERT order_ts TO DATETIME
# --------------------------------------------------
orders["order_ts"] = pd.to_datetime(
   orders["order_ts"],
   errors="coerce"
)
# --------------------------------------------------
# 4. REMOVE EXACT DUPLICATE ROWS
# --------------------------------------------------
orders = orders.drop_duplicates().copy()
# --------------------------------------------------
# 5. KEEP THE LATEST RECORD FOR EACH order_id
# --------------------------------------------------
orders = (
   orders.sort_values("order_ts", kind="stable")
   .drop_duplicates(subset=["order_id"], keep="last")
   .copy()
)
# --------------------------------------------------
# 6. CONVERT order_amount TO NUMERIC
# --------------------------------------------------
orders["order_amount"] = pd.to_numeric(
   orders["order_amount"],
   errors="coerce"
)
# --------------------------------------------------
# 7. PREPARE PRODUCT PRICES
# --------------------------------------------------
products["price_inr"] = pd.to_numeric(
   products["price_inr"],
   errors="coerce"
)
# Match orders with their product prices.
# Rename the price column to avoid conflicts.
orders = orders.merge(
   products[["product_id", "price_inr"]],
   on="product_id",
   how="left",
   validate="many_to_one"
)
# Convert quantity and discount to numeric.
orders["quantity"] = pd.to_numeric(
   orders["quantity"],
   errors="coerce"
)
orders["discount_pct"] = pd.to_numeric(
   orders["discount_pct"],
   errors="coerce"
)
# --------------------------------------------------
# 8. FILL MISSING ORDER AMOUNTS
# Formula:
# price * quantity * (1 - discount_pct / 100)
# --------------------------------------------------
calculated_amount = (
   orders["price_inr"]
   * orders["quantity"]
   * (1 - orders["discount_pct"] / 100)
).round(2)
orders["order_amount"] = orders["order_amount"].fillna(
   calculated_amount
)
# Remove the temporary product price column.
orders = orders.drop(columns=["price_inr"])
# --------------------------------------------------
# 9. SET NEGATIVE DELIVERY TIMES TO MISSING
# --------------------------------------------------
orders["delivery_minutes"] = pd.to_numeric(
   orders["delivery_minutes"],
   errors="coerce"
)
orders.loc[
   orders["delivery_minutes"] < 0,
   "delivery_minutes"
] = float("nan")
# --------------------------------------------------
# 10. IMPUTE COMPLETED-ORDER DELIVERY TIMES
# Use the median for each product category among
# completed orders, using groupby and transform.
# --------------------------------------------------
# Get product categories.
orders = orders.merge(
   products[["product_id", "category"]],
   on="product_id",
   how="left",
   validate="many_to_one"
)
completed_mask = orders["status"].astype(str).str.strip().str.lower().eq(
   "completed"
)
completed_medians = (
   orders.loc[completed_mask]
   .groupby("category")["delivery_minutes"]
   .transform("median")
)
# Fill missing delivery times only for completed orders.
orders.loc[completed_mask, "delivery_minutes"] = (
   orders.loc[completed_mask, "delivery_minutes"]
   .fillna(completed_medians)
)
# Cancelled orders must have missing delivery times.
cancelled_mask = orders["status"].astype(str).str.strip().str.lower().eq(
   "cancelled"
)
orders.loc[cancelled_mask, "delivery_minutes"] = float("nan")
# --------------------------------------------------
# 11. SAVE CLEANED ORDERS
# --------------------------------------------------
orders.to_csv(
   CLEAN_DIR / "orders_clean.csv",
   index=False
)
# --------------------------------------------------
# 12. VALIDATE RESULTS
# --------------------------------------------------
print("\nCLEAN ORDERS VALIDATION")
print("-" * 50)
print("Total rows:", len(orders))
print("Distinct order IDs:", orders["order_id"].nunique())
print("\nOrder status counts:")
print(orders["status"].value_counts())
print("\nMissing order amounts:", orders["order_amount"].isna().sum())
print(
   "Missing delivery minutes among completed orders:",
   orders.loc[completed_mask, "delivery_minutes"].isna().sum()
)
print(
   "Missing delivery minutes among cancelled orders:",
   orders.loc[cancelled_mask, "delivery_minutes"].isna().sum()
)
print(
   "Completed orders amount total:",
   round(orders.loc[completed_mask, "order_amount"].sum(), 2)
)
print("\nCleaned orders saved to data/clean/orders_clean.csv")