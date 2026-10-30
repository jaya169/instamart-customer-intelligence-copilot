import sqlite3
from pathlib import Path
import pandas as pd
# --------------------------------------------------
# 1. SETUP
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "instamart.db"
OUTPUT_DIR = BASE_DIR / "data" / "clean"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
with sqlite3.connect(DB_PATH) as conn:
   # Load completed orders joined with customers and products
   df = pd.read_sql_query(
       """
       SELECT
           o.order_id,
           o.customer_id,
           o.product_id,
           o.order_ts,
           o.order_amount,
           o.discount_pct,
           o.quantity,
           o.delivery_minutes,
           c.city,
           p.category
       FROM orders AS o
       JOIN customers AS c
           ON o.customer_id = c.customer_id
       JOIN products AS p
           ON o.product_id = p.product_id
       WHERE LOWER(TRIM(o.status)) = 'completed'
       """,
       conn,
   )
   # SQL revenue total for cross-checking
   sql_total = pd.read_sql_query(
       """
       SELECT ROUND(SUM(order_amount), 2) AS total_revenue
       FROM orders
       WHERE LOWER(TRIM(status)) = 'completed'
       """,
       conn,
   ).iloc[0]["total_revenue"]

# Convert analysis columns to numeric
numeric_columns = [
   "order_amount",
   "discount_pct",
   "quantity",
   "delivery_minutes",
]
for column in numeric_columns:
   df[column] = pd.to_numeric(df[column], errors="coerce")
df["order_amount"] = df["order_amount"].round(2)
print("=" * 65)
print("PANDAS CROSS-CHECK AND EXPLORATORY DATA ANALYSIS")
print("=" * 65)

# --------------------------------------------------
# 2. PART A: PIVOT TABLE CROSS-CHECK
# --------------------------------------------------
print("\nPART A1: CITY AND CATEGORY REVENUE PIVOT TABLE")
pivot = pd.pivot_table(
   df,
   values="order_amount",
   index="city",
   columns="category",
   aggfunc="sum",
   fill_value=0,
   margins=True,
   margins_name="All",
)
print(pivot.round(2).to_string())
# Check grand total against SQL
pivot_total = round(float(pivot.loc["All", "All"]), 2)
sql_total = round(float(sql_total), 2)
print(f"\nPandas pivot grand total: INR {pivot_total:,.2f}")
print(f"SQL completed revenue:    INR {sql_total:,.2f}")
assert pivot_total == sql_total, (
   f"Pivot total {pivot_total} does not match "
   f"SQL total {sql_total}"
)
print("Pivot total matches SQL total: PASS")

# Save the pivot table
pivot.to_csv(OUTPUT_DIR / "pandas_revenue_pivot.csv")

# --------------------------------------------------
# 3. CITY-LEVEL NAMED AGGREGATION
# --------------------------------------------------
print("\nPART A2: COMPLETED ORDER AMOUNT BY CITY")
city_summary = (
   df.groupby("city")
   .agg(
       total_revenue=("order_amount", "sum"),
       mean_order_amount=("order_amount", "mean"),
       order_count=("order_amount", "count"),
   )
   .round(
       {
           "total_revenue": 2,
           "mean_order_amount": 2,
       }
   )
   .sort_index()
)
print(city_summary.to_string())
print("\nReference checks:")
expected_city_values = {
   "Bengaluru": {
       "total_revenue": 523643.40,
       "mean_order_amount": 276.47,
       "order_count": 1894,
   },
   "Mumbai": {
       "total_revenue": 479058.50,
       "mean_order_amount": 297.00,
       "order_count": 1613,
   },
}
for city, expected in expected_city_values.items():
   actual = city_summary.loc[city]
   print(f"\n{city}:")
   print(f"  Revenue: INR {actual['total_revenue']:,.2f}")
   print(f"  Mean order amount: INR {actual['mean_order_amount']:,.2f}")
   print(f"  Order count: {int(actual['order_count'])}")
   assert round(actual["total_revenue"], 2) == expected["total_revenue"]
   assert round(actual["mean_order_amount"], 2) == expected["mean_order_amount"]
   assert int(actual["order_count"]) == expected["order_count"]
print("\nCity reference checks: PASS")
city_summary.to_csv(OUTPUT_DIR / "pandas_city_summary.csv")

# --------------------------------------------------
# 4. PART B: DESCRIPTIVE STATISTICS
# --------------------------------------------------
print("\nPART B1: ORDER AMOUNT DISTRIBUTION")
amount = df["order_amount"].dropna()
mean_amount = amount.mean()
median_amount = amount.median()
skewness = amount.skew()
q1 = amount.quantile(0.25)
q2 = amount.quantile(0.50)
q3 = amount.quantile(0.75)
iqr = q3 - q1
lower_fence = q1 - 1.5 * iqr
upper_fence = q3 + 1.5 * iqr
lower_outliers = int((amount < lower_fence).sum())
upper_outliers = int((amount > upper_fence).sum())
statistics = pd.Series(
   {
       "Count": amount.count(),
       "Mean": mean_amount,
       "Median": median_amount,
       "Skewness": skewness,
       "Minimum": amount.min(),
       "Q1 (25%)": q1,
       "Q2 (50%)": q2,
       "Q3 (75%)": q3,
       "Maximum": amount.max(),
       "IQR": iqr,
       "Lower fence": lower_fence,
       "Upper fence": upper_fence,
       "Outliers below lower fence": lower_outliers,
       "Outliers above upper fence": upper_outliers,
   }
)
print(statistics.to_string())

# --------------------------------------------------
# 5. PART B: CORRELATION MATRIX
# --------------------------------------------------
print("\nPART B2: CORRELATION MATRIX")
correlation_columns = [
   "order_amount",
   "discount_pct",
   "quantity",
   "delivery_minutes",
]
correlation_matrix = df[correlation_columns].corr()
print(correlation_matrix.round(3).to_string())
# Find the pair with the largest absolute correlation
pairs = []
for i in range(len(correlation_columns)):
   for j in range(i + 1, len(correlation_columns)):
       col1 = correlation_columns[i]
       col2 = correlation_columns[j]
       value = correlation_matrix.loc[col1, col2]
       if pd.notna(value):
           pairs.append((col1, col2, value))
largest_pair = max(pairs, key=lambda pair: abs(pair[2]))
print(
   "\nLargest absolute correlation: "
   f"{largest_pair[0]} and {largest_pair[1]} "
   f"({largest_pair[2]:.3f})"
)
correlation_matrix.to_csv(
   OUTPUT_DIR / "pandas_correlation_matrix.csv"
)

# --------------------------------------------------
# 6. SAVE DESCRIPTIVE STATISTICS
# --------------------------------------------------
statistics.to_csv(
   OUTPUT_DIR / "pandas_order_amount_statistics.csv",
   header=["value"],
)
print("\nAnalysis output files saved in data/clean/.")
print("\nAll Pandas cross-checks completed successfully.")