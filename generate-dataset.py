
import os
from PIL import Image

path = f"../../../android/assets/pokemon/pokemon/"
output_dir = f"./pokemon/"

# Image sizes have to be a power of 2 for vae
size = 64

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
        output = Image.new('RGB', (size, size), (255, 255, 255))

        # Offsets ensure that image is bottom-center of the 56x56 output.
        offset_x = (int)((size - width) / 2)
        offset_y = (int)(size - width)

        # Crop out the top of the image.
        # output.paste(image, (offset_x, offset_y))

        # Required to fixup images because the alpha channel is using black.
        for x in range(width):
            for y in range(width):
                r, g, b, a = image.getpixel((x, y))
                if a == 0:
                    r, g, b = (255, 255, 255)
                output.putpixel((x + offset_x, y + offset_y), (r, g, b))

        with open(fullpath, 'r') as f:
            lines = f.readlines()

        # Parse out type information.
        type1, type2 = lines[5].split("db ")[1].split(";")[0].strip().split(", ")

        vae_class = type1.lower() + " " + type2.lower()

        # Save the cropped image to output directory.
        pokemon_name = dirname
        fullpath = os.path.join(output_dir, vae_class)
        if not os.path.exists(fullpath):
            os.mkdir(fullpath)

        output.save(os.path.join(fullpath, pokemon_name + ".png"), "png") 

        # Save type information to file.
        with open(os.path.join(fullpath, pokemon_name + ".txt"), 'w') as f:
            f.write(vae_class)
