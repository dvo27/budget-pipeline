-- Creates table view of our transactions df as a SQL table with a column that checks whether a transaction was income from direct deposit

{{ config(schema='staging') }}

SELECT 
    *, 
    ABS(amount) AS amount_abs,
    CASE 
        WHEN UPPER(description) LIKE '%UNIVERSITY OF CA%' THEN TRUE
        WHEN UPPER(description) LIKE '%VENMO CASHOUT%' THEN TRUE
        ELSE FALSE
    END AS is_income
FROM raw.transactions
WHERE amount IS NOT NULL 
    AND transaction_date IS NOT NULL
