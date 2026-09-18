-- Q1(b) Idempotency verification

SELECT count(*) AS row_count
FROM read_csv(
    's3://annapurna/raw/sales/sales/SALES_S01_*.csv',
    header=true,
    all_varchar=true
);

SELECT
    count(*) AS row_count,
    md5(string_agg(
        bill_no || '|' || line_no || '|' || product_code || '|' ||
        qty || '|' || unit_price || '|' || line_type || '|' || ts,
        '||' ORDER BY bill_no, line_no, product_code, qty, unit_price, line_type, ts
    )) AS checksum
FROM read_csv(
    's3://annapurna/raw/sales/sales/SALES_S01_*.csv',
    header=true,
    all_varchar=true
);