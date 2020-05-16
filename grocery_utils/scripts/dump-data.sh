set -e

DB=${1:-"data/grocery.db"}

sqlite3 $DB < grocery_utils/scripts/dump-types.sql
sqlite3 $DB < grocery_utils/scripts/dump-locations.sql
sqlite3 $DB < grocery_utils/scripts/dump-items.sql
