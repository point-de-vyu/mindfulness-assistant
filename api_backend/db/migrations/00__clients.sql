CREATE TABLE IF NOT EXISTS client_types(
    id serial PRIMARY KEY UNIQUE NOT NULL,
    name VARCHAR(30) UNIQUE NOT NULL
);

-- 100+ for telegram
-- 200+ for web
CREATE TABLE IF NOT EXISTS clients(
    id INT PRIMARY KEY,
    client_type_id INT,
    token VARCHAR(64) UNIQUE NOT NULL,
    FOREIGN KEY(client_type_id) REFERENCES client_types(id) ON UPDATE CASCADE ON DELETE CASCADE
);



CREATE TABLE IF NOT EXISTS clients_users (
    client_id INT,
    user_id_from_client BIGINT,
    user_id BIGINT,
    PRIMARY KEY(client_id, user_id_from_client),
    FOREIGN KEY (client_id) REFERENCES clients(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE
);