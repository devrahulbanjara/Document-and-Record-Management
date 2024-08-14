import random
import csv

# Expanded lists of common Nepali surnames and female names
surnames = [
    "Thapa", "Gurung", "Rai", "Tamang", "Magar", "Khatri", "Shrestha",
    "Bajracharya", "Pradhan", "Adhikari", "Sapkota", "Pokhrel", "Bista",
    "Neupane", "Dahal", "Bhattarai", "Pandey", "Sharma", "Karki", "Devkota",
    "Basnet", "Poudel", "Acharya", "Bhandari", "Panta", "Khatiwada",
    "Chhetri", "Aryal", "Ghimire", "Regmi", "Dhamala", "Bista", "Rijal",
    "Bhusal", "Subedi", "Gyawali", "Poudyal", "KC", "Timilsina"
]

female_names = [
    "Sita", "Gita", "Rita", "Laxmi", "Radha", "Sarita", "Sunita", "Anita",
    "Manisha", "Sushila", "Bina", "Bimala", "Kavita", "Ranju", "Roshani",
    "Maya", "Prabha", "Nirmala", "Kalpana", "Mina", "Gauri", "Lila",
    "Sabina", "Namrata", "Pooja", "Sneha", "Asha", "Sanjita", "Santoshi",
    "Nisha", "Rupa", "Dipika", "Komal", "Pratima", "Shova", "Susmita",
    "Asmita", "Prativa", "Kusum", "Sumitra", "Rekha"
]

# Ensure we have enough unique combinations
assert len(surnames) * len(female_names) >= 400, "Insufficient unique combinations available"

# Generate 400 unique names
generated_names = set()
while len(generated_names) < 400:
    first_name = random.choice(female_names)
    last_name = random.choice(surnames)
    full_name = f"{first_name} {last_name}"
    generated_names.add(full_name)

# Save to CSV
output_file = "female_names.csv"
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name"])
    for name in generated_names:
        writer.writerow([name])

print(f"Generated 400 female names and saved to {output_file}")
