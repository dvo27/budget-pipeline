import duckdb
from pathlib import Path
import pandas as pd
from config import DB_PATH


class Loader:
    def get_connection(self) -> duckdb.DuckDBPyConnection:
        # should auto create db file if not exists?
        con = duckdb.connect(str(DB_PATH))
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
       
        con.close()
    
    def load_transactions(self, df: pd.DataFrame) -> int:
        con = self.get_connection()
        
        before = con.sql("SELECT COUNT(*) FROM raw.transactions").fetchone()[0]
        con.sql("INSERT OR IGNORE INTO raw.transactions SELECT * FROM df")
        after = con.sql("SELECT COUNT(*) FROM raw.transactions").fetchone()[0]
        new_rows_added = after - before
        
        print(f"{new_rows_added} Rows Added!")
        
        con.close()
        return new_rows_added
