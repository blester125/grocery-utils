set -e

tail -n +2 data/locations.csv > data/locations-without-header.csv
tail -n +2 data/types.csv > data/types-without-header.csv
tail -n +2 data/items.csv > data/items-without-header.csv

sqlite3 data/grocery.db < grocery_utils/scripts/setup.sql

rm data/items-without-header.csv
rm data/types-without-header.csv
rm data/locations-without-header.csv
