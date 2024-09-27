from PIL import ImageDraw, ImageFont

def draw_citizenship_details(draw, details, font):
    draw.text((10, 20), f"नाम       : {details['name']}", font=font, fill=(0, 0, 0))
    draw.text((10, 60), f"जन्मस्थान    : {details.get('district', 'Unknown')}", font=font, fill=(0, 0, 0))
    draw.text((10, 100), f"जन्म साल   : {details.get('year_of_birth', 'Unknown')}", font=font, fill=(0, 0, 0))
    draw.text((10, 140), f"लिङ्ग       : {details.get('gender', 'Unknown')}", font=font, fill=(0, 0, 0))
    draw.text((10, 180), f"नागरिकता नम्बर: {details.get('citizenship_number', 'Unknown')}", font=font, fill=(0, 0, 0))

def draw_license_details(draw, details, font):
    draw.text((10, 20), f"Name              : {details['name']}", font=font, fill=(0, 0, 0))
    draw.text((10, 60), f"DOB               : {details.get('dob', 'Unknown')}", font=font, fill=(0, 0, 0))
    draw.text((10, 100), f"Contact Number    : {details.get('contact_number', 'Unknown')}", font=font, fill=(0, 0, 0))
    draw.text((10, 140), f"Citizenship Number: {details.get('citizenship_number', 'Unknown')}", font=font, fill=(0, 0, 0))
    draw.text((10, 180), f"License Number    : {details.get('license_number', 'Unknown')}", font=font, fill=(0, 0, 0))

def draw_passport_details(draw, details, font):
    draw.text((10, 20), f"Name              : {details['name']}", font=font, fill=(0, 0, 0))
    draw.text((10, 60), f"Surname           : {details.get('surname', 'Unknown')}", font=font, fill=(0, 0, 0))
    draw.text((10, 100), f"DOB               : {details.get('dob', 'Unknown')}", font=font, fill=(0, 0, 0))
    draw.text((10, 140), f"Citizenship Number: {details.get('citizenship_number', 'Unknown')}", font=font, fill=(0, 0, 0))
    draw.text((10, 180), f"Passport Number   : {details.get('passport_number', 'Unknown')}", font=font, fill=(0, 0, 0))