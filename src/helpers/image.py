import base64
from io import BytesIO
from PIL import Image

def image_to_base64(image_path):
    """
    Convert an image file to base64 string
    """
    with Image.open(image_path) as image:
        # Convert image to bytes
        buffered = BytesIO()
        image.save(buffered, format=image.format)
        # Encode to base64
        img_str = base64.b64encode(buffered.getvalue())
        return img_str.decode('utf-8')


def save_base64_image(base64_string, output_path):
    """
    Convert a base64 string back to an image file
    """
    # Decode base64 string
    img_data = base64.b64decode(base64_string)
    # Create image from bytes
    img = Image.open(BytesIO(img_data))
    # Save image
    img.save(output_path + f".{img.format.lower()}")
