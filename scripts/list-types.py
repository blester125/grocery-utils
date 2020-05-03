import sys
import sqlite3
import argparse
from .utils import get_types_with_plurals


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="data/grocery.db")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)

    types = get_types_with_plurals(conn)

    for t, tp in types:
        print(f"{t} ({tp})")


if __name__ == "__main__":
    main()
