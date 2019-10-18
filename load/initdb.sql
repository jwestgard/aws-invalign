CREATE TABLE inventories (
    id INTEGER PRIMARY KEY,
    filename TEXT NOT NULL,
    batch TEXT NOT NULL,
    bytes INTEGER NOT NULL,
    md5 TEXT NOT NULL
);

CREATE TABLE assets (
    id INTEGER PRIMARY KEY,
    filename TEXT NOT NULL,
    sourceline INTEGER NOT NULL,
    inventory_id INTEGER,
    FOREIGN KEY(inventory_id) REFERENCES inventories(id)
);
