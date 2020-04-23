import sys
import csv
from cs50 import SQL

if len(sys.argv) != 2:
    sys.exit('Usage: $ python import.py csv-file')

import_file = sys.argv[1]

# Connect to the database
database = SQL('sqlite:///students.db')

# Since we may assume the file exists, the try is unnecessary
# But it feels safe to just implement it.
try:
    with open(import_file) as file:
        reader = csv.DictReader(file, delimiter=',')

        for row in reader:
            entry = []

            name = row['name'].split(' ')
            first_name = name[0]
            middle_name = None
            last_name = name[len(name) - 1]

            if len(name) != 2:
                middle_name = name[1]

            entry.append(first_name)
            entry.append(middle_name)
            entry.append(last_name)
            entry.append(row['house'])
            entry.append(row['birth'])

            database.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)", entry[:5])

except FileNotFoundError:
    sys.exit('Could not find specified CSV')
