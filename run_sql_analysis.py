import sqlite3
from pathlib import Path
import pandas as pd
# Define paths
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "instamart.db"
SQL_PATH = BASE_DIR / "sql" / "queries.sql"
# Load all seven SQL queries
sql_text = SQL_PATH.read_text(encoding="utf-8")
# Split queries using the Q1, Q2, ..., Q7 comment markers.
queries = {}
for i in range(1, 8):
   start_marker = f"-- Q{i}"
   start = sql_text.find(start_marker)
   if start == -1:
       raise ValueError(f"Q{i} was not found in queries.sql")
   next_marker = f"-- Q{i + 1}"
   end = sql_text.find(next_marker, start + len(start_marker))
   if end == -1:
       end = len(sql_text)
   query_block = sql_text[start:end]
   # Remove SQL comments and keep executable SQL.
   executable_lines = [
       line for line in query_block.splitlines()
       if not line.strip().startswith("--")
   ]
   query = "\n".join(executable_lines).strip()
   if query:
       queries[f"Q{i}"] = query
# Execute queries against SQLite
with sqlite3.connect(DB_PATH) as conn:
   for name, query in queries.items():
       result = pd.read_sql_query(query, conn)
       print("\n" + "=" * 60)
       print(f"{name} RESULTS")
       print("=" * 60)
       print(f"Rows returned: {len(result)}")
       print(result.to_string(index=False))
       # Save each query result for inspection.
       output_path = (
           BASE_DIR / "sql" / f"{name.lower()}_results.csv"
       )
       result.to_csv(output_path, index=False)
print("\nAll seven SQL queries executed successfully.")