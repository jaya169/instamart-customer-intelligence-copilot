from pathlib import Path
import pandas as pd
RAW = Path("data/raw")
CLEAN = Path("data/clean")
CLEAN.mkdir(parents=True, exist_ok=True)
# Load the original customer data
customers = pd.read_csv(RAW / "customers.csv")
print("Original customer rows:", len(customers))
# 1. Remove duplicate customer IDs, keeping the first record
customers = customers.drop_duplicates(
   subset=["customer_id"],
   keep="first"
)
# 2. Clean city names
customers["city"] = (
   customers["city"]
   .astype("string")
   .str.strip()
   .str.title()
)
# Standardize known city-name variations
city_mapping = {
   "Bangalore": "Bengaluru",
   "Bengaluru": "Bengaluru",
   "Delhi": "Delhi",
   "New Delhi": "Delhi",
   "Chennai": "Chennai",
   "Mumbai": "Mumbai",
   "Hyderabad": "Hyderabad",
   "Pune": "Pune",
}
customers["city"] = customers["city"].replace(city_mapping)
# 3. Standardize gender values
customers["gender"] = (
   customers["gender"]
   .astype("string")
   .str.strip()
   .str.upper()
)
gender_mapping = {
   "M": "MALE",
   "MALE": "MALE",
   "F": "FEMALE",
   "FEMALE": "FEMALE",
}
customers["gender"] = customers["gender"].replace(gender_mapping)
# Treat unrecognized gender values as missing
customers.loc[
   ~customers["gender"].isin(["MALE", "FEMALE"]),
   "gender"
] = pd.NA
# 4. Convert age to numeric
customers["age"] = pd.to_numeric(
   customers["age"],
   errors="coerce"
)
# Ages outside the plausible range are treated as missing
customers.loc[
   ~customers["age"].between(10, 100),
   "age"
] = pd.NA
# Fill missing ages with the median age of the corresponding gender group
for gender in ["MALE", "FEMALE"]:
   gender_mask = customers["gender"] == gender
   median_age = customers.loc[gender_mask, "age"].median()
   if pd.notna(median_age):
       customers.loc[gender_mask, "age"] = (
           customers.loc[gender_mask, "age"].fillna(median_age)
       )
# Handle any remaining missing ages using the overall median
overall_median_age = customers["age"].median()
if pd.notna(overall_median_age):
   customers["age"] = customers["age"].fillna(overall_median_age)
# Standardize gender values to lowercase
customers["gender"] = customers["gender"].str.lower()
# Replace missing gender values with "unknown"
customers["gender"] = customers["gender"].fillna("unknown")
# 5. Standardize signup dates
customers["signup_date"] = pd.to_datetime(
   customers["signup_date"],
   errors="coerce"
)
# Save cleaned data
output_path = CLEAN / "customers_clean.csv"
customers.to_csv(output_path, index=False)
print("\nCustomer cleaning completed.")
print("Cleaned customer rows:", len(customers))
print("Output file:", output_path)
print("\nRemaining missing values:")
print(customers.isna().sum().to_string())
print("\nCleaned sample:")
print(customers.head().to_string(index=False))