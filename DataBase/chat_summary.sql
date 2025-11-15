-- Chat summary table: stores conversation summary per user
CREATE TABLE IF NOT EXISTS chat_summary (
    user_id INT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    summary TEXT,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Updates or inserts summary text
-- Returns: nothing
CREATE OR REPLACE FUNCTION update_chat_summary(
    p_user_id INT,
    p_summary TEXT
)
RETURNS VOID AS $$
BEGIN
    UPDATE chat_summary
    SET summary = p_summary, updated_at = NOW()
    WHERE user_id = p_user_id;

    IF NOT FOUND THEN
        INSERT INTO chat_summary (user_id, summary)
        VALUES (p_user_id, p_summary);
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Returns the stored summary
-- Returns: summary text (or NULL if not exists)
CREATE OR REPLACE FUNCTION get_chat_summary(
    p_user_id INT
)
RETURNS TEXT AS $$
DECLARE s TEXT;
BEGIN
    SELECT summary INTO s
    FROM chat_summary
    WHERE user_id = p_user_id;

    RETURN s;  -- NULL if no summary exists
END;
$$ LANGUAGE plpgsql;
