import random
import csv

def generate_license_number():
    """Generate a random license number in the format xx-xx-xx-xxxxx"""
    return f"{random.randint(0, 9)}{random.randint(0, 9)}-{random.randint(0, 9)}{random.randint(0, 9)}-{random.randint(0, 9)}{random.randint(0, 9)}-{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"

# Generate 400 unique license numbers
generated_licenses = set()
while len(generated_licenses) < 400:
    license_number = generate_license_number()
    generated_licenses.add(license_number)

# Save to CSV
output_file = "License_number.csv"
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["License Number"])
    for license_number in generated_licenses:
        writer.writerow([license_number])

print(f"Generated 400 license numbers and saved to {output_file}")
