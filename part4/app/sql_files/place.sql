CREATE TABLE IF NOT EXISTS Place(
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36),
   FOREIGN KEY (owner_id) REFERENCES User(id)
);