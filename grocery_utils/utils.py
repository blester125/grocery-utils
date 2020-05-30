import sqlite3
from typing import Dict, List
from itertools import zip_longest


def reflow(grouped: Dict[str, List[str]], count: int = 100) -> List[List[str]]:
    columns = []
    column = []
    for loc, group in grouped.items():
        if len(column) + 1 + len(group) > count:
            columns.append(column)
            column = []
        column.append(f"{loc}:")
        column.extend(group)
        column.append("")
    if column:
        columns.append(column)

    max_per_column = [len(max(col, key=lambda x: len(x))) for col in columns]
    lines = []
    for col in zip_longest(*columns, fillvalue=""):
        line = []
        for c, width in zip(col, max_per_column):
            line.append(c.ljust(width))
        lines.append("   ".join(line))
    return lines


def insert_location(conn, location, priority):
    with conn:
        c = conn.cursor()
        if priority == "":
            priority = c.execute("SELECT MAX(priority) + 1 FROM locations").fetchone()[0]
        c.execute("UPDATE locations SET priority = priority + 1 WHERE priority >= ?", (priority,))
        c.execute("INSERT INTO locations(loc, priority) VALUES(?, ?)", (location, priority))
        return priority, c.lastrowid


def update_location_priority(conn, location, new_prio):
    # Something weird is happening here because this is updating the prios correctly but the unique constraint is failing.
    with conn:
        c = conn.cursor()
        old_prio = c.execute("SELECT priority FROM locations WHERE loc = ?", (location,)).fetchone()[0]
        c.execute("UPDATE locations SET priority = ? WHERE loc = ?", (-1, location))
        print(tabulate(c.execute("SELECT * FROM locations ORDER BY priority").fetchall()))
        sql = """
            UPDATE locations
            SET priority = CASE
                WHEN ? > ? THEN
                    CASE
                        WHEN priority <= ? AND priority > ? THEN priority - 1
                        ELSE priority
                    END
                WHEN ? < ? THEN
                    CASE
                        WHEN priority < ? AND priority > ? THEN priority + 1
                        ELSE priority
                    END
                ELSE priority
            END
            WHERE loc != ?;
        """
        c.execute(sql, (new_prio, old_prio, new_prio, old_prio, new_prio, old_prio, old_prio, new_prio, location))
        print(tabulate(c.execute("SELECT * FROM locations ORDER BY priority").fetchall()))
        c.execute("UPDATE locations SET priority = ? WHERE loc = ?", (new_prio, location))
        print(tabulate(c.execute("SELECT * FROM locations ORDER BY priority").fetchall()))
        return old_prio, c.lastrowid


def update_location_name(conn, old_name, new_name):
    with conn:
        c = conn.cursor()
        c.execute("UPDATE locations SET loc = ? WHERE loc = ?", (new_name, old_name))
        return c.lastrowid


def delete_location(conn, location):
    # Something weird is happening here because this is updating the prios correctly but the unique constraint is failing.
    from tabulate import tabulate

    with conn:
        c = conn.cursor()
        prio = c.execute("SELECT priority FROM locations WHERE loc = ?", (location,)).fetchone()[0]
        print(prio)
        c.execute("DELETE FROM locations WHERE loc = ?", (location,))
        print(tabulate(c.execute("SELECT * FROM locations ORDER BY priority").fetchall()))
        print(tabulate(c.execute("SELECT * FROM locations WHERE priority > ? ORDER BY priority", (prio,))))
        c.execute("UPDATE locations SET priority = priority - 1 WHERE priority > ?", (prio,))
        return c.lastrowid


def insert_type(conn, type_name, plural):
    with conn:
        c = conn.cursor()
        c.execute("INSERT INTO types(type, type_plural) VALUES(?, ?)", (type_name, plural))
        return c.lastrowid


def get_location_id(conn, location):
    with conn:
        c = conn.cursor()
        c.execute("SELECT loc_id FROM locations WHERE loc = ?;", (location,))
        return c.fetchall()[0][0]


def get_type_id(conn, name):
    with conn:
        c = conn.cursor()
        c.execute("select type_id from types where type = ?;", (name,))
        return c.fetchall()[0][0]


def get_type_id_by_plural(conn, name):
    with conn:
        c = conn.cursor()
        c.execute("select type_id from types where type_plural = ?;", (name,))
        return c.fetchall()[0][0]


def check_type(conn, type_name):
    with conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM types WHERE type = ?;", (type_name,))
        types = c.fetchall()
        return True if types else False


def insert_item(conn, name, quantity, type_name, type_plural, location):
    try:
        loc_id = insert_location(conn, location, "")
    except sqlite3.IntegrityError:
        loc_id = get_location_id(conn, location)
    try:
        type_id = insert_type(conn, type_name, type_plural)
    except sqlite3.IntegrityError:
        type_id = get_type_id(conn, type_name)
    _insert_item(conn, name, quantity, type_id, loc_id, True)


def skip_item(conn, item_id):
    return set_item_status(conn, item_id, get=False)


def buy_item(conn, item_id):
    return set_item_status(conn, item_id, get=True)


def set_item_status(conn, item_id, get=True):
    with conn:
        c = conn.cursor()
        c.execute("UPDATE items SET buy = ? WHERE item_id = ?;", (get, item_id,))
        return c.lastrowid


def update_item_quantity(conn, item_id, quantity):
    with conn:
        c = conn.cursor()
        c.execute("UPDATE items SET quantity = ? WHERE item_id = ?;", (quantity, item_id))
        return c.lastrowid


def _insert_item(conn, name, quantity, type_id, loc_id, get=True):
    with conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO items(name, quantity, type_id, loc_id, buy) VALUES(?, ?, ?, ?, ?)",
            (name, quantity, type_id, loc_id, get),
        )
        return c.lastrowid


def insert_item_with_type(conn, name, quantity, type_id, location):
    try:
        loc_id = insert_location(conn, location, "")
    except sqlite3.IntegrityError:
        loc_id = get_location_id(conn, location)
    _insert_item(conn, name, quantity, type_id, loc_id, get=True)


def delete_type(conn, type_name):
    with conn:
        c = conn.cursor()
        c.execute("DELETE FROM types WHERE type = ?", (type_name,))
        return c.lastrowid


def get_locations(conn):
    with conn:
        c = conn.cursor()
        c.execute("SELECT loc from locations ORDER BY priority;")
        return [l[0] for l in c.fetchall()]


def get_types(conn):
    with conn:
        c = conn.cursor()
        c.execute("SELECT type FROM types ORDER BY type;")
        return [t[0] for t in c.fetchall()]


def get_plural_types(conn):
    with conn:
        c = conn.cursor()
        c.execute("SELECT type_plural FROM types ORDER BY type;")
        return [t[0] for t in c.fetchall()]


def get_types_with_plurals(conn):
    with conn:
        c = conn.cursor()
        c.execute("SELECT type, type_plural FROM types;")
        return c.fetchall()


def list_items(conn):
    with conn:
        c = conn.cursor()
        c.execute("SELECT name FROM items;")
        return [i[0] for i in c.fetchall()]


def get_items(conn):
    sql = """
        SELECT
            item_id,
            quantity,
            CASE WHEN quantity == 1 THEN type
            ELSE type_plural
            END AS type,
            name,
            loc,
            buy,
            priority
        FROM items
        INNER JOIN locations
            ON items.loc_id == locations.loc_id
        INNER JOIN types
            ON items.type_id == types.type_id
        ORDER BY priority, quantity DESC, name
    """
    with conn:
        c = conn.cursor()
        c.execute(sql)
        return c.fetchall()


def get_todays(conn):
    sql = """
        SELECT
            item_id,
            quantity,
            CASE WHEN quantity == 1 THEN type
            ELSE type_plural
            END AS type,
            name,
            loc,
            buy,
            priority
        FROM items
        INNER JOIN locations
            ON items.loc_id == locations.loc_id
        INNER JOIN types
            ON items.type_id == types.type_id
        WHERE items.buy == 1
        ORDER BY priority, quantity DESC, name
    """
    with conn:
        c = conn.cursor()
        c.execute(sql)
        return c.fetchall()
