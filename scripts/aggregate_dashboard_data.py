import csv
import json
from collections import Counter, defaultdict

def aggregate_data(input_path, output_path):
    print(f"Reading {input_path}...")
    
    country_counter = Counter()
    year_counter = Counter()
    category_counter = Counter()
    fatality_counter = defaultdict(int) # Fatalities per year
    
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i % 100000 == 0 and i > 0:
                print(f"Processed {i} rows...")
            
            country = row.get('country', 'Unknown')
            year = row.get('year', 'Unknown')
            category = row.get('type_of_violence_label', 'Unknown')
            try:
                fatalities = int(row.get('best', 0))
            except (ValueError, TypeError):
                fatalities = 0
            
            country_counter[country] += 1
            year_counter[year] += 1
            category_counter[category] += 1
            fatality_counter[year] += fatalities

    # Top 10 countries by event count
    top_countries = dict(country_counter.most_common(10))
    
    # Events per year (sorted)
    years = sorted(year_counter.keys())
    events_per_year = {y: year_counter[y] for y in years}
    
    # Events by category
    categories = dict(category_counter)
    
    # Fatalities per year
    fatalities_per_year = {y: fatality_counter[y] for y in years}

    data = {
        "top_countries": top_countries,
        "events_per_year": events_per_year,
        "categories": categories,
        "fatalities_per_year": fatalities_per_year
    }

    print(f"Writing aggregated data to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    aggregate_data('data/processed/GEDEvent_v25_1_cleaned.csv', 'js/dashboard_data.json')
