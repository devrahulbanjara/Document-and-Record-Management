import random
import csv

# Nepali digits mapping
nepali_digits = str.maketrans("0123456789", "०१२३४५६७८९")

def generate_format_1():
    return ''.join(random.choices('0123456789', k=8))

def generate_format_2():
    return f"{''.join(random.choices('0123456789', k=2))}-{''.join(random.choices('0123456789', k=2))}-{''.join(random.choices('0123456789', k=2))}-{''.join(random.choices('0123456789', k=5))}"

def generate_format_3():
    return f"{''.join(random.choices('0123456789', k=4))}-{''.join(random.choices('0123456789', k=5))}"

def convert_to_nepali(number_str):
    return number_str.translate(nepali_digits)

# Generate 800 citizenship numbers
citizenship_numbers = []
for _ in range(800):
    format_type = random.choice([generate_format_1, generate_format_2, generate_format_3])
    formatted_number = format_type()
    nepali_number = convert_to_nepali(formatted_number)
    citizenship_numbers.append(nepali_number)

# Write to CSV
with open('citizenship_numbers.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Citizenship Number'])
    writer.writerows([[number] for number in citizenship_numbers])

print('Generated 800 citizenship numbers and saved to citizenship_numbers.csv')
