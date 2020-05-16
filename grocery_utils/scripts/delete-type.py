import sys
import sqlite3
import argparse
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from ..utils import get_types, delete_type


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="data/grocery.db")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)

    locations = get_types(conn)
    completer = WordCompleter(locations)
    t = prompt("Enter a type to delete: ", completer=completer)
    try:
        type_id = delete_type(conn, t)
        print(f"Deleted type {t}")
    except sqlite3.IntegrityError as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
