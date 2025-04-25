from PyQt6.QtWidgets import (
    QScrollArea, QWidget, QVBoxLayout, 
    QLabel, QFrame, QHBoxLayout
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize
from models.comic import Comic

class ComicPanel(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setup_ui()
        
    def setup_ui(self):
        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(15)
        self.setWidget(self.container)
        
    def display_comics(self, comics: list[Comic]):
        """Muestra los cómics en el panel"""
        self.clear()
        
        for comic in comics:
            comic_frame = QFrame()
            comic_frame.setFrameShape(QFrame.Shape.StyledPanel)
            comic_frame.setStyleSheet("""
                QFrame {
                    background: rgba(30, 30, 30, 150);
                    border-radius: 5px;
                }
            """)
            
            layout = QHBoxLayout(comic_frame)
            
            # Portada
            cover_label = QLabel()
            cover_pixmap = QPixmap(comic.get_cover_or_default())
            if not cover_pixmap.isNull():
                cover_pixmap = cover_pixmap.scaled(
                    100, 150, 
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                cover_label.setPixmap(cover_pixmap)
            
            # Info
            info_label = QLabel(
                f"<b>{comic.character}: {comic.title}</b><br>"
                f"Archivo: {comic.file_path}"
            )
            info_label.setWordWrap(True)
            
            layout.addWidget(cover_label)
            layout.addWidget(info_label)
            self.layout.addWidget(comic_frame)
    
    def clear(self):
        """Limpia el panel"""
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()