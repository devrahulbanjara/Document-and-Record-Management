from PIL import Image, ImageDraw, ImageFont

# Path to the test font
font_path = '/mnt/c/Users/drenergydrink/Desktop/Document-and-Record-Management/Citizenship Generator/Preeti Normal.otf'

# Create a new image
img = Image.new('RGB', (800, 600), color='white')
draw = ImageDraw.Draw(img)

# Load the font
try:
    font = ImageFont.truetype(font_path, 40)
except OSError as e:
    print(f"Error loading font: {e}")
    font = ImageFont.load_default()

# Sample text
text = "यह एक परीक्षण है।"

# Add text to image
draw.text((50, 50), text, font=font, fill='black')

# Save the image
img.save('/mnt/c/Users/drenergydrink/Desktop/Document-and-Record-Management/Citizenship Generator/test_font_output.jpg')

print("Font test image generated successfully!")
