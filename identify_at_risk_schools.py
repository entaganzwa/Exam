import json
import csv
import math

# 1. Function to calculate distance between two points (Latitude/Longitude)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# 2. Load the schools from GeoJSON
geojson_file = 'hotosm_mli_education_facilities_points_geojson.geojson'
with open(geojson_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

schools = []
for feature in data['features']:
    props = feature['properties']
    geom = feature['geometry']
    if geom['type'] == 'Point':
        school = {
            'name': props.get('name') or 'Unnamed School',
            'type': props.get('amenity') or 'education',
            'lat': geom['coordinates'][1],
            'lon': geom['coordinates'][0]
        }
        schools.append(school)

# 3. Save ALL schools to a simple CSV first
with open('mali_schools_all.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'type', 'lat', 'lon'])
    writer.writeheader()
    writer.writerows(schools)

# 4. Load conflict data
conflicts = []
with open('mali_conflicts.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        conflicts.append({
            'lat': float(row['latitude']),
            'lon': float(row['longitude']),
            'date': row['date_start']
        })

# 5. Filter schools within 1km of any conflict
at_risk_schools = []
for school in schools:
    is_at_risk = False
    nearby_conflict_date = ""
    
    for conflict in conflicts:
        dist = haversine(school['lat'], school['lon'], conflict['lat'], conflict['lon'])
        if dist <= 1.0: # 1 km
            is_at_risk = True
            nearby_conflict_date = conflict['date']
            break # Found one, that's enough
    
    if is_at_risk:
        school_copy = school.copy()
        school_copy['nearby_conflict_date'] = nearby_conflict_date
        at_risk_schools.append(school_copy)

# 6. Save at-risk schools to a new CSV
with open('at_risk_schools.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'type', 'lat', 'lon', 'nearby_conflict_date'])
    writer.writeheader()
    writer.writerows(at_risk_schools)

print(f"Total schools found: {len(schools)}")
print(f"Schools within 1km of conflict: {len(at_risk_schools)}")
print("Files saved: 'mali_schools_all.csv' and 'at_risk_schools.csv'")
