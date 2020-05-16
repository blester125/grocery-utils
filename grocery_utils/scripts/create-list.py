import os
import sqlite3
import argparse
from typing import Dict, List
from itertools import zip_longest
import pandas as pd
from tabulate import tabulate
from ..utils import get_items


def reflow(grouped: Dict[str, List[str]], count: int = 100) -> List[List[str]]:
    columns = []
    column = []
    for loc, group in grouped.items():
        if len(column) + 1 + len(group) > count:
            columns.append(column)
            column = []
        column.append(f"{loc}:")
        column.extend(group)
        column.append("")
    if column:
        columns.append(column)

    max_per_column = [len(max(col, key=lambda x: len(x))) for col in columns]
    lines = []
    for col in zip_longest(*columns, fillvalue=""):
        line = []
        for c, width in zip(col, max_per_column):
            line.append(c.ljust(width))
        lines.append("   ".join(line))
    return lines


def main():
    parser = argparse.ArgumentParser(description="Create a Grocery list")
    parser.add_argument("--db", default="data/grocery.db", type=os.path.realpath)
    parser.add_argument("--lines", default=100, type=int)
    parser.add_argument("--show_all", "--show-all", action="store_true")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)

    get = get_items if args.show_all else get_todays
    items = pd.DataFrame(get(conn), columns=["item_id", "quantity", "type", "name", "loc", "priority"])

    groups = items.groupby(["priority", "loc"], sort=True)

    grouped = {}
    for (prio, loc), items in groups:
        items = items[["quantity", "type", "name"]]
        table = tabulate(items, showindex=False, tablefmt='plain')
        grouped[loc] = table.split("\n")

    for l in reflow(grouped, args.lines):
        print(l)


if __name__ == "__main__":
    main()
