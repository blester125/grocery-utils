import sys
import sqlite3
import argparse
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from .utils import get_locations, get_types, list_items, insert_item, check_type, insert_item_with_type, get_type_id


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="data/grocery.db")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)

    items = list_items(conn)
    completer = WordCompleter(items)
    new_item = prompt("Enter a new item name: ", completer=completer)

    locations = get_locations(conn)
    completer = WordCompleter(locations)
    new_location = prompt(f"Enter the location of {new_item}: ", completer=completer)

    types = get_types(conn)
    completer = WordCompleter(types)
    new_type = prompt(f"Enter the type of {new_item}: ", completer=completer)
    if check_type(conn, new_type):
        quant = prompt(f"Enter the quantity of {new_item}: ")
        type_id = get_type_id(conn, new_type)
        insert_item_with_type(conn, new_item, quant, type_id, new_location)
    else:
        quant = prompt(f"Enter the quantity of {new_item}: ")
        new_pural = prompt(f"Enter the plural version of this type: ", completer=WordCompleter([new_type + "s"]))
        insert_item(conn, new_item, quant, new_type, new_pural, new_location)


if __name__ == "__main__":
    main()
