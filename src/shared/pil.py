# Third-party imports.
from PIL import Image
from PIL.ImageQt import ImageQt
from PySide6.QtGui import QPixmap

# Local imports.
from src.shared.funcs import path

def change_image_colour(img_src: str, new_color: tuple[int, int, int]) -> QPixmap:
    """Converts the colour in a PNG to another colour, returning a QPixmap object.

    Args:
        img_src (str): Source of the image file.
        new_color (tuple[int, int, int]): New colour to set the image to. (R, G, B)

    Returns:
        QPixmap: The recoloured image as a QPixmap object.
    """
    img_src = path(img_src)
    img = Image.open(img_src).convert("RGBA")
    pixels = img.load()
    width, height = img.size
    
    # Replaces all non-transparent pixels.
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            
            if a != 0:
                pixels[x, y] = (*new_color, a)

    qimage = ImageQt(img)
    pixmap = QPixmap.fromImage(qimage)
    
    return pixmap