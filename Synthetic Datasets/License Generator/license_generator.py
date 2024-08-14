import random
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
import textwrap

# Load data from CSV files
male_names_df = pd.read_csv("/mnt/c/Users/drenergydrink/Desktop/Document-and-Record-Management/License_generator_2/Male Names/male_names.csv", encoding='utf-8')
female_names_df = pd.read_csv("/mnt/c/Users/drenergydrink/Desktop/Document-and-Record-Management/License_generator_2/Female Names/female_names.csv", encoding='utf-8')
dob_df = pd.read_csv("/mnt/c/Users/drenergydrink/Desktop/Document-and-Record-Management/License_generator_2/DOB/DOB.csv", encoding='utf-8')
phone_df = pd.read_csv("/mnt/c/Users/drenergydrink/Desktop/Document-and-Record-Management/License_generator_2/Contact Number/phone_numbers.csv", encoding='utf-8')
citizenship_df = pd.read_csv("/mnt/c/Users/drenergydrink/Desktop/Document-and-Record-Management/License_generator_2/Citizenship Number/Citizenship_number.csv", encoding='utf-8')
license_df = pd.read_csv("/mnt/c/Users/drenergydrink/Desktop/Document-and-Record-Management/License_generator_2/License_Number/license_numbers.csv", encoding='utf-8')
father_names_df = pd.read_csv("/mnt/c/Users/drenergydrink/Desktop/Document-and-Record-Management/License_generator_2/Male Names/male_names.csv", encoding='utf-8')

# Convert columns to lists
male_names_list = male_names_df['Name'].tolist()
female_names_list = female_names_df['Name'].tolist()
dob_list = dob_df['Date of Birth'].tolist()
phone_list = phone_df['Phone Number'].tolist()
citizenship_list = citizenship_df['Citizenship Number'].tolist()
license_list = license_df['License Number'].tolist()
father_names_list = father_names_df['Name'].tolist()

# Function to generate random name (male or female)
def generate_name():
    return random.choice(male_names_list + female_names_list)

# Function to generate random license number
def generate_license_number():
    return random.choice(license_list)

# Function to generate random date of birth
def generate_dob():
    return random.choice(dob_list)

# Function to generate random citizenship number
def generate_citizenship_number():
    return random.choice(citizenship_list)

# Function to generate random phone number
def generate_phone_number():
    return random.choice(phone_list)

# Create the DataFrame
data = {
    "License_Number": [generate_license_number() for _ in range(400)],
    "Name": [generate_name() for _ in range(400)],
    "Date_of_Birth": [generate_dob() for _ in range(400)],
    "Father_Name": [random.choice(father_names_list) for _ in range(400)],
    "Citizenship_Number": [generate_citizenship_number() for _ in range(400)],
    "Phone_Number": [generate_phone_number() for _ in range(400)],
}

df = pd.DataFrame(data)
df.to_csv("license_data.csv", index=False)

# Load your template image
template_path = "template.jpg"
template_image = Image.open(template_path)

# Define font and positions for each field (using Noto Sans)
font_size = 25
font_path = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"  # Ensure this path is correct
font = ImageFont.truetype(font_path, font_size)

positions = {
    "Name": (479, 192),
    "Date_of_Birth": (488, 358),
    "Father_Name": (523, 402),
    "Citizenship_Number": (582, 445),
    "Phone_Number": (541, 533),
    "License_Number": (165, 150),
    "Kathmandu_Metropolitan": (503, 232)
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
        if field == "Kathmandu_Metropolitan":
            draw.text(position, "Kathmandu Metro", font=font, fill="black")
        else:
            draw.text(position, str(row[field]), font=font, fill="black")
    
    output_path = f"{output_dir}/license_{i}.png"
    image.save(output_path)

print("Finished generating images.")
