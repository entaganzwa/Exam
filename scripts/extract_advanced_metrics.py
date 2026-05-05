import csv
import json
from collections import Counter, defaultdict

INPUT_CSV = 'data/processed/GEDEvent_v25_1_cleaned.csv'
OUTPUT_JSON = 'js/advanced_dashboard_data.json'

def process():
    # 1. Top 10 countries
    country_counts = Counter()
    
    # 2. Events per region per year
    region_year_counts = defaultdict(lambda: defaultdict(int))
    
    # 3. Events by category
    CATEGORY_MAP = {
        '1': 'State-based',
        '2': 'Non-state',
        '3': 'One-sided'
    }
    category_counts = Counter()
    
    # 4. Severity
    severity_counts = Counter()
    
    # 5. Infrastructure damage
    infra_damage_counts = Counter()

    print(f"Reading global data from {INPUT_CSV}...")
    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Country
            country_counts[row['country']] += 1
            
            # Region + Year
            region = row['region']
            year = row['year']
            region_year_counts[region][year] += 1
            
            # Category
            cat_code = row['type_of_violence']
            cat_name = CATEGORY_MAP.get(cat_code, f"Type {cat_code}")
            category_counts[cat_name] += 1
            
            # Severity
            try:
                fatalities = int(row['best'])
                if fatalities == 0: sev = "Low (0)"
                elif fatalities < 10: sev = "Medium (1-9)"
                elif fatalities < 50: sev = "High (10-49)"
                else: sev = "Critical (50+)"
            except:
                sev = "Unknown"
            severity_counts[sev] += 1
            
            # Infrastructure (Basic keyword search)
            desc = (row['source_headline'] + " " + row['where_description']).lower()
            if any(k in desc for k in ['school', 'école', 'college', 'lycée']):
                infra_damage_counts['Education'] += 1
            if any(k in desc for k in ['hospital', 'health', 'santé', 'clinique']):
                infra_damage_counts['Health'] += 1
            if any(k in desc for k in ['bridge', 'road', 'pont', 'route']):
                infra_damage_counts['Transport'] += 1
            if any(k in desc for k in ['market', 'marché', 'shop', 'boutique']):
                infra_damage_counts['Commerce'] += 1

    # Format for Chart.js
    data = {
        "countries": dict(country_counts.most_common(10)),
        "regions": {reg: dict(years) for reg, years in region_year_counts.items()},
        "categories": dict(category_counts),
        "severity": dict(severity_counts),
        "infrastructure": dict(infra_damage_counts)
    }

    print(f"Writing metrics to {OUTPUT_JSON}...")
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print("Done!")

if __name__ == '__main__':
    process()
