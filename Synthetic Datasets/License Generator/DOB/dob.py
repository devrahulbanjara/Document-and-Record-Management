import random
import csv
from datetime import datetime, timedelta

def generate_random_date(start_year=1970, end_year=2006):
    """Generate a random date in the format dd-mm-yyyy"""
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date.strftime("%d-%m-%Y")

# Generate 400 unique dates of birth
generated_dobs = set()
while len(generated_dobs) < 400:
    dob = generate_random_date()
    generated_dobs.add(dob)

# Save to CSV
output_file = "generated_dob.csv"
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Date of Birth"])
    for dob in generated_dobs:
        writer.writerow([dob])

print(f"Generated 400 unique dates of birth from 1970 to 2006 and saved to {output_file}")
