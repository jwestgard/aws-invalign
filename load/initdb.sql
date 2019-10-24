CREATE TABLE IF NOT EXISTS inventories (
    id INTEGER PRIMARY KEY,
    filename TEXT NOT NULL,
    batch_name TEXT NOT NULL,
    batch_number INTEGER,
    batch_date TEXT,
    bytes INTEGER NOT NULL,
    md5 TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY,
    filename TEXT NOT NULL,
    sourceline INTEGER NOT NULL,
    inventory_id INTEGER,
    FOREIGN KEY(inventory_id) REFERENCES inventories(id)
);
