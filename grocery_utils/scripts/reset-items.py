import sqlite3
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="data/grocery.db")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)

    with conn:
        c = conn.cursor()
        c.execute("UPDATE items SET buy = 0;")


if __name__ == "__main__":
    main()
