from PIL import Image, ImageOps

def correct_image_orientation(uploaded_file):
    image = Image.open(uploaded_file)
    image = ImageOps.exif_transpose(image)
    return image