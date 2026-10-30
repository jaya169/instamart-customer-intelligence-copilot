from pathlib import Path
import pandas as pd
# 1. Define input and output directories
RAW = Path("data/raw")
CLEAN = Path("data/clean")
# 2. Create the clean directory if it doesn't exist
CLEAN.mkdir(parents=True, exist_ok=True)
# 3. Load the original product data
products = pd.read_csv(RAW / "products.csv")
print("--- ORIGINAL PRODUCT DATA ---")
print("Dataset shape:", products.shape)
# 4. Clean column names
products.columns = products.columns.str.strip().str.lower()
# 5. Remove exact duplicate rows
products = products.drop_duplicates()
# 6. Clean text columns
for column in ["product_name", "category"]:
   if column in products.columns:
       products[column] = (
           products[column]
           .astype("string")
           .str.strip()
       )
# 7. Clean product ID
if "product_id" in products.columns:
   products["product_id"] = (
       products["product_id"]
       .astype("string")
       .str.strip()
   )
# 8. Convert product price to numeric
if "price_inr" in products.columns:
   products["price_inr"] = pd.to_numeric(
       products["price_inr"],
       errors="coerce"
   )
# 9. Remove records with missing essential identifiers
essential_columns = [
   column
   for column in ["product_id", "product_name"]
   if column in products.columns
]
if essential_columns:
   products = products.dropna(subset=essential_columns)
# 10. Validate product prices
if "price_inr" in products.columns:
   invalid_prices = products["price_inr"].le(0)
   products.loc[invalid_prices, "price_inr"] = pd.NA
# 11. Save the cleaned dataset
output_file = CLEAN / "products_clean.csv"
products.to_csv(output_file, index=False)
# 12. Display cleaning results
print("\n--- PRODUCT CLEANING RESULTS ---")
print("Cleaned product rows:", len(products))
print("Missing values:\n", products.isnull().sum())
print("Duplicate rows:", products.duplicated().sum())
print("Output file:", output_file)
print("\nProduct cleaning completed.")