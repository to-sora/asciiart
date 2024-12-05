#!/usr/bin/env python3
import sys
from PIL import Image
import unicodedata

import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import os
if os.name == 'nt':
    import ctypes
    kernel32 = ctypes.windll.kernel32
    # Enable ANSI escape sequences
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


def main():
    # Check for correct number of arguments
    if len(sys.argv) != 4:
        print("Usage: python ascii_art.py <image_path> <scale> <character_sequence>")
        sys.exit(1)

    image_path = sys.argv[1]
    try:
        scale = float(sys.argv[2])
    except ValueError:
        print("Scale must be a number (e.g., 0.5 for half size).")
        sys.exit(1)

    char_sequence = sys.argv[3]
    if not char_sequence:
        print("Character sequence must not be empty.")
        sys.exit(1)

    # Calculate the total display width of the character sequence
    char_widths = [char_display_width(c) for c in char_sequence]
    total_char_width = sum(char_widths)

    # Open the image
    try:
        image = Image.open(image_path)
    except IOError:
        print(f"Cannot open image file: {image_path}")
        sys.exit(1)

    # Original image dimensions
    original_width, original_height = image.size
    aspect_ratio = original_height / original_width

    # Adjust the new width based on the scale and character widths
    new_width = int(original_width * scale)
    new_height = int(aspect_ratio * new_width * 0.5)  # Adjust for character aspect ratio

    # Resize the image
    image = image.resize((new_width, new_height))
    image = image.convert('RGB')  # Ensure image is in RGB mode

    # Convert image to ASCII art
    ascii_art = convert_to_ascii(image, char_sequence, char_widths)

    # Print the ASCII art
    print(ascii_art)

def char_display_width(char):
    """Determine the display width of a Unicode character."""
    east_asian_width = unicodedata.east_asian_width(char)
    if east_asian_width in ('F', 'W', 'A'):
        return 2  # Full-width character
    else:
        return 1  # Half-width character

def convert_to_ascii(image, char_sequence, char_widths):
    pixels = image.load()
    img_width, img_height = image.size
    num_chars = len(char_sequence)
    ascii_art_lines = []

    char_index = 0  # To iterate over the character sequence

    for y in range(img_height):
        line = ""
        x = 0
        while x < img_width:
            r, g, b = pixels[x, y]
            # Get the current character and its display width
            char = char_sequence[char_index % num_chars]
            width = char_widths[char_index % num_chars]
            char_index += 1  # Move to the next character in the sequence

            # ANSI escape code for setting the foreground color
            ansi_color = f"\033[38;2;{r};{g};{b}m"
            line += f"{ansi_color}{char}\033[0m"

            x += 1  # Move to the next pixel
            if width == 2:
                x += 1  # Skip an extra pixel for full-width character

        ascii_art_lines.append(line)

    return "\n".join(ascii_art_lines)

if __name__ == "__main__":
    main()
