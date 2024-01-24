CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_registered DATE DEFAULT NOW() NOT NULL
);


--CREATE TABLE IF NOT EXISTS user_tokens (
--    user_id bigint PRIMARY KEY UNIQUE NOT NULL,
--    token character varying(64) UNIQUE NOT NULL,
--    FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE
--);