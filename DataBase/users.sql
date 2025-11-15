-- Users table: stores basic account info
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index for faster username lookups
CREATE INDEX IF NOT EXISTS idx_users_username
ON users (username);

-- Trigger function: ensures username is unique before insertion
CREATE OR REPLACE FUNCTION check_user_unique()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM users WHERE username = NEW.username) THEN
        RETURN NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: runs before inserting a new user
CREATE TRIGGER trg_user_unique
BEFORE INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION check_user_unique();

-- Adds a new user (the trigger handles duplicates)
-- Returns: user id(or Null)
CREATE OR REPLACE FUNCTION add_user(
    p_username TEXT,
    p_password TEXT
)
RETURNS INT AS $$
DECLARE new_id INT;
BEGIN
    INSERT INTO users (username, password)
    VALUES (p_username, p_password)
    RETURNING id INTO new_id;
    RETURN new_id;
END;
$$ LANGUAGE plpgsql;

-- Finds a user by username
-- Returns: id, username, password (or Null)
CREATE OR REPLACE FUNCTION find_user(
    p_username TEXT
)
RETURNS TABLE (
    id INT,
    username TEXT,
    password TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT u.id, u.username, u.password
    FROM users u
    WHERE u.username = p_username;
END;
$$ LANGUAGE plpgsql;

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
