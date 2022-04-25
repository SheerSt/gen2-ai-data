
import os
from PIL import Image

path = f"../../../android/assets/pokemon/pokemon/"
output_dir = f"./pokemon/"

for root, dirnames, _ in os.walk(path):

    for dirname in dirnames:

        fullpath = os.path.join(root, dirname, "front.png")

        # Skip this Pokemon if front.png doesn't exist.
        if not os.path.exists(fullpath):
            continue

        # Open PIL image.
        image = Image.open(fullpath).convert('RGBA')
        width, height = image.size

        # Open base stats file to get type data.
        fullpath = os.path.join(root, dirname, "base_stats.asm")

        # Skip this Pokemon if base_stats.asm doesn't exist.
        if not os.path.exists(fullpath):
            continue

        # Create the output image.
        output = Image.new('RGBA', (56, 56), (255, 255, 255, 0))

        # Offsets ensure that image is bottom-center of the 56x56 output.
        offset_x = (int)((56 - width) / 2)
        offset_y =  (int)(56 - width)

        # Crop out the top of the image.
        output.paste(image, (offset_x, offset_y))

        # Save the cropped image to output directory.
        pokemon_name = dirname
        output.save(output_dir + pokemon_name + ".png", "png") 

        with open(fullpath, 'r') as f:
            lines = f.readlines()

        # Parse out type information.
        type1, type2 = lines[5].split("db ")[1].split(";")[0].strip().split(", ")

        # Save type information to file.
        with open(output_dir + pokemon_name + ".txt", 'w') as f:
            f.write(type1.lower() + " " + type2.lower())
