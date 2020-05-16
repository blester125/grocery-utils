import os
import flask
import sqlite3
import pandas as pd
from tabulate import tabulate
from flask import Flask, current_app, g, jsonify, request
from grocery_utils.utils import (
    get_items,
    buy_item,
    skip_item,
    get_locations,
    get_todays,
    reflow,
    get_types,
    get_type_id,
    get_location_id,
    _insert_item,
    insert_type,
    insert_location,
    get_plural_types,
)

app = Flask(__name__)
app.config["DATABASE"] = os.getenv("DATABASE")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"],)
    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


@app.route("/")
def index():
    return current_app.send_static_file("index.html")


@app.route("/generate")
def generate_list():
    return current_app.send_static_file("list.html")


@app.route("/add-item")
def _add_item_page():
    return current_app.send_static_file("item.html")


@app.route("/add-location")
def _add_location_page():
    return current_app.send_static_file("location.html")


@app.route("/add-type")
def _add_type_page():
    return current_app.send_static_file("type.html")


@app.route("/list")
def list():
    lines = int(request.args.get("lines", 100))
    show_all = True if int(request.args.get("show_all", 1)) == 1 else False

    get = get_items if show_all else get_todays
    items = pd.DataFrame(get(get_db()), columns=["item_id", "quantity", "type", "name", "loc", "buy", "priority"])

    groups = items.groupby(["priority", "loc"], sort=True)

    grouped = {}
    for (prio, loc), items in groups:
        items = items[["quantity", "type", "name"]]
        table = tabulate(items, showindex=False, tablefmt="plain")
        grouped[loc] = table.split("\n")

    return "\n".join(reflow(grouped, lines))


@app.route("/items")
def _get_items():
    resp = []
    for type_id, quant, _type, name, location, buy, _ in get_items(get_db()):
        resp.append({"id": type_id, "quantity": quant, "type": _type, "name": name, "location": location, "buy": buy})
    return jsonify(resp)


@app.route("/item/<item_id>/buy", methods=["POST"])
def _buy_item(item_id):
    buy = bool(request.json["buy"])
    try:
        if buy:
            buy_item(get_db(), item_id)
        else:
            skip_item(get_db(), item_id)
        return jsonify({"Stats": "Success"})
    except:
        return "Failed", 500


@app.route("/item", methods=["POST"])
def _add_item():
    name = request.json["name"]
    quant = request.json["quantity"]
    type_name = request.json["type"]
    loc = request.json["location"]
    type_id = get_type_id(get_db(), type_name)
    loc_id = get_location_id(get_db(), loc)
    try:
        item_id = _insert_item(get_db(), name, quant, type_id, loc_id)
        return jsonify({"Status": "Success", "id": item_id})
    except:
        return "Failure", 500


@app.route("/type", methods=["POST"])
def _add_type():
    type_name = request.json["type"]
    plural = request.json["plural"]
    try:
        type_id = insert_type(get_db(), type_name, plural)
        return jsonify({"Status": "Success", "id": type_id})
    except:
        return "Failure", 500


@app.route("/location", methods=["POST"])
def _add_location():
    print(request.json)
    loc = request.json["location"]
    try:
        loc_id = insert_location(get_db(), loc, "")
        return jsonify({"Status": "Success", "id": loc_id})
    except:
        return "Failure", 500


@app.route("/locations")
def _get_locations():
    return jsonify(get_locations(get_db()))


@app.route("/types")
def _get_types():
    return jsonify(get_types(get_db()))


@app.route("/types-plural")
def _get_plural_types():
    return jsonify(get_plural_types(get_db()))
