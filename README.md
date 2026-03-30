------------
Purpose:
------------
My money is spread across various apps and platforms. Tracking how much money is in where takes a lot of work and remembering. 
I don't want to go back and forth between multiple apps and logging the values from each into a manual spreadsheet and then calculating.
I want to be able to see how much money I have in my checkings, debts to pay off from credit cards, how much I have saved in my HYSA,
and how my investments are doing. Currently, I have to go between Wells Fargo, Chase, Discover, Robinhood, and Marcus, pull values from
all those apps into a spreadsheet, and manually track things. This is too time consuming. Additoinally, I want to be able to track my budget
from this app. Currently, when I get paid, I also have to put that into a spreadsheet and manually divide things out into my budget split (50/30/20). 
Then I put each transaction into what I think are their respective categories. The app should handle budget tracking automatically, from my bank and 
credit cards. It should display each budget split and how much is left from each check.

------------
Features:
------------
- Main page that displays values for the month:
    - Current checkings amount
    - Total debt amount
    - Amount left to spend on budget
    - Month's saved amount
    - Month's earned amount
    - Month's budget split

- Investment Page:
    - Growth visualizations over time
    - See what stocks you're invested in
    - See which stocks made most returns
    - See which stocks lost the most
    - Select view by month, week, day

- Budget Page:
    - Budget splitting
        - Enter your paycheck amount
        - Select your split (ex. 50/30/20, 60/30/10, 70/20/10)
        - Auto-split budget amount by category
        - Auto-pulls your transactions from your card for the month and decrements each budget catgory by transaction
        - See how much you spent and have left in each category in detail

- Savings Page:
    - See how much is in each of your savings accounts (HYSA/Marcus and Fidelity Roth IRA)
    - Show visualizations of growth over time
    - Maybe have a tool that predicts how much growth over time based on how much you add?

------------
Tech Stack
------------
- Python
    - Pandas for data manipulation (cleaning, transforming)
    - Scikit-learn for ML features
    - DuckDB for database management and storage
    - Streamlit front end
    
-----------------
What I've Learned
-----------------
- DBT: Data Build Tool, focuses on the T part of ELT. Transforms data stored in data warehouse by using modular and reusable SQL SELECT 
       statements to build tables and views.
    - Our DBT follows this layered architecture:
        - raw.transactions  →  stg_transactions  →  int_transactions_enriched  →  marts

- Creating SQL tables should have columns created in the same order as the schema of our normalized dataframes
- SQL SELECT statements go in this order:
    - SELECT (columns) -> FROM (table) -> WHERE (filters)

- When using GROUP BY, only select what you're grouping by, plus your aggregations
- ex:
        SELECT
            transaction_month,
            category,
            SUM(amount_abs) AS total_spent,
            COUNT(*) AS transaction_count
        FROM {{ ref('int_transactions_enriched') }}
        WHERE is_income = FALSE
        GROUP BY transaction_month, category

- Use '= FALSE' to check for FALSE, 'IS FALSE' is used to check for NULL



-----------------
Premise
-----------------
- Raw transaction csv files uploaded to respective files (chase, discover, wells_fargo)
- Respective parsers ingest raw csv files and parse it into pandas DataFrames that fit our predetermined schema we created in config.py
- Then, loader.py initalizes the duckdb data warehouse that will store our transactions as SQL tables
- After warehouse has been created and our table has been made according to transaction schema, we load each transaction from the parsed DataFrames
- Transactions are loaded into the raw.transactions table where our DBT models will work on transforming the data to add further context in individual layers
    - ex. Whether the transaction was income, categorizing it according to config categories, grouping by month, how much of our budget was spent or saved, etc
