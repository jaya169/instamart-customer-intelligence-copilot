import re
import sqlite3
from pathlib import Path
import pandas as pd
# Define project paths
BASE_DIR = Path(__file__).resolve().parent
CLEAN_DIR = BASE_DIR / "data" / "clean"
DB_PATH = BASE_DIR / "data" / "instamart.db"
# Load cleaned datasets
customers = pd.read_csv(CLEAN_DIR / "customers_clean.csv")
products = pd.read_csv(CLEAN_DIR / "products_clean.csv")
orders = pd.read_csv(CLEAN_DIR / "orders_clean.csv")
# Normalise fields used in validation
customers["age"] = pd.to_numeric(
   customers["age"], errors="coerce"
)
orders["order_amount"] = pd.to_numeric(
   orders["order_amount"], errors="coerce"
)
orders["delivery_minutes"] = pd.to_numeric(
   orders["delivery_minutes"], errors="coerce"
)
orders["status"] = (
   orders["status"].astype(str).str.strip().str.lower()
)
customers["city"] = (
   customers["city"].astype(str).str.strip()
)
customers["gender"] = (
   customers["gender"].astype(str).str.strip().str.lower()
)
# --------------------------------------------------
# 1. CUSTOMER VALIDATION
# --------------------------------------------------
# Expected city counts
expected_cities = {
   "Pune": 227,
   "Delhi": 210,
   "Bengaluru": 197,
   "Chennai": 191,
   "Hyderabad": 191,
   "Mumbai": 184,
}
city_counts = customers["city"].value_counts().to_dict()
assert city_counts == expected_cities, (
   f"Unexpected city counts: {city_counts}"
)
# Expected gender counts
expected_genders = {
   "female": 610,
   "male": 560,
   "unknown": 30,
}
gender_counts = customers["gender"].value_counts().to_dict()
assert gender_counts == expected_genders, (
   f"Unexpected gender counts: {gender_counts}"
)
# No missing ages
assert customers["age"].isna().sum() == 0, (
   "Missing customer ages found"
)
# Every cleaned age must be between 18 and 60
assert customers["age"].between(18, 60).all(), (
   "Customer ages outside 18-60 found"
)
# Signup dates must be valid datetimes
signup_dates = pd.to_datetime(
   customers["signup_date"], errors="coerce"
)
assert signup_dates.notna().all(), (
   "Invalid or missing signup dates found"
)
# --------------------------------------------------
# 2. ORDER VALIDATION
# --------------------------------------------------
# Exactly one row per order ID
assert len(orders) == 12309, (
   f"Unexpected order row count: {len(orders)}"
)
assert orders["order_id"].nunique() == 12309, (
   "Order IDs are not unique"
)
# Expected order status counts
status_counts = orders["status"].value_counts().to_dict()
assert status_counts == {
   "completed": 11110,
   "cancelled": 1199,
}, f"Unexpected status counts: {status_counts}"
# No missing order amounts
assert orders["order_amount"].notna().all(), (
   "Missing order amounts found"
)
# Completed orders must have delivery times
completed = orders[orders["status"] == "completed"]
assert completed["delivery_minutes"].notna().all(), (
   "Completed orders have missing delivery times"
)
# Cancelled orders must have missing delivery times
cancelled = orders[orders["status"] == "cancelled"]
assert cancelled["delivery_minutes"].isna().all(), (
   "Cancelled orders contain delivery times"
)
# Completed order amount must match the reference total
completed_total = round(completed["order_amount"].sum(), 2)
assert completed_total == 2998668.80, (
   f"Unexpected completed order total: {completed_total}"
)
# Order timestamps must use YYYY-MM-DD HH:MM:SS format
assert orders["order_ts"].notna().all(), (
   "Missing order timestamps found"
)
timestamp_pattern = re.compile(
   r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
)
assert orders["order_ts"].astype(str).map(
   lambda value: bool(timestamp_pattern.fullmatch(value))
).all(), "Order timestamps have an invalid format"
# --------------------------------------------------
# 3. CSV FILE VALIDATION
# --------------------------------------------------
assert (CLEAN_DIR / "customers_clean.csv").is_file()
assert (CLEAN_DIR / "products_clean.csv").is_file()
assert (CLEAN_DIR / "orders_clean.csv").is_file()
# --------------------------------------------------
# 4. SQLITE DATABASE VALIDATION
# --------------------------------------------------
assert DB_PATH.is_file(), "SQLite database not found"
with sqlite3.connect(DB_PATH) as connection:
   # Verify that all required tables exist
   table_names = {
       row[0]
       for row in connection.execute(
           "SELECT name FROM sqlite_master "
           "WHERE type = 'table'"
       ).fetchall()
   }
   assert {"customers", "products", "orders"}.issubset(
       table_names
   ), f"Missing SQLite tables: {table_names}"
   # Verify that database row counts match the CSV files
   for table_name, expected_rows in {
       "customers": len(customers),
       "products": len(products),
       "orders": len(orders),
   }.items():
       actual_rows = connection.execute(
           f'SELECT COUNT(*) FROM "{table_name}"'
       ).fetchone()[0]
       assert actual_rows == expected_rows, (
           f"{table_name}: expected {expected_rows}, "
           f"found {actual_rows}"
       )
   # Confirm that order_ts is stored as SQLite text
   timestamp_type = connection.execute(
       "SELECT typeof(order_ts) "
       "FROM orders LIMIT 1"
   ).fetchone()[0]
   assert timestamp_type == "text", (
       f"Expected order_ts to be stored as text, "
       f"found {timestamp_type}"
   )
# Print only this success message when every assertion passes
print("ALL CHECKPOINTS PASSED")