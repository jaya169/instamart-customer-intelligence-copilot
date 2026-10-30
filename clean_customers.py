import pandas as pd
from pathlib import Path
# Define input and output paths
RAW_DIR = Path("data/raw")
CLEAN_DIR = Path("data/clean")
CLEAN_DIR.mkdir(parents=True, exist_ok=True)
# Load raw customers
customers = pd.read_csv(RAW_DIR / "customers.csv")
# Make a copy of the raw data
customers_clean = customers.copy()
# --------------------------------------------------
# 1. STANDARDISE CITY NAMES
# Remove leading/trailing spaces and apply title case
# --------------------------------------------------
customers_clean["city"] = (
   customers_clean["city"]
   .astype("string")
   .str.strip()
   .str.title()
)
# --------------------------------------------------
# 2. STANDARDISE GENDER
# Map every spelling to male, female, or unknown
# --------------------------------------------------
gender_mapping = {
   "male": "male",
   "m": "male",
   "man": "male",
   "female": "female",
   "f": "female",
   "woman": "female",
   "unknown": "unknown",
   "": "unknown",
}
customers_clean["gender"] = (
   customers_clean["gender"]
   .fillna("")
   .astype(str)
   .str.strip()
   .str.lower()
   .map(gender_mapping)
   .fillna("unknown")
)
# --------------------------------------------------
# 3. CLEAN AGE VALUES
# Ages outside 10-100 become missing
# --------------------------------------------------
customers_clean["age"] = pd.to_numeric(
   customers_clean["age"],
   errors="coerce"
)
customers_clean.loc[
   ~customers_clean["age"].between(10, 100),
   "age"
] = pd.NA
# Fill missing ages using the median age of each city
customers_clean["age"] = customers_clean["age"].fillna(
   customers_clean.groupby("city")["age"].transform("median")
)
# --------------------------------------------------
# 4. CONVERT SIGNUP DATE TO DATETIME
# --------------------------------------------------
customers_clean["signup_date"] = pd.to_datetime(
   customers_clean["signup_date"],
   errors="coerce"
)
# --------------------------------------------------
# 5. SAVE CLEANED CUSTOMERS
# --------------------------------------------------
customers_clean.to_csv(
   CLEAN_DIR / "customers_clean.csv",
   index=False
)
# --------------------------------------------------
# 6. VALIDATE RESULTS
# --------------------------------------------------
print("\nCITY COUNTS:")
print(customers_clean["city"].value_counts())
print("\nGENDER COUNTS:")
print(customers_clean["gender"].value_counts())
print("\nMISSING AGES:")
print(customers_clean["age"].isna().sum())
print("\nAGE RANGE:")
print(customers_clean["age"].min(), customers_clean["age"].max())
print("\nSIGNUP DATE DATA TYPE:")
print(customers_clean["signup_date"].dtype)
print("\nCLEANED CUSTOMERS SAVED SUCCESSFULLY.")