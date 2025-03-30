import duckdb

conn = duckdb.connect("ecommerce.duckdb")

query_void_cancel_no_initial = """
SELECT COUNT(*) 
FROM transactions 
WHERE status IN ('void', 'cancel') 
AND transaction_id NOT IN (
    SELECT transaction_id FROM transactions WHERE status = 'paid'
);
"""
void_cancel_no_initial = conn.execute(query_void_cancel_no_initial).fetchone()[0]
print(f"\n Void/Cancel without Initial Payment: {void_cancel_no_initial}")

query_negative_amount = "SELECT COUNT(*) FROM transactions WHERE amount < 0"
negative_amount_count = conn.execute(query_negative_amount).fetchone()[0]
print(f"\n Negative Transaction Amounts: {negative_amount_count}")

query_status_distribution = """
SELECT status, COUNT(*) 
FROM transactions 
GROUP BY status
ORDER BY COUNT(*) DESC;
"""
status_distribution = conn.execute(query_status_distribution).fetchall()
print("\n Transaction Status Distribution:")
for status, count in status_distribution:
    print(f"  - {status}: {count} transactions")

for i in range(1, 6):
    print(f"\nProfiling data for daily transactions (Day {i}):")

    query_void_cancel_no_initial_daily = f"""
    SELECT COUNT(*) 
    FROM daily_transactions_day{i} 
    WHERE status IN ('void', 'cancel') 
    AND transaction_id NOT IN (
        SELECT transaction_id FROM daily_transactions_day{i} WHERE status = 'paid'
    );
    """
    void_cancel_no_initial_daily = conn.execute(query_void_cancel_no_initial_daily).fetchone()[0]
    print(f"  - Void/Cancel without Initial Payment: {void_cancel_no_initial_daily}")

    query_negative_amount_daily = f"SELECT COUNT(*) FROM daily_transactions_day{i} WHERE amount < 0"
    negative_amount_count_daily = conn.execute(query_negative_amount_daily).fetchone()[0]
    print(f"  - Negative Transaction Amounts: {negative_amount_count_daily}")

    query_status_distribution_daily = f"""
    SELECT status, COUNT(*) 
    FROM daily_transactions_day{i} 
    GROUP BY status
    ORDER BY COUNT(*) DESC;
    """
    status_distribution_daily = conn.execute(query_status_distribution_daily).fetchall()
    print(f"  - Transaction Status Distribution:")
    for status, count in status_distribution_daily:
        print(f"      - {status}: {count} transactions")

    query_transaction_trends_daily = f"""
    SELECT timestamp::date AS transaction_date, COUNT(*) AS total_transactions
    FROM daily_transactions_day{i}
    GROUP BY transaction_date
    ORDER BY transaction_date;
    """
    transaction_trends_daily = conn.execute(query_transaction_trends_daily).fetchall()

    print(f"  - Daily Transaction Trends (First 10 Days):")
    for date, count in transaction_trends_daily[:10]: 
        print(f"      - {date}: {count} transactions")