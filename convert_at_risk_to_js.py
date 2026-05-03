import csv
import json

input_file = 'at_risk_schools.csv'
output_file = 'at_risk_data.js'

schools = []

with open(input_file, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            school = {
                'name': row['name'],
                'type': row['type'],
                'lat': float(row['lat']),
                'lng': float(row['lon']),
                'conflict_date': row['nearby_conflict_date'].split(' ')[0]
            }
            schools.append(school)
        except (ValueError, KeyError):
            continue

with open(output_file, mode='w', encoding='utf-8') as f:
    f.write("const atRiskSchools = ")
    json.dump(schools, f, indent=2)
    f.write(";")

print(f"Converted {len(schools)} at-risk schools to {output_file}")
