import csv

# 1. Define the file names
# This is our big source file
input_file = 'GEDEvent_v25_1.csv'
# This is the new, smaller file we want to create
output_file = 'mali_conflicts.csv'

print(f"Reading {input_file} and filtering for Mali...")

# 2. Open the files
# 'with open' is a safe way to open files because it closes them automatically when finished.
# mode='r' means Read; mode='w' means Write.
with open(input_file, mode='r', encoding='utf-8', newline='') as infile:
    with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        
        # 3. Create a 'Reader' and a 'Writer'
        # DictReader treats each row like a dictionary so we can use column names like 'country'
        reader = csv.DictReader(infile)
        # DictWriter needs to know the 'fieldnames' (the header) to know how to write the columns
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        
        # 4. Write the header (the first row with column names) to the new file
        writer.writeheader()
        
        # 5. Loop through every row in the big file
        counter = 0
        for row in reader:
            # 6. Check if the 'country' column says 'Mali'
            if row['country'] == 'Mali':
                # 7. Write that specific row to our new file
                writer.writerow(row)
                counter += 1

print(f"Success! Found {counter} rows for Mali.")
print(f"The filtered data has been saved to '{output_file}'.")
