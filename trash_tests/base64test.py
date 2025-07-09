import base64
from io import BytesIO
from PIL import Image


def image_to_base64(image_path):
    """
    Convert an image file to base64 string
    """
    try:
        with Image.open(image_path) as image:
            # Convert image to bytes
            buffered = BytesIO()
            image.save(buffered, format=image.format)
            # Encode to base64
            img_str = base64.b64encode(buffered.getvalue())
            return img_str.decode('utf-8')
    except Exception as e:
        print(f"Error converting image to base64: {e}")
        return None


def base64_to_image(base64_string, output_path):
    """
    Convert a base64 string back to an image file
    """
    try:
        # Decode base64 string
        img_data = base64.b64decode(base64_string)
        # Create image from bytes
        img = Image.open(BytesIO(img_data))
        # Save image
        img.save(output_path)
        return True
    except Exception as e:
        print(f"Error converting base64 to image: {e}")
        return False


# Example usage
if __name__ == "__main__":
    # Convert image to base64
    base64_str = image_to_base64("./img.png")
    if base64_str:
        print("Image converted to base64 successfully")

        # Convert back to image
        if base64_to_image(base64_str, "output_image.jpg"):
            print("Base64 converted back to image successfully")