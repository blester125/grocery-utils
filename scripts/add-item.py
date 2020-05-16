import sys
import sqlite3
import argparse
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from .utils import get_locations, get_types, list_items, insert_item


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="data/grocery.db")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)

    items = list_items(conn)
    completer = WordCompleter(items)
    new_item = prompt("Enter a new item name: ", completer=completer)
    types = get_types(conn)
    completer = WordCompleter(types)
    new_type = prompt(f"Enter the type of {new_item}: ", completer=completer)
    new_pural = prompt(f"Enter the plural version of this type: ", completer=WordCompleter([new_type + "s"]))
    quant = prompt(f"Enter the quantity of {new_item}: ")
    locations = get_locations(conn)
    completer = WordCompleter(locations)
    new_location = prompt(f"Enter the location of {new_item}: ", completer=completer)

    insert_item(conn, new_item, quant, new_type, new_pural, new_location)


if __name__ == "__main__":
    main()
