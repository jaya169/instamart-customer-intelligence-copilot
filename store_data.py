import sqlite3
from pathlib import Path
import pandas as pd
# Define project paths
BASE_DIR = Path(__file__).resolve().parent
CLEAN_DIR = BASE_DIR / "data" / "clean"
DB_PATH = BASE_DIR / "data" / "instamart.db"
# Ensure the required directories exist
CLEAN_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
# Load the three cleaned datasets
customers = pd.read_csv(CLEAN_DIR / "customers_clean.csv")
products = pd.read_csv(CLEAN_DIR / "products_clean.csv")
orders = pd.read_csv(CLEAN_DIR / "orders_clean.csv")
# Store order_ts as text in YYYY-MM-DD HH:MM:SS format
orders["order_ts"] = pd.to_datetime(
   orders["order_ts"], errors="raise"
).dt.strftime("%Y-%m-%d %H:%M:%S")
# Write the three clean CSV files
customers.to_csv(CLEAN_DIR / "customers_clean.csv", index=False)
products.to_csv(CLEAN_DIR / "products_clean.csv", index=False)
orders.to_csv(CLEAN_DIR / "orders_clean.csv", index=False)
# Write the datasets to SQLite
with sqlite3.connect(DB_PATH) as connection:
   customers.to_sql(
       "customers", connection, if_exists="replace", index=False
   )
   products.to_sql(
       "products", connection, if_exists="replace", index=False
   )
   orders.to_sql(
       "orders", connection, if_exists="replace", index=False
   )
print("Clean CSV files saved successfully.")
print("SQLite database saved to data/instamart.db")
print("Tables created: customers, products, orders")