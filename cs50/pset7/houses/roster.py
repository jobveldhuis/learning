import sys
from csv import DictReader
from cs50 import SQL

if len(sys.argv) != 2:
    sys.exit('Usage: $ python roster.py house')

house = sys.argv[1]

# Connect to the database
database = SQL('sqlite:///students.db')

# Since we may assume the file exists, the try is unnecessary
# But it feels safe to just implement it.
roster = database.execute('SELECT first, middle, last, birth FROM students WHERE house LIKE ? ORDER BY last, first', house)
for entry in roster:
    if entry['middle'] == None:
        print('{} {}, born {}'.format(entry['first'], entry['last'], entry['birth']))
    else:
        print('{} {} {}, born {}'.format(entry['first'], entry['middle'], entry['last'], entry['birth']))

