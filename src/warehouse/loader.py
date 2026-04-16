import duckdb
from pathlib import Path
import pandas as pd
from config import DB_PATH

DEBUG = False


class Loader:
    def get_connection(self) -> duckdb.DuckDBPyConnection:
        # should auto create db file if not exists?
        con = duckdb.connect(str(DB_PATH))

        if DEBUG:
            print('connected to duckdb')

        return con

    def init_warehouse(self):
        con = self.get_connection()

        con.sql("CREATE SCHEMA IF NOT EXISTS raw")
        con.sql("""CREATE TABLE IF NOT EXISTS raw.transactions 
                (transaction_date DATE, 
                post_date DATE, 
                description VARCHAR,
                amount FLOAT, 
                category VARCHAR,
                source_bank VARCHAR,
                account_type VARCHAR,
                original_description VARCHAR,
                transaction_id VARCHAR PRIMARY KEY)""")

        if DEBUG:
            print('created warehouse')

        con.close()

    def load_transactions(self, df: pd.DataFrame) -> int:
        con = self.get_connection()

        before = con.sql("SELECT COUNT(*) FROM raw.transactions").fetchone()[0]
        con.sql("""
        INSERT OR IGNORE INTO raw.transactions 
        (transaction_date, post_date, original_description, description, 
        amount, category, source_bank, account_type, transaction_id)
        SELECT * FROM df
        """)
        after = con.sql("SELECT COUNT(*) FROM raw.transactions").fetchone()[0]

        new_rows_added = after - before

        if DEBUG:
            print(f"{new_rows_added} Rows Added!")

        con.close()
        return new_rows_added

    def update_categories(self, df: pd.DataFrame):
        con = self.get_connection()

        con.register('categorized', df)

        con.sql("""
                UPDATE raw.transactions
                SET category = categorized.category
                FROM categorized
                WHERE raw.transactions.transaction_id = categorized.transaction_id
                AND (raw.transactions.category IS NULL OR raw.transactions.category = 'uncategorized')
                """)
        
        con.close()
