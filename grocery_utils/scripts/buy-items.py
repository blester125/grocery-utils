import sqlite3
import argparse
from prompt_toolkit.shortcuts import yes_no_dialog
from ..utils import get_all, skip_item, buy_item


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="data/grocery.db")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)

    for item in get_all(conn):
        buy = yes_no_dialog(title="Are u gonna buy it? 🎶", text=f"{item[1]} {item[2]} of {item[3]}?").run()
        if buy:
            buy_item(conn, item[0])
        else:
            skip_item(conn, item[0])


if __name__ == "__main__":
    main()
