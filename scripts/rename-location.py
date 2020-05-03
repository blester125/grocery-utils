import sys
import sqlite3
import argparse
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from .utils import get_locations, update_location_name


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="data/grocery.db")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)

    locations = get_locations(conn)
    completer = WordCompleter(locations)
    old_loc = prompt("Enter a location to rename: ", completer=completer)
    new_loc = prompt("Enter the new name for this location: ")
    try:
        loc_id = update_location_name(conn, old_loc, new_loc)
        print(f"Updated location {old_loc} to be called {new_loc}")
    except sqlite3.IntegrityError as e:
        print(f"Location {new_loc} already exists, can't rename {old_loc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
