import csv
import json
import math

# File paths
CONFLICT_CSV = 'data/processed/mali_conflicts.csv'
SCHOOLS_GEOJSON = 'data/raw/hotosm_mli_education_facilities_points_geojson.geojson'
OUTPUT_NEAR = 'data/processed/schools_within_1km_conflict.geojson'
OUTPUT_FAR = 'data/processed/schools_far_from_conflict.geojson'

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points on the earth."""
    # Radius of Earth in kilometers
    R = 6371.0
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2)**2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def process_spatial_analysis():
    print(f"Reading conflict data from {CONFLICT_CSV}...")
    conflicts = []
    with open(CONFLICT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                lat = float(row['latitude'])
                lon = float(row['longitude'])
                conflicts.append((lat, lon))
            except (ValueError, KeyError):
                continue
    
    print(f"Loaded {len(conflicts)} conflict events.")

    print(f"Reading school data from {SCHOOLS_GEOJSON}...")
    with open(SCHOOLS_GEOJSON, 'r', encoding='utf-8') as f:
        schools_data = json.load(f)
    
    all_schools = schools_data.get('features', [])
    print(f"Loaded {len(all_schools)} school facilities.")

    schools_within_1km = []
    schools_outside_1km = []

    # Bounding box optimization: 1km is roughly 0.009 degrees in latitude
    # and roughly 0.009 / cos(lat) in longitude. For Mali (lat ~17), 
    # 0.01 degrees is a safe over-estimation for a 1km buffer.
    DEGREE_BUFFER = 0.01 

    print("Analyzing spatial relationships...")
    for i, school in enumerate(all_schools):
        if i % 1000 == 0 and i > 0:
            print(f"Processed {i} schools...")
            
        coords = school['geometry']['coordinates']
        s_lon, s_lat = coords[0], coords[1]
        
        is_near = False
        for c_lat, c_lon in conflicts:
            # Quick bounding box check
            if abs(s_lat - c_lat) < DEGREE_BUFFER and abs(s_lon - c_lon) < DEGREE_BUFFER:
                # Precise Haversine check
                if haversine(s_lat, s_lon, c_lat, c_lon) <= 1.0:
                    is_near = True
                    break
        
        if is_near:
            schools_within_1km.append(school)
        else:
            schools_outside_1km.append(school)

    print(f"Analysis complete.")
    print(f"Schools within 1km: {len(schools_within_1km)}")
    print(f"Schools further than 1km: {len(schools_outside_1km)}")

    # Prepare GeoJSON structures
    output_near_data = {
        "type": "FeatureCollection",
        "features": schools_within_1km
    }
    output_far_data = {
        "type": "FeatureCollection",
        "features": schools_outside_1km
    }

    print(f"Saving results to {OUTPUT_NEAR} and {OUTPUT_FAR}...")
    with open(OUTPUT_NEAR, 'w', encoding='utf-8') as f:
        json.dump(output_near_data, f, indent=2)
    
    with open(OUTPUT_FAR, 'w', encoding='utf-8') as f:
        json.dump(output_far_data, f, indent=2)

    print("Done.")

if __name__ == "__main__":
    process_spatial_analysis()
