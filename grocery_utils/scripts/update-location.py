import sys
import sqlite3
import argparse
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from ..utils import get_locations, update_location_priority


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="data/grocery.db")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)

    locations = get_locations(conn)
    completer = WordCompleter(locations)
    loc = prompt("Enter a location to change the priority of: ", completer=completer)
    prio = prompt("Enter the new priority: ")
    try:
        old_prio, loc_id = update_location_priority(conn, loc, prio)
        print(f"Updated location {loc} priority from {old_prio} -> {new_prio}")
    except sqlite3.IntegrityError as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
