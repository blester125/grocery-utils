DROP TABLE IF EXISTS locations;

CREATE TABLE locations(
    loc_id INTEGER PRIMARY KEY AUTOINCREMENT,
    loc TEXT UNIQUE,
    priority INTEGER UNIQUE
);

DROP TABLE if EXISTS types;

CREATE TABLE types(
    type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT UNIQUE,
    type_plural TEXT UNIQUE
);

DROP TABLE if EXISTS items;

CREATE TABLE items(
    item_id INTEGER PRIMARY KEY,
    name TEXT,
    quantity FLOAT,
    type_id INTEGER,
    loc_id INTEGER,
    buy BOOLEAN,
    FOREIGN KEY(type_id) REFERENCES types(type_id),
    FOREIGN KEY(loc_id) REFERENCES locations(loc_id)
);

.separator ,

.import data/locations-without-header.csv locations

.import data/types-without-header.csv types

.import data/items-without-header.csv items
