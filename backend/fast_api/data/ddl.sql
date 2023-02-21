CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    username TEXT NOT NULL UNIQUE,
    passphrase TEXT NOT NULL
    );

-- INSERT INTO users (username, passphrase)
-- VALUES ('admin', 'admin');