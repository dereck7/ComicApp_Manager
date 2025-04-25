from PyQt6.QtWidgets import QPushButton, QMenu
from PyQt6.QtCore import Qt
from core import theme_manager
class ThemeControls:
    def __init__(self, parent):
        self.parent = parent
        self.theme_button = QPushButton("Temas")
        self.setup_ui()

    def setup_ui(self):
        self.theme_button.setObjectName("themeButton")
        self.theme_button.setFixedSize(120, 40)
        self.theme_button.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Configurar menú de temas
        theme_menu = QMenu()
        theme_menu.setStyleSheet("""
            QMenu {
                background-color: #333333;
                color: white;
                border: 1px solid #555;
                padding: 5px;
            }
            QMenu::item {
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: #d62828;
            }
        """)
        
        # Añadir opciones de tema
        for theme_id in self.parent.theme_manager.themes:
            action = theme_menu.addAction(theme_id.capitalize())
            action.triggered.connect(lambda checked, t=theme_id: self.parent.set_theme(t))
        
        self.theme_button.setMenu(theme_menu)
        
        # Estilo del botón
        self.theme_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 #555555, stop:1 #222222);
                color: white;
                border: 2px solid #7a7a7a;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 #666666, stop:1 #333333);
                border: 2px solid #d62828;
            }
        """)