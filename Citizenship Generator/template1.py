from PIL import Image, ImageDraw, ImageFont
import os
import pandas as pd
import random

# Paths
font_path = '/home/rahul/Desktop/Document-and-Record-Management/Citizenship Generator/mangal.ttf'
bold_font_path = '/home/rahul/Desktop/Document-and-Record-Management/Citizenship Generator/Mangal Bold.ttf'
template_path = '/home/rahul/Desktop/Document-and-Record-Management/Citizenship Generator/template.jpg'
output_dir = '/home/rahul/Desktop/Document-and-Record-Management/Citizenship Generator/Template1_Generated_image/'

# Load CSVs
citizenship_numbers = pd.read_csv('/home/rahul/Desktop/Document-and-Record-Management/Citizenship Generator/Citizenship Number/citizenship_numbers.csv')
names = pd.read_csv('/home/rahul/Desktop/Document-and-Record-Management/Citizenship Generator/Names/names.csv')
districts = pd.read_csv('/home/rahul/Desktop/Document-and-Record-Management/Citizenship Generator/District/nepali_districts.csv')
municipalities = pd.read_csv('/home/rahul/Desktop/Document-and-Record-Management/Citizenship Generator/Nagarpalika/nepali_municipalities.csv')
dates = pd.read_csv('/home/rahul/Desktop/Document-and-Record-Management/Citizenship Generator/Date generator/nepali_dates.csv')

# Create output directory if it does not exist
os.makedirs(output_dir, exist_ok=True)

# Load fonts
try:
    font = ImageFont.truetype(font_path, 18)  # Regular font
    bold_font = ImageFont.truetype(bold_font_path, 18)  # Bold font for citizenship number
except OSError as e:
    print(f"Error loading font: {e}")
    font = ImageFont.load_default()
    bold_font = font  # Fallback to default font if bold font fails

# Helper function to convert a number to Nepali digits
def convert_to_nepali_digits(number):
    nepali_digits = {
        '0': '०', '1': '१', '2': '२', '3': '३', '4': '४',
        '5': '५', '6': '६', '7': '७', '8': '८', '9': '९'
    }
    return ''.join(nepali_digits[digit] for digit in str(number))

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
    random_number = random.randint(1, 32)  # Generate a number between 1 and 32
    random_digits = convert_to_nepali_digits(random_number)
    year, month, day = random.choice(dates['Year']), random.choice(dates['Month']), random.choice(dates['Date'])
    father_name = random.choice(names['Names'])

    draw.text((173, 211), citizenship_number, font=bold_font, fill='black')  # Bold font for citizenship number
    draw.text((338, 232), name, font=font, fill='black')
    draw.text((730, 232), gender, font=font, fill='black')
    draw.text((490, 256), district, font=font, fill='black')
    draw.text((494, 279), municipality, font=font, fill='black')
    draw.text((740, 278), random_digits, font=font, fill='black')
    draw.text((467, 344), year, font=font, fill='black')
    draw.text((566, 346), month, font=font, fill='black')
    draw.text((631, 346), day, font=font, fill='black')
    draw.text((391, 367), father_name, font=font, fill='black')

    # Save the image with the new filename format
    img.save(os.path.join(output_dir, f'template1_citizenship{i+1}.jpg'))

print("800 images generated successfully!")
