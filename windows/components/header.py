from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QFont,QColor
from themes.Shadow_Label import ShadowLabel
from PyQt6.QtCore import Qt

class MainHeader:
    def __init__(self, parent):
        self.parent = parent
        self.layout = QVBoxLayout()
        self.setup_ui()

    def setup_ui(self):
        # Layout horizontal para el título
        title_layout = QHBoxLayout()
        
        # Título principal
        self.title_label = ShadowLabel("DC COMIC MANAGER")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Bangers", 48, QFont.Weight.Bold))
        self.title_label.setObjectName("title_label")
        
        # Subtítulo
        self.subtitle_label = ShadowLabel("Organiza tu colección de cómics")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.subtitle_label.setObjectName("subtitle_label")
        
        # Añadir al layout
        title_layout.addWidget(self.title_label)
        self.layout.addLayout(title_layout)
        self.layout.addWidget(self.subtitle_label)

    def update_theme(self, theme_name):
        colors = {
            "batman": {"title": "#d62828", "subtitle": "#e0e0e0"},
            "superman": {"title": "#0D47A1", "subtitle": "#333333"},
            "claro": {"title": "#d62828", "subtitle": "#333333"}
        }
        theme_colors = colors.get(theme_name.lower(), colors["claro"])
        self.title_label.setTextColor(QColor(theme_colors["title"]))
        self.subtitle_label.setTextColor(QColor(theme_colors["subtitle"]))