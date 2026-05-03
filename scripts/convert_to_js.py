import csv
import json

input_file = 'mali_conflicts.csv'
output_file = 'data.js'

conflicts = []

with open(input_file, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            # Extract basic info
            lat = float(row['latitude'])
            lng = float(row['longitude'])
            deaths = int(row['best'])
            
            # Create a simplified conflict object
            conflict = {
                'lat': lat,
                'lng': lng,
                'date': row['date_start'].split(' ')[0], # Keep just the date part
                'cause': row['conflict_name'],
                'damages': deaths,
                'location': row['where_description']
            }
            conflicts.append(conflict)
        except (ValueError, KeyError):
            continue

# Write to a JS file that defines a variable
with open(output_file, mode='w', encoding='utf-8') as f:
    f.write("const conflictData = ")
    json.dump(conflicts, f, indent=2)
    f.write(";")

print(f"Converted {len(conflicts)} events to {output_file}")
