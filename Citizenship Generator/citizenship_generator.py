from PIL import Image, ImageDraw, ImageFont
import os
import pandas as pd
import random

# Paths
font_path = '/mnt/c/Users/drenergydrink/Desktop/Document-and-Record-Management/Citizenship Generator/preeti.TTF'
template_path = '/mnt/c/Users/drenergydrink/Desktop/Document-and-Record-Management/Citizenship Generator/template2.jpg'
output_dir = '/mnt/c/Users/drenergydrink/Desktop/Document-and-Record-Management/Citizenship Generator/GeneratedImages/'

# Load CSVs
citizenship_numbers = pd.read_csv('/mnt/c/Users/drenergydrink/Desktop/Document-and-Record-Management/Citizenship Generator/Citizenship Number/citizenship_numbers.csv')
names = pd.read_csv('/mnt/c/Users/drenergydrink/Desktop/Document-and-Record-Management/Citizenship Generator/Names/names.csv')
districts = pd.read_csv('/mnt/c/Users/drenergydrink/Desktop/Document-and-Record-Management/Citizenship Generator/District/nepali_districts.csv')
municipalities = pd.read_csv('/mnt/c/Users/drenergydrink/Desktop/Document-and-Record-Management/Citizenship Generator/Nagarpalika/nepali_municipalities.csv')
dates = pd.read_csv('/mnt/c/Users/drenergydrink/Desktop/Document-and-Record-Management/Citizenship Generator/Date generator/nepali_dates.csv')

# Create output directory if it does not exist
os.makedirs(output_dir, exist_ok=True)

# Load font
try:
    font = ImageFont.truetype(font_path, 20)
except OSError as e:
    print(f"Error loading font: {e}")
    font = ImageFont.load_default()

# Generate images
for i in range(800):
    img = Image.open(template_path)
    draw = ImageDraw.Draw(img)

    # Add random text to the image
    citizenship_number = random.choice(citizenship_numbers['Citizenship Number'])
    name = random.choice(names['Names'])
    gender = random.choice(['महिला', 'पुरुष'])
    district = random.choice(districts['District'])
    municipality = random.choice(municipalities['Municipality'])
    random_digits = ''.join(random.choices(['१', '२', '३', '४', '५', '६', '७', '८', '९', '०'], k=32))
    year, month, day = random.choice(dates['Year']), random.choice(dates['Month']), random.choice(dates['Date'])
    additional_name = random.choice(names['Names'])

    draw.text((100, 183), citizenship_number, font=font, fill='black')
    draw.text((284, 211), name, font=font, fill='black')
    draw.text((716, 209), gender, font=font, fill='black')
    draw.text((448, 240), district, font=font, fill='black')
    draw.text((448, 272), municipality, font=font, fill='black')
    draw.text((727, 268), random_digits, font=font, fill='black')
    draw.text((424, 357), year, font=font, fill='black')
    draw.text((533, 355), month, font=font, fill='black')
    draw.text((602, 355), day, font=font, fill='black')
    draw.text((347, 384), additional_name, font=font, fill='black')

    # Save the image
    img.save(os.path.join(output_dir, f'citizenship_{i+1}.jpg'))

print("800 images generated successfully!")
