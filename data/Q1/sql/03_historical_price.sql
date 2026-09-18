-- Q1(d) Historical price

SELECT
    p.product_code,
    p.product_name,
    pr.selling_price,
    pr.effective_from,
    pr.effective_to
FROM pg.products p
JOIN pg.price_revisions pr
    ON p.product_sk = pr.product_sk
WHERE pr.effective_from <= DATE '2024-03-31'
  AND (
      pr.effective_to IS NULL
      OR pr.effective_to >= DATE '2024-03-01'
  )
ORDER BY p.product_code
LIMIT 20;