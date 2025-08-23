CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS supplements (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    embedding VECTOR(1536)
);

CREATE INDEX IF NOT EXISTS sup_emb_idx
ON supplements
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

ANALYZE supplements;
