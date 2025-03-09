from src.imports import *

class Login(QWidget):
    def __init__(
            self,
            parent: QWidget,
            main_window: QWidget
    ):
        super().__init__(parent)
        
        # Assigning args to self.
        self.main_window = main_window
        self.config = LoginConfig()
    
        self._set_design()
        self._set_widgets()
    
    def _set_design(self):
        self.setFixedSize(self.parentWidget().size())
    
    def _set_widgets(self):
        self.background = self.Background(
            parent = self,
            config = self.config
        )
        
        self.triangle = self.Triangle(
            parent = self,
            config = self.config.triangle
        )
        
        self.texture = self.Texture(
            parent = self,
            config = self.config.texture
        )
    
    def resizeEvent(self, event: QResizeEvent):
        # Resize the background to fill the size of the login screen.
        self.background.setFixedSize(self.size())
        self.triangle.setFixedSize(self.size())
        
        return super().resizeEvent(event)
            
    class Background(QLabel):
        def __init__(
                self,
                parent: QWidget,
                config: LoginConfig
        ):
            super().__init__(parent)
            self.config = config
            
            self.setFixedSize(self.parentWidget().size())
            self.setStyleSheet(f"background-color: {self.config.background_colour}")
    
    class Texture(QLabel):
        def __init__(
                self,
                parent: QWidget,
                config: LoginConfig.Texture
        ):
            super().__init__(parent)
            self.config = config
            
            self._set_design()
        
        def _set_design(self):
            self.setFixedSize(self.parentWidget().size())
            self.setPixmap(self.create_texture_pixmap(self.size()))
            self.setStyleSheet("background-color: transparent;")
        
        def create_texture_pixmap(self, size: QSize) -> QPixmap:
            colour_values = self.config.icon_colour.replace("rgb(", "").replace(")", "").split(",")
            red = int(colour_values[0])
            green = int(colour_values[1])
            blue = int(colour_values[2])
            
            pixmap = QPixmap(size)
            pixmap.fill(Qt.GlobalColor.transparent)
            
            up_icon = change_svg_colour(self.config.icon_src, (64, 64), (red, green, blue))
            down_icon = up_icon.copy().transformed(QTransform().rotate(180), Qt.TransformationMode.SmoothTransformation)
    
            # Painter object to paint the texture onto the pixmap.
            painter = QPainter(pixmap)

            painter.drawPixmap(QPoint(100, 100), up_icon)
            painter.drawPixmap(QPoint(82, 82), down_icon)
            painter.drawPixmap(QPoint(64, 100), up_icon)
            
            painter.end()
            
            return pixmap
            
    class Triangle(QLabel):
        def __init__(
                self,
                parent: QWidget,
                config: LoginConfig.Triangle
        ):
            super().__init__(parent)
            self.config = config
            
            self._set_design()

        def _set_design(self):
            self.setFixedSize(self.parentWidget().size())
            self.setPixmap(self.create_triangle_pixmap(self.width(), self.height()))
            self.setStyleSheet("background-color: transparent;") # So objects can be viewed behind it.

        def create_triangle_pixmap(self, width: int, height: int) -> QPixmap:
            colour_values = self.config.background_colour.replace("rgb(", "").replace(")", "").split(",")
            red = int(colour_values[0])
            green = int(colour_values[1])
            blue = int(colour_values[2])
            
            colour = QColor(red, green, blue)
            
            # Transparent pixmap to paint to.
            pixmap = QPixmap(width, height)
            pixmap.fill(Qt.GlobalColor.transparent)
            
            # Painter object to draw triangle.
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Define the points of the triangle.
            top_left = QPoint(0, 0)
            top_right = QPoint(self.width(), 0)
            right_middle = QPoint(self.width(), int(self.height() / 2))
            bottom_middle = QPoint(int(self.width() / 2), self.height())
            bottom_left = QPoint(0, self.height())
            
            # Draw the triangle.
            painter.setPen(colour) # Create the lines.
            painter.setBrush(colour) # Fill the triangle.
            
            draw_points = [top_left, top_right, right_middle, bottom_middle, bottom_left] # Points to draw in order.
            
            painter.drawPolygon(draw_points) # Draw the shape.
            
            painter.end()
            
            return pixmap
        
        def resizeEvent(self, event: QResizeEvent):
            pixmap = self.create_triangle_pixmap(event.size().width(), event.size().height())
            self.setPixmap(pixmap)
            
            return super().resizeEvent(event)