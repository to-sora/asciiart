# ASCII Art Generator

## Description
This script converts an image into colorful ASCII art using a specified character sequence. It ensures compatibility with various character widths (e.g., half-width, full-width).

---

## Usage
Run the script with the following arguments:

```bash
python main.py <image_path> <scale> <character_sequence>
```

Parameters:

    <image_path>: Path to the image file.
    <scale>: Scale factor for resizing the image (e.g., 0.5 for half size).
    <character_sequence>: A sequence of characters to use for the ASCII art.

Example:
```bash
python main.py sample.jpg 0.5 "@#$%"
```
