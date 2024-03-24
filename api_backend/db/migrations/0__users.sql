CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_registered DATE DEFAULT NOW() NOT NULL
);
