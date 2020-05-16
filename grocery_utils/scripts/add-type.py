import sys
import sqlite3
import argparse
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from ..utils import get_types, insert_type


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="data/grocery.db")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    types = get_types(conn)
    completer = WordCompleter(types)
    new_type = prompt("Enter a new type: ", completer=completer)
    new_plural = prompt("Enter the plural version of this type: ", completer=WordCompleter([new_type + "s"]))
    try:
        type_id = insert_type(conn, new_type, new_plural)
        print(f"Inserted new type {new_type} ({new_plural}) with id {type_id}.")
    except sqlite3.IntegrityError:
        print(f"Type {new_type} already exists, northing to do.")
        sys.exit(1)


if __name__ == "__main__":
    main()
