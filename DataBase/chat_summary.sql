-- Chat summary table: stores conversation summary per user
CREATE TABLE IF NOT EXISTS chat_summary (
    user_id INT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    summary TEXT,
    updated_at TIMESTAMP DEFAULT NOW()
);

