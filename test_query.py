import duckdb
from config import DB_PATH
con = duckdb.connect(DB_PATH)

# # See all tables/views in your database
# con.sql("SHOW ALL TABLES").show()

# # Look at your staging output
# con.sql("SELECT * FROM main_staging.stg_transactions LIMIT 100").show()

# # Look at your intermediate output
# con.sql("SELECT * FROM main_intermediate.int_transactions_enriched LIMIT 10").show()

# # Check what columns and types you have
# con.sql("DESCRIBE main_intermediate.int_transactions_enriched").show()

# # Explore the data — what categories exist?
# con.sql("SELECT DISTINCT category FROM main_intermediate.int_transactions_enriched").show()

# # How many transactions per bank?
# con.sql("SELECT source_bank, COUNT(*) FROM main_intermediate.int_transactions_enriched GROUP BY source_bank").show()

# con.sql("SELECT * FROM main_marts.fct_budget_vs_actual ORDER BY transaction_month").show()
# con.sql("SELECT * FROM main_marts.fct_monthly_spending ORDER BY transaction_month, total_spent DESC").show()


# con.sql("SELECT DISTINCT description FROM raw.transactions WHERE category IS NULL").show(max_rows=500, max_width=200)

# con.sql("SELECT * FROM main_marts.fct_budget_vs_actual ORDER BY transaction_month").show()

# con.sql("""
#     SELECT transaction_month, category, total_spent, transaction_count
#     FROM main_marts.fct_monthly_spending
#     WHERE transaction_month >= '2026-01%'
#     AND transaction_month < '2026-01%'
#     ORDER BY transaction_month, total_spent DESC
# """).show(max_rows=100, max_width=200)

con.sql("""
    SELECT transaction_date, description, amount, source_bank
    FROM raw.transactions
    WHERE category = 'uncategorized'
    AND transaction_date >= '2026-01-01'
    AND transaction_date < '2026-02-01'
    ORDER BY amount DESC
""").show(max_rows=200, max_width=300)

con.sql("""
    SELECT transaction_date, description, amount, source_bank
    FROM raw.transactions
    WHERE category = 'uncategorized'
    AND transaction_date >= '2026-02-01'
    AND transaction_date < '2026-03-01'
    ORDER BY amount DESC
""").show(max_rows=200, max_width=300)

