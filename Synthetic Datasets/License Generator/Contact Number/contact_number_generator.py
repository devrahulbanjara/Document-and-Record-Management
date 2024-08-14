import random
import csv

def generate_phone_number():
    """Generate a random Nepal phone number in the format 97-XXXXXXX or 98-XXXXXXX"""
    prefix = random.choice(["97", "98"])  # Prefix can be 97 or 98
    phone_number = f"{random.randint(1000000, 9999999):07d}"  # 7-digit phone number
    return f"{prefix}{phone_number}"

# Generate 400 unique phone numbers
generated_phone_numbers = set()
while len(generated_phone_numbers) < 400:
    phone_number = generate_phone_number()
    generated_phone_numbers.add(phone_number)

# Save to CSV
output_file = "generated_phone_numbers.csv"
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Phone Number"])
    for phone_number in generated_phone_numbers:
        writer.writerow([phone_number])

print(f"Generated 400 unique Nepal phone numbers and saved to {output_file}")
