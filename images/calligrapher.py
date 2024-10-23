from PIL import Image, UnidentifiedImageError
import os
from rembg import remove
from io import BytesIO

# Folder containing the images
input_folder = './signatures/'
output_folder = './signatures_new/'

# Creating output directory if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Max dimension constraint
max_dimension = 60

# Function to process the images
def process_images(input_folder, output_folder, max_dimension):
    for filename in os.listdir(input_folder):
        if filename.endswith('.png'):
            image_path = os.path.join(input_folder, filename)
            print(f"Processing {image_path}")

            try:
                with open(image_path, 'rb') as input_file:
                    # Remove background using rembg
                    img_data = remove(input_file.read())

                    # Convert the binary data to a BytesIO object
                    img_no_bg = Image.open(BytesIO(img_data))

                    # Resize image maintaining aspect ratio
                    img_width, img_height = img_no_bg.size
                    aspect_ratio = img_width / img_height

                    if img_width > img_height:
                        new_width = max_dimension
                        new_height = int(max_dimension / aspect_ratio)
                    else:
                        new_height = max_dimension
                        new_width = int(max_dimension * aspect_ratio)

                    # Replace ANTIALIAS with LANCZOS for resizing
                    img_resized = img_no_bg.resize((new_width, new_height), Image.Resampling.LANCZOS)

                    # Save the processed image
                    output_path = os.path.join(output_folder, filename)
                    img_resized.save(output_path, format='PNG')
                    print(f"Saved resized image to {output_path}")

            except UnidentifiedImageError:
                print(f"Unidentified image file: {image_path}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Processing the images
process_images(input_folder, output_folder, max_dimension)
