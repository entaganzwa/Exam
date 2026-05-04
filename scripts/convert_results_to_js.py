import json

def geojson_to_js(input_path, variable_name, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    js_content = f"const {variable_name} = {json.dumps(data, indent=2)};"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(js_content)

if __name__ == "__main__":
    geojson_to_js('data/processed/schools_within_1km_conflict.geojson', 'schoolsNearConflict', 'js/schools_near.js')
    geojson_to_js('data/processed/schools_far_from_conflict.geojson', 'schoolsFarFromConflict', 'js/schools_far.js')
    print("Converted GeoJSON files to JS variables.")
