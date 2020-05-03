import sys
import sqlite3
import argparse
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from .utils import get_locations, delete_location


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="data/grocery.db")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)

    locations = get_locations(conn)
    completer = WordCompleter(locations)
    loc = prompt("Enter a location to delete: ", completer=completer)
    try:
        loc_id = delete_location(conn, loc)
        print(f"Deleted location {loc}")
    except sqlite3.IntegrityError as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
