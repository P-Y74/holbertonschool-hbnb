CREATE TABLE IF NOT EXISTS Amenity(
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);
CREATE TABLE IF NOT EXISTS place_amenity(
    place_id CHAR(36),
    amenity_id CHAR(36),
    PRIMARY KEY (place_id, amenity_id)
    FOREIGN KEY (place_id) REFERENCES Place(id),
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id)
);
