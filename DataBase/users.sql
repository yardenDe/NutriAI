-- Users table: stores basic account info
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Authenticates a user
-- Returns: user id if credentials match, NULL otherwise
CREATE OR REPLACE FUNCTION authenticate(
    p_username TEXT,
    p_password TEXT
)
RETURNS INT AS $$
DECLARE uid INT;
BEGIN
    SELECT id INTO uid
    FROM users
    WHERE username = p_username
      AND password = p_password;

    RETURN uid; 
END;
$$ LANGUAGE plpgsql;
