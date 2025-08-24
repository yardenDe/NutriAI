CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS supplements (
    id SERIAL PRIMARY KEY,
    name text NOT NULL,
    description TEXT,
    embedding VECTOR(1536)
);

CREATE INDEX IF NOT EXISTS sup_emb_idx
ON supplements
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

ANALYZE supplements;

CREATE OR REPLACE FUNCTION add_supplements(
    supp_name TEXT,
    supp_description TEXT,
    supp_embedding VECTOR(1536)
)
RETURNS VOID
AS $$
BEGIN
    INSERT INTO supplements (name, description, embedding)
    VALUES (supp_name, supp_description, supp_embedding);
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION find_supplements(
    query_emb VECTOR(1536),
    cnt INT
)
RETURNS TABLE (
    id INT,
    name TEXT,
    description TEXT,
    similarity FLOAT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        s.id, 
        s.name, 
        s.description,
        1 - (s.embedding <-> query_emb) AS similarity
    FROM supplements s
    ORDER BY s.embedding <-> query_emb
    LIMIT cnt;
END;
$$ LANGUAGE plpgsql;


