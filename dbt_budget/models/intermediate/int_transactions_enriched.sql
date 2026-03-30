-- This model reads from the staging model and enriches each transaction with budget context
{{ config(schema='intermediate') }}

SELECT 
    *,
    CASE
        WHEN is_income = TRUE THEN 'income'
        ELSE 'uncategorized'
    END AS budget_bucket,
    STRFTIME(transaction_date, '%Y-%m') AS transaction_month
FROM {{ ref('stg_transactions') }}