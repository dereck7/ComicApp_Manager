import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QMessageBox
)
from PyQt6.QtGui import QKeySequence, QIcon, QShortcut
from PyQt6.QtCore import Qt
from core.theme_manager import ThemeManager
from core.comic_loader import ComicLoader
from windows.comics_window import ComicsWindow
from windows.components.header import MainHeader
from windows.components.theme_controls import ThemeControls
from windows.components.navigation_panel import NavigationPanel

class ComicApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuración de rutas
        self.current_dir = Path(__file__).parent.parent.absolute()
        print(f"[DEBUG] Directorio base: {self.current_dir}")
        
        # Inicialización de componentes
        self.init_managers()
        self.init_ui()
        self.apply_theme()

    def init_managers(self):
        """Inicializa los gestores principales"""
        try:
            self.theme_manager = ThemeManager(self.current_dir)
            self.current_theme = (
                list(self.theme_manager.themes.keys())[0] 
                if self.theme_manager.themes 
                else 'Claro'
            )
            
            comics_root = self.current_dir.parent / "comics"
            self.comic_loader = ComicLoader(comics_root)
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Error de Inicialización", 
                f"No se pudieron cargar los recursos:\n{str(e)}"
            )
            raise

    def init_ui(self):
        """Configura la interfaz de usuario principal"""
        self.setWindowTitle("DC Comic Manager")
        self.setWindowIcon(QIcon(str(self.current_dir / "logos" / "DC_comics.png")))
        self.showFullScreen()

        # Widget central
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 10, 20, 20)
        main_layout.setSpacing(15)

        # Componentes
        self.header = MainHeader(self)
        self.theme_controls = ThemeControls(self)
        self.navigation_panel = NavigationPanel(self)

        # Botón de salida
        self.exit_btn = QPushButton("Salir (ESC)")
        self.exit_btn.setObjectName("exitButton")
        self.exit_btn.setFixedSize(120, 40)
        self.exit_btn.clicked.connect(self.toggle_fullscreen)

        # Configurar atajos
        self.exit_shortcut = QShortcut(QKeySequence("Esc"), self)
        self.exit_shortcut.activated.connect(self.toggle_fullscreen)

        # Conexiones de navegación
        self.navigation_panel.heroes_btn.clicked.connect(
            lambda: self.open_comics_category("heroes")
        )
        self.navigation_panel.villains_btn.clicked.connect(
            lambda: self.open_comics_category("villains")
        )
        self.navigation_panel.dc_btn.clicked.connect(self.show_dc_info)

        # Añadir componentes al layout
        main_layout.addLayout(self.header.layout)
        main_layout.addWidget(self.theme_controls.theme_button, 
                            alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addLayout(self.navigation_panel.layout)
        main_layout.addWidget(self.exit_btn, 
                            alignment=Qt.AlignmentFlag.AlignCenter)

    def open_comics_category(self, category: str):
        """Abre la ventana de cómics para la categoría especificada"""
        try:
            category_path = self.comic_loader.get_category_path(category)
            if not category_path.exists():
                raise FileNotFoundError(f"No se encontró la categoría: {category}")
                
            self.comics_window = ComicsWindow(category_path, self)
            self.comics_window.show()
            
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error al cargar cómics",
                f"No se pudo abrir la categoría {category}:\n{str(e)}"
            )

    def show_dc_info(self):
        """Muestra información sobre DC Comics"""
        QMessageBox.information(
            self,
            "DC Comics by dRk",
            "Bienvenido al gestor de cómics de DC\n\n"
            "Versión 1.0\n"
            "© 2025 DC Comics Manager"
        )

    def apply_theme(self):
        """Aplica el tema seleccionado a la interfaz"""
        try:
            qss = self.theme_manager.get_theme_qss(self.current_theme)
            self.setStyleSheet(qss)
            self.header.update_theme(self.current_theme)
            self.navigation_panel.update_theme(self.current_theme)
        except Exception as e:
            print(f"Error aplicando tema: {e}")

    def set_theme(self, theme_id: str):
        """Cambia el tema actual"""
        self.current_theme = theme_id
        self.apply_theme()

    def toggle_fullscreen(self):
        """Alterna entre pantalla completa y modo ventana"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def closeEvent(self, event):
        """Maneja el cierre de la aplicación"""
        reply = QMessageBox.question(
            self,
            "Salir",
            "¿Estás seguro de que quieres salir?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()