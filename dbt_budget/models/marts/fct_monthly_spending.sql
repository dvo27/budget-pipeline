-- aggregates transactions into monthly summaries by category
{{ config(schema='marts') }}

SELECT
    transaction_month,
    category,
    SUM(amount_abs) AS total_spent,
    COUNT(*) AS transaction_count
FROM {{ ref('int_transactions_enriched') }}
WHERE is_income = FALSE AND category <> 'rent' AND NOT (category = 'reimbursement' AND amount_abs > 1000)
GROUP BY transaction_month, category