from src.shared.imports import *

class TopBar(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setHidden(True) # Start hidden.
        
        self.setFixedWidth(self.parentWidget().width())
        self.setFixedHeight(50)
    
        self.background_label = self.BackgroundLabel(self)
        self.chats = self.Chats(self)
        self.right_buttons = self.RightButtons(self)
    
    def resizeEvent(self, event: QResizeEvent):
        # Move the right buttons to the right side of the top bar.
        self.right_buttons.move(
            self.width() - self.right_buttons.width(), # Right side of top bar.
            self.right_buttons.y() # Same as before.
        )
        
        return super().resizeEvent(event)
    
    class BackgroundLabel(QLabel):
        def __init__(self, parent: QWidget):
            super().__init__(parent)
            self.setFixedSize(self.parentWidget().size())
            self.setStyleSheet("background-color: white;")
    
    class Chats(QWidget):
        def __init__(self, parent: QWidget):
            super().__init__(parent)
            self.main_layout = QHBoxLayout()
            self.setLayout(self.main_layout)
            
            self.main_layout.addWidget(self.Button(self))
            self.main_layout.addWidget(self.Button(self))
            self.main_layout.addWidget(self.Button(self))
            
            self.setFixedHeight(self.parentWidget().height())
            self.setFixedWidth(self.sizeHint().width())
    
        class Button(QPushButton):
            def __init__(self, parent: QWidget):
                super().__init__(parent)
    
    class RightButtons(QWidget):
        def __init__(self, parent: QWidget):
            super().__init__(parent)
            self.main_layout = QHBoxLayout()
            self.setLayout(self.main_layout)
            
            self.main_layout.addWidget(self.Button(self))
            self.main_layout.addWidget(self.Button(self))
            self.main_layout.addWidget(self.Button(self))
            
            self.setFixedHeight(self.parentWidget().height())
            self.setFixedWidth(self.sizeHint().width())
        
        class Button(QPushButton):
            def __init__(self, parent: QWidget):
                super().__init__(parent)