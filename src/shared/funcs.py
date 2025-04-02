from PySide6.QtSvg import QtSvg, QSvgRenderer
from PySide6.QtGui import QPainter, QPixmap, QColor, QBrush
from PySide6.QtCore import QSize, Qt
from PySide6.QtXml import QDomDocument

def path(src: str) -> str:
    """A function to fix paths

    Args:
        src (str): Source directory to be fixed.

    Returns:
        str: Fixed Source directory.
    """
    if src[0] == "/": # Removes the first / from the relative path.
        src = src[1:]
    
    return src

def get_svg(src: str, size: QSize = None, colour: QColor = None) -> QPixmap:
    renderer = QSvgRenderer(path(src))
    pixmap = QPixmap(renderer.defaultSize())
    
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    
    painter.setCompositionMode(painter.CompositionMode.CompositionMode_SourceIn)
    
    if colour is None:
        painter.fillRect(pixmap.rect(), QColor(255, 0, 0))
    else:
        painter.fillRect(pixmap.rect(), colour)
    
    painter.end()
    
    return pixmap.scaled(
        size,
        aspectMode = Qt.AspectRatioMode.IgnoreAspectRatio,
        mode = Qt.TransformationMode.SmoothTransformation
    )

def replace_svg_elements(
        src: str,
        colours: list[QColor]
) -> QDomDocument:
    """A function to load an SVG as a document, replace colours within its style and return the document.

    Args:
        src (str): Source string of the SVG file.
        colours (list[QColor]): Colours to replace.

    Returns:
        QDomDocument: Document editted.
    """
    # Loading to document data.
    with open(path(src), "r") as file:
        svg_data = file.read()
        
    # Creatin document object from read binary data.
    dom = QDomDocument()
    dom.setContent(svg_data)
    
    # Getting the style elements within the document.
    dom_elements = dom.elementsByTagName("style")
    
    # For each style element found in the dom document.
    for i in range(dom_elements.count()):
        dom_style_element = dom_elements.item(i).toElement() # Getting the element object.
        dom_style_content = dom_style_element.text() # Getting the content of the element as string.
        
        # For each colour in the colours list.
        for x in range(len(colours)):
            colour = colours[x].name(QColor.NameFormat.HexRgb) # Get colour from list as hex string.
            current_fill = f"fill_{x + 1}" # Get the name of the fill area in the document.
            
            # Replace the fill area with the new colour.
            dom_style_content = dom_style_content.replace(current_fill, colour)
        
        # Set the updated style string back to dom_style_element.
        text_node = dom_style_element.firstChild()
        if text_node.isText():
            text_node.setNodeValue(dom_style_content)
    
    # Return the modified QDomDocument.
    return dom
    
def get_svg_using_elements(
        src: str,
        colours: list[QColor],
        size: QSize = None,
    ) -> QPixmap:
    dom = replace_svg_elements(src, colours) # Obtain modified qdom XML.
    dom_data = dom.toString() # Serialise modified XML to string.
    
    renderer = QSvgRenderer() # Create the renderer object.
    renderer.load(dom_data.encode()) # Load the new SVG data to the renderer object.
    
    # Create and fill a blank pixmap to paint on.
    pixmap = QPixmap(renderer.defaultSize())
    pixmap.fill(Qt.GlobalColor.transparent)
    
    # Paint the SVG onto the pixmap using painter.
    painter = QPainter(pixmap)
    renderer.render(painter)
    
    painter.end()
    
    # Return a scaled version of the modified SVG as a QPixmap.
    return pixmap.scaled(
        size,
        aspectMode = Qt.AspectRatioMode.IgnoreAspectRatio,
        mode = Qt.TransformationMode.SmoothTransformation
    )