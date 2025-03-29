import pandas as pd
import duckdb

conn = duckdb.connect("ecommerce.duckdb")

transaction_data_path = "historical_transaction.csv"
df = pd.read_csv(transaction_data_path)

conn.register("df_view", df)
conn.execute("CREATE TABLE transactions AS SELECT * FROM df_view")

daily_files = [f'daily_transaction_day{i}.csv' for i in range(1, 6)]

for i, daily_file in enumerate(daily_files, start=1):
    daily_df = pd.read_csv(daily_file)
    table_name = f"daily_transactions_day{i}"
    
    conn.register("daily_df_view", daily_df)
    
    conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM daily_df_view")

total_transactions = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
print(f"Total transactions in transactions table: {total_transactions}")

for i in range(1, 6):
    result = conn.execute(f"SELECT COUNT(*) FROM daily_transactions_day{i}").fetchone()[0]
    print(f"Total transactions in daily_transactions_day{i}: {result}")