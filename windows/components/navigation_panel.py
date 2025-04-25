from PyQt6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, 
    QPushButton, QFrame
)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize
from themes.Shadow_Label import ShadowLabel
from pathlib import Path

class NavigationPanel:
    def __init__(self, parent):
        self.parent = parent
        self.layout = QHBoxLayout()
        self.setup_ui()

    def setup_ui(self):
        """Configura los componentes de navegación"""
        self.layout.setContentsMargins(50, 20, 50, 50)
        self.layout.setSpacing(50)

        # Obtener fuentes del theme_manager
        title_font = self.parent.theme_manager.get_font("Bangers", 24, True)
        
        # Botón Héroes
        self.heroes_btn = self._create_image_button(350, "heroButton")
        self.heroes_label = ShadowLabel("HÉROES")
        self.heroes_label.setFont(title_font)  # Usamos la fuente obtenida
        self.heroes_label.setObjectName("heroes_label")

        # Botón DC Comics
        self.dc_btn = self._create_image_button(400, "dcButton")
        self.dc_label = ShadowLabel("DC COMICS")
        self.dc_label.setFont(title_font)
        self.dc_label.setObjectName("dc_label")

        # Botón Villanos
        self.villains_btn = self._create_image_button(350, "villainButton")
        self.villains_label = ShadowLabel("VILLANOS")
        self.villains_label.setFont(title_font)
        self.villains_label.setObjectName("villains_label")

        # Añadir botones al layout
        self.layout.addWidget(self._create_button_container(self.heroes_btn, self.heroes_label))
        self.layout.addWidget(self._create_button_container(self.dc_btn, self.dc_label))
        self.layout.addWidget(self._create_button_container(self.villains_btn, self.villains_label))

    def _create_image_button(self, size: int, object_name: str) -> QPushButton:
        """Crea un botón con imagen"""
        btn = QPushButton()
        btn.setObjectName(object_name)
        btn.setFixedSize(size, size)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 30);
            }
        """)
        return btn

    def _create_button_container(self, button: QPushButton, label: ShadowLabel) -> QFrame:
        """Envuelve un botón y su etiqueta en un contenedor"""
        container = QFrame()
        container.setFixedHeight(int(button.height() * 1.25))
        
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10)
        
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        return container

    def update_theme(self, theme_name: str):
        """Actualiza los íconos según el tema"""
        logos = self.parent.theme_manager.get_logo_paths(theme_name)
        
        # Cargar imágenes
        self._load_button_image(self.dc_btn, logos.get('dc'))
        self._load_button_image(self.heroes_btn, logos.get('hero'))
        self._load_button_image(self.villains_btn, logos.get('villain'))

    def _load_button_image(self, button: QPushButton, image_path: str):
        """Carga una imagen en un botón"""
        if image_path and Path(image_path).exists():
            pixmap = QPixmap(image_path).scaled(
                button.width(), button.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            button.setIcon(QIcon(pixmap))
            button.setIconSize(QSize(button.width(), button.height()))