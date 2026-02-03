-- Enables vector support for semantic search
CREATE EXTENSION IF NOT EXISTS vector;

-- Supplements table: stores supplement info + vector embedding
CREATE TABLE IF NOT EXISTS supplements (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    embedding VECTOR(384)
);

-- Index for vector similarity search
CREATE INDEX IF NOT EXISTS idx_supplements_embedding
ON supplements
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Inserts a new supplement with embedding
-- Returns: nothing
CREATE OR REPLACE FUNCTION add_supplements(
    p_name TEXT,
    p_description TEXT,
    p_embedding VECTOR(384)
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO supplements (name, description, embedding)
    VALUES (p_name, p_description, p_embedding);
END;
$$ LANGUAGE plpgsql;

-- Finds similar supplements by embedding
-- Returns: id, name, description, similarity score
CREATE OR REPLACE FUNCTION find_supplements(
    p_query VECTOR(384),
    p_limit INT
)
RETURNS TABLE(
    id INT,
    name TEXT,
    description TEXT,
    similarity FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        s.id,
        s.name,
        s.description,
        1 - (s.embedding <=> p_query) AS similarity
    FROM supplements s
    ORDER BY s.embedding <=> p_query
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;
