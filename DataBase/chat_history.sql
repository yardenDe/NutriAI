-- Chat history table: stores all messages for each user
CREATE TABLE IF NOT EXISTS chat_history (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role TEXT NOT NULL,      -- 'user' or 'assistant'
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index for fast lookup per user
CREATE INDEX IF NOT EXISTS idx_chat_history_user
ON chat_history (user_id);

-- Adds a new chat message
-- Returns: nothing
CREATE OR REPLACE FUNCTION add_chat_message(
    p_user_id INT,
    p_role TEXT,
    p_content TEXT
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO chat_history (user_id, role, content)
    VALUES (p_user_id, p_role, p_content);
END;
$$ LANGUAGE plpgsql;

-- Returns last N messages for a user
-- Returns: role, content, created_at
CREATE OR REPLACE FUNCTION get_last_messages(
    p_user_id INT,
    p_limit INT
)
RETURNS TABLE (
    role TEXT,
    content TEXT,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        h.role,
        h.content,
        h.created_at
    FROM chat_history h
    WHERE h.user_id = p_user_id
    ORDER BY h.created_at DESC
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;


-- Counts how many new messages exist after last summary time
CREATE OR REPLACE FUNCTION count_new_messages(
    p_user_id INT,
    p_last_time TIMESTAMP
)
RETURNS INT AS $$
DECLARE
    c INT;
BEGIN
    SELECT COUNT(*) INTO c
    FROM chat_history
    WHERE user_id = p_user_id
      AND created_at > p_last_time;

    RETURN c;
END;
$$ LANGUAGE plpgsql;

