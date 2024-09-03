import random
import csv

def generate_license_number():
    """Generate a random license number in the format xx-xx-xxxxxxxx"""
    part1 = f"{random.randint(0, 99):02d}"  # Two-digit part
    part2 = f"{random.randint(0, 99):02d}"  # Two-digit part
    part3 = f"{random.randint(10000000, 99999999):08d}"  # Eight-digit part
    return f"{part1}-{part2}-{part3}"

# Generate 400 unique license numbers
generated_license_numbers = set()
while len(generated_license_numbers) < 400:
    license_number = generate_license_number()
    generated_license_numbers.add(license_number)

# Save to CSV
output_file = "license_numbers.csv"
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["License Number"])
    for license_number in generated_license_numbers:
        writer.writerow([license_number])

print(f"Generated 400 unique license numbers and saved to {output_file}")
