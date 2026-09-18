-- Q1(c) Revenue by line type

SELECT
    line_type,
    COUNT(*) AS rows,
    SUM(
        CAST(qty AS DOUBLE) * CAST(unit_price AS DOUBLE)
    ) AS amount
FROM read_csv(
    's3://annapurna/raw/sales/sales/SALES_S01_*.csv',
    header=true,
    all_varchar=true
)
GROUP BY line_type
ORDER BY line_type;