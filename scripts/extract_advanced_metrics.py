import csv
import json
from collections import Counter, defaultdict

INPUT_CSV = 'data/processed/GEDEvent_v25_1_cleaned.csv'
OUTPUT_JSON = 'js/advanced_dashboard_data.json'

# Mappings for regions to match user request
REGION_MAPPING = {
    'Africa': 'Sub-Saharan Africa',
    'Middle East': 'Middle East',
    'Asia': 'South-East Asia' # We'll treat Asia as South-East Asia for this specific request
}

def process():
    country_counts = Counter()
    region_year_counts = defaultdict(lambda: defaultdict(int))
    
    CATEGORY_MAP = {
        '1': 'State-based',
        '2': 'Non-state',
        '3': 'One-sided'
    }
    category_counts = Counter()
    severity_counts = Counter()

    print(f"Reading global data from {INPUT_CSV}...")
    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 1. Country
            country_counts[row['country']] += 1
            
            # 2. Region + Year (Filtered for specific regions)
            raw_region = row['region']
            if raw_region in REGION_MAPPING:
                mapped_region = REGION_MAPPING[raw_region]
                year = row['year']
                region_year_counts[mapped_region][year] += 1
            
            # 3. Category
            cat_code = row['type_of_violence']
            cat_name = CATEGORY_MAP.get(cat_code, f"Type {cat_code}")
            category_counts[cat_name] += 1
            
            # 4. Severity (Based on 'best' fatalities as proxy for severity)
            try:
                fatalities = int(row['best'])
                if fatalities == 0: sev = "Low (0)"
                elif fatalities < 10: sev = "Medium (1-9)"
                elif fatalities < 50: sev = "High (10-49)"
                else: sev = "Critical (50+)"
            except:
                sev = "Unknown"
            severity_counts[sev] += 1

    # Format for Chart.js
    data = {
        "countries": dict(country_counts.most_common(10)),
        "regions": {reg: dict(years) for reg, years in region_year_counts.items()},
        "categories": dict(category_counts),
        "severity": dict(severity_counts)
    }

    print(f"Writing metrics to {OUTPUT_JSON}...")
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print("Done!")

if __name__ == '__main__':
    process()
