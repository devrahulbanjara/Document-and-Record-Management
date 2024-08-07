import random
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
import textwrap

# Read Nepali names from CSV with explicit encoding (replace 'utf-8' with the correct encoding)
nepali_names_df = pd.read_csv("nepali_names.csv", encoding='utf-16')

# Convert the 'Name' column to a list
nepali_names_list = nepali_names_df['Name'].tolist()

# Read Nepali addresses from CSV
nepali_addresses_df = pd.read_csv("nepal_addresses.csv", encoding='utf-8')
nepali_addresses_list = nepali_addresses_df['Address'].tolist()

# Function to generate license number
def generate_license_number():
    return f"01-06-{random.randint(10000000, 99999999)}"

# Function to generate date in mm/dd/yyyy format
def generate_date():
    month = f"{random.randint(1, 12):02d}"
    day = f"{random.randint(1, 28):02d}"
    year = random.randint(1980, 2000)
    return f"{month}/{day}/{year}"

# Function to generate citizenship number
def generate_citizenship_number():
    return f"27-01-78-{random.randint(10000, 99999)}"

# Function to generate random 10-digit phone number
def generate_phone_number():
    return f"9{random.randint(100000000, 999999999)}"

# Function to generate random license category (A, B, C)
def generate_license_category():
    return random.choice(['A', 'B', 'C'])

# Create the DataFrame
data = {
    "License_Number": [generate_license_number() for _ in range(100)],
    "Name": [random.choice(nepali_names_list) for _ in range(100)],
    "Blood_Group": [random.choice(['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']) for _ in range(100)],
    "Address": [random.choice(nepali_addresses_list) for _ in range(100)],
    "DOB": [generate_date() for _ in range(100)],
    "Father_Name": [random.choice(nepali_names_list) for _ in range(100)],
    "Citizenship_Number": [generate_citizenship_number() for _ in range(100)],
    "Phone_Number": [generate_phone_number() for _ in range(100)],
    "License_Category": [generate_license_category() for _ in range(100)],
}

df = pd.DataFrame(data)
df.to_csv("license_data.csv", index=False)

# Load your template image
template_path = "template.jpg"
template_image = Image.open(template_path)

# Define font and positions for each field (using Times New Roman)
font_size = 20
font = ImageFont.truetype("times.ttf", font_size)  # Adjust path if necessary

positions = {
    "License_Number": (119, 101),
    "Name": (353, 100),
    "Blood_Group": (98, 129),
    "Address": (383, 129),
    "DOB": (360, 217),
    "Father_Name": (389, 248),
    "Citizenship_Number": (430, 278),
    "Phone_Number": (395, 337),
    "License_Category": (680, 283)
}

output_dir = "output_images"
os.makedirs(output_dir, exist_ok=True)

# Function to wrap text if it exceeds a certain width
def draw_text_with_wrap(draw, text, position, font, max_width):
    lines = textwrap.wrap(text, width=max_width)
    y_text = position[1]
    for line in lines:
        draw.text((position[0], y_text), line, font=font, fill="black")
        line_height = font.getsize(line)[1] if hasattr(font, 'getsize') else draw.textbbox((0, 0), line, font=font)[3]
        y_text += line_height

# Create images with text
for i, row in df.iterrows():
    image = template_image.copy()
    draw = ImageDraw.Draw(image)
    
    for field, position in positions.items():
        if field == "Address":
            draw_text_with_wrap(draw, str(row[field]), position, font, max_width=20)
        else:
            draw.text(position, str(row[field]), font=font, fill="black")
    
    output_path = f"{output_dir}/license_{i}.png"
    image.save(output_path)

print("Finished generating images.")
