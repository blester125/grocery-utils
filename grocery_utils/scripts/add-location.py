import sys
import sqlite3
import argparse
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from ..utils import get_locations, insert_location


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="data/grocery.db")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)

    locations = get_locations(conn)
    completer = WordCompleter(locations)
    new_loc = prompt("Enter a new location: ", completer=completer)
    new_priority = prompt("Enter the priority of the this location (Enter for lowest priority): ")
    try:
        new_priority, loc_id = insert_location(conn, new_loc, new_priority)
        print(f"Inserted new location {new_loc} (with prio: {new_priority}) with id {loc_id}")
    except sqlite3.IntegrityError:
        print(f"Location {new_loc} already exists, nothing to do.")
        sys.exit(1)


if __name__ == "__main__":
    main()
