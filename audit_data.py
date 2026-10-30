import pandas as pd
from pathlib import Path
# Define the raw data directory
RAW_DIR = Path("data/raw")
# Load the three raw tables
orders = pd.read_csv(RAW_DIR / "orders.csv")
customers = pd.read_csv(RAW_DIR / "customers.csv")
products = pd.read_csv(RAW_DIR / "products.csv")

# --------------------------------------------------
# 1. AUDIT: SHAPE, DATA TYPES, AND MISSING VALUES
# --------------------------------------------------
def audit_table(name, df):
   print(f"\n{'=' * 60}")
   print(f"RAW DATA AUDIT: {name.upper()}")
   print(f"{'=' * 60}")
   # Report number of rows and columns
   print(f"\nShape: {df.shape}")
   print(f"Rows: {df.shape[0]}")
   print(f"Columns: {df.shape[1]}")
   # Report data types
   print("\nDATA TYPES:")
   print(df.dtypes.to_string())
   # Report missing values for every column
   missing_count = df.isna().sum()
   missing_percentage = (df.isna().mean() * 100).round(2)
   missing_summary = pd.DataFrame({
       "missing_count": missing_count,
       "missing_percentage": missing_percentage
   })
   print("\nMISSING VALUES BY COLUMN:")
   print(missing_summary.to_string())

# Audit all three tables
audit_table("Orders", orders)
audit_table("Customers", customers)
audit_table("Products", products)

# --------------------------------------------------
# 2. RAW ORDERS AUDIT FIGURES
# --------------------------------------------------
# Convert amounts to numeric for validation
numeric_amount = pd.to_numeric(
   orders["order_amount"], errors="coerce"
)
# Convert delivery times to numeric for validation
numeric_delivery = pd.to_numeric(
   orders["delivery_minutes"], errors="coerce"
)
order_audit = {
   "Raw orders rows": len(orders),
   "Exact duplicate rows": int(orders.duplicated().sum()),
   "Pending order rows": int(
       orders["status"].astype(str).str.strip().str.lower()
       .eq("pending").sum()
   ),
   "Distinct order_id values": int(
       orders["order_id"].nunique()
   ),
   "Non-numeric order_amount entries": int(
       numeric_amount.isna().sum()
   ),
   "Negative delivery minutes": int(
numeric_delivery.lt(0).sum()
   ),
   "Blank delivery minutes": int(
       orders["delivery_minutes"].isna().sum()
       + orders["delivery_minutes"].astype(str)
       .str.strip().eq("").sum()
   )
}

# --------------------------------------------------
# 3. RAW CUSTOMERS AUDIT FIGURES
# --------------------------------------------------
numeric_age = pd.to_numeric(
   customers["age"], errors="coerce"
)
blank_age = (
   customers["age"].isna()
   | customers["age"].astype(str).str.strip().eq("")
)
blank_gender = (
   customers["gender"].isna()
   | customers["gender"].astype(str).str.strip().eq("")
)
blank_city = (
   customers["city"].isna()
   | customers["city"].astype(str).str.strip().eq("")
)
# Keep raw spellings; do not normalize capitalization
# or spelling before counting distinct values.
distinct_cities = customers.loc[
   ~blank_city, "city"
].nunique()
distinct_genders = customers.loc[
   ~blank_gender, "gender"
].nunique()
customers_audit = {
   "Blank age": int(blank_age.sum()),
   "Age outside 10-100": int(
       (
           numeric_age.notna()
& ~numeric_age.between(10, 100)
       ).sum()
   ),
   "Distinct raw city spellings": int(distinct_cities),
   "Distinct non-blank raw gender spellings": int(
       distinct_genders
   ),
   "Blank gender": int(blank_gender.sum())
}

# --------------------------------------------------
# 4. PRINT THE REQUIRED AUDIT FIGURES
# --------------------------------------------------
print("\n" + "=" * 60)
print("REQUIRED RAW DATA AUDIT FIGURES")
print("=" * 60)
audit_results = pd.DataFrame(
   list(order_audit.items()) + list(customers_audit.items()),
   columns=["Audit Metric", "Observed Value"]
)
print(audit_results.to_string(index=False))

# --------------------------------------------------
# 5. COMPARE WITH ASSIGNMENT REFERENCE VALUES
# --------------------------------------------------
reference_values = {
   "Raw orders rows": 13084,
   "Exact duplicate rows": 119,
   "Pending order rows": 656,
   "Distinct order_id values": 12309,
   "Non-numeric order_amount entries": 120,
   "Negative delivery minutes": 106,
   "Blank delivery minutes": 2541,
   "Blank age": 61,
   "Age outside 10-100": 6,
   "Distinct raw city spellings": 24,
   "Distinct non-blank raw gender spellings": 10,
   "Blank gender": 30
}
audit_results["Expected Value"] = audit_results[
   "Audit Metric"
].map(reference_values)
audit_results["Result"] = audit_results.apply(
   lambda row: (
       "PASS"
       if row["Observed Value"] == row["Expected Value"]
       else "CHECK"
   ),
   axis=1
)
print("\n" + "=" * 60)
print("REFERENCE VALUE VALIDATION")
print("=" * 60)
print(audit_results.to_string(index=False))
print("\nAudit completed.")