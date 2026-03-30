-- aggregates transactions into monthly summaries by category
{{ config(schema='marts') }}

SELECT
    transaction_month,
    category,
    SUM(amount_abs) AS total_spent,
    COUNT(*) AS transaction_count
FROM {{ ref('int_transactions_enriched') }}
WHERE is_income = FALSE
GROUP BY transaction_month, category