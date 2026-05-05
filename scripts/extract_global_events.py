import csv
import json
import random

# Input: The large dataset
# Output: A small JavaScript file for the web map
INPUT_FILE = 'data/processed/GEDEvent_v25_1_cleaned.csv'
OUTPUT_FILE = 'js/global_conflict_data.js'
MAX_EVENTS = 3000  # Limiting to 3000 events for fast loading in browsers

def extract():
    events = []
    
    print(f"Reading {INPUT_FILE}...")
    with open(INPUT_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # We only need a few columns to keep the file small
            event = {
                'lat': float(row['latitude']) if row['latitude'] else 0,
                'lng': float(row['longitude']) if row['longitude'] else 0,
                'date': row['date_start'].split(' ')[0], # Just the date part
                'cause': row['dyad_name'],
                'deaths': row['best'],
                'civ_deaths': row['deaths_civilians'],
                'country': row['country']
            }
            events.append(event)
    
    # If we have too many events, take a random sample
    if len(events) > MAX_EVENTS:
        print(f"Sampling {MAX_EVENTS} events from {len(events)} total...")
        events = random.sample(events, MAX_EVENTS)
    
    # Save as a JavaScript variable
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("const globalConflictData = " + json.dumps(events) + ";")
    
    print(f"Success! Created {OUTPUT_FILE}")

if __name__ == "__main__":
    extract()
