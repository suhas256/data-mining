DROP TABLE IF EXISTS q2_notice_card;
DROP TABLE IF EXISTS q2_opportunity_card;
DROP TABLE IF EXISTS q2_lsh_bucket;
DROP TABLE IF EXISTS q2_notice;

CREATE TABLE q2_notice (
    notice_id TEXT PRIMARY KEY,
    portal_id TEXT NOT NULL,
    published_at DATE,
    title TEXT,
    body TEXT,
    estimated_value NUMERIC,
    closing_date DATE
);

CREATE TABLE q2_lsh_bucket (
    band_no INTEGER NOT NULL,
    bucket_hash TEXT NOT NULL,
    notice_id TEXT NOT NULL REFERENCES q2_notice(notice_id)
);

CREATE INDEX q2_lsh_bucket_idx
ON q2_lsh_bucket(band_no, bucket_hash);

CREATE INDEX q2_lsh_notice_idx
ON q2_lsh_bucket(notice_id);

CREATE TABLE q2_opportunity_card (
    card_id TEXT PRIMARY KEY,
    anchor_notice_id TEXT UNIQUE NOT NULL
);

CREATE TABLE q2_notice_card (
    notice_id TEXT PRIMARY KEY REFERENCES q2_notice(notice_id),
    card_id TEXT NOT NULL REFERENCES q2_opportunity_card(card_id)
);

CREATE INDEX q2_notice_card_idx
ON q2_notice_card(card_id);