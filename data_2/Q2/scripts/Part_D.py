import psycopg2, csv, glob, time

conn=psycopg2.connect(
    dbname="annapurna",
    user="postgres",
    password="postgres",
    host="localhost",
    port=5432
)

cur=conn.cursor()

with open("Part_D.sql",encoding="utf-8") as f:
    cur.execute(f.read())

rows=[]

for file in glob.glob("notices\\part-*.csv"):
    with open(file,encoding="utf-8-sig",newline="") as f:
        for r in csv.DictReader(f):
            rows.append((
                r["notice_id"],r["portal_id"],r["published_at"],
                r["title"],r["body"],r["estimated_value"],
                r["closing_date"]
            ))

cur.executemany(
"""INSERT INTO q2_notice
(notice_id,portal_id,published_at,title,body,estimated_value,closing_date)
VALUES (%s,%s,%s,%s,%s,%s,%s)""",rows)

cur.execute("ANALYZE q2_notice")

cur.execute("""
SELECT band_no,bucket_hash,COUNT(*)
FROM q2_lsh_bucket
GROUP BY band_no,bucket_hash
ORDER BY COUNT(*) DESC LIMIT 1
""")

print("Database loaded notices:",len(rows))
print("Schema created successfully.")

conn.commit()
cur.close()
conn.close()