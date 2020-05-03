import sys
import sqlite3
import argparse
from .utils import get_locations


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="data/grocery.db")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)

    locations = get_locations(conn)

    for location in locations:
        print(location)


if __name__ == "__main__":
    main()
