set -e

DB=${1:-"data/grocery.db"}

sqlite3 $DB < scripts/dump-types.sql
sqlite3 $DB < scripts/dump-locations.sql
sqlite3 $DB < scripts/dump-items.sql
