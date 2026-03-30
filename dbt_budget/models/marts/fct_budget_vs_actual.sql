{{ config(schema='marts') }}

SELECT
    transaction_month,
    -- This is called conditional aggregation, i never seen it before but its cool
    -- lets you sum different subsets in the same query without filtering
    SUM(CASE WHEN is_income = TRUE THEN amount ELSE 0 END) AS monthly_income,
    SUM(CASE WHEN is_income = FALSE THEN amount_abs ELSE 0 END) AS monthly_expenses
FROM {{ ref('int_transactions_enriched') }}
GROUP BY transaction_month