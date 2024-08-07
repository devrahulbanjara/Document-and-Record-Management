import random
import csv

# Expanded lists of common Nepali surnames and male names
surnames = [
    "Thapa", "Gurung", "Rai", "Tamang", "Magar", "Khatri", "Shrestha",
    "Bajracharya", "Pradhan", "Adhikari", "Sapkota", "Pokhrel", "Bista",
    "Neupane", "Dahal", "Bhattarai", "Pandey", "Sharma", "Karki", "Devkota",
    "Basnet", "Poudel", "Acharya", "Bhandari", "Panta", "Khatiwada",
    "Chhetri", "Aryal", "Ghimire", "Regmi", "Dhamala", "Bista", "Rijal",
    "Bhusal", "Subedi", "Gyawali", "Poudyal", "KC", "Timilsina"
]

male_names = [
    "Ram", "Shyam", "Hari", "Krishna", "Bishnu", "Maheshwar", "Shiva",
    "Ganesh", "Naren", "Suren", "Dipesh", "Pradeep", "Rabin", "Suresh",
    "Milan", "Kiran", "Arjun", "Bimal", "Prabin", "Santosh", "Bijay",
    "Dinesh", "Ramesh", "Deepak", "Jitendra", "Narendra", "Prashant",
    "Sandeep", "Niraj", "Suman", "Manish", "Saroj", "Bikash", "Roshan",
    "Pawan", "Bibek", "Sunil", "Anil", "Ashok", "Rajan"
]

# Ensure we have enough unique combinations
assert len(surnames) * len(male_names) >= 400, "Insufficient unique combinations available"

# Generate 400 unique names
generated_names = set()
while len(generated_names) < 400:
    first_name = random.choice(male_names)
    last_name = random.choice(surnames)
    full_name = f"{first_name} {last_name}"
    generated_names.add(full_name)

# Save to CSV
output_file = "male_names.csv"
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name"])
    for name in generated_names:
        writer.writerow([name])

print(f"Generated 400 names and saved to {output_file}")
