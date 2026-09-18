-- Q1(e) DuckDB + MinIO + PostgreSQL federated query

SELECT
    p.product_name,
    COUNT(*) AS line_count,
    SUM(
        CAST(s.qty AS DOUBLE) * CAST(s.unit_price AS DOUBLE)
    ) AS revenue
FROM read_csv(
    's3://annapurna/raw/sales/sales/SALES_S01_*.csv',
    header=true,
    all_varchar=true
) s
JOIN pg.products p
    ON s.product_code = p.product_code
GROUP BY p.product_name
ORDER BY revenue DESC
LIMIT 10;

EXPLAIN
SELECT
    p.product_name,
    COUNT(*) AS line_count,
    SUM(
        CAST(s.qty AS DOUBLE) * CAST(s.unit_price AS DOUBLE)
    ) AS revenue
FROM read_csv(
    's3://annapurna/raw/sales/sales/SALES_S01_*.csv',
    header=true,
    all_varchar=true
) s
JOIN pg.products p
    ON s.product_code = p.product_code
GROUP BY p.product_name;