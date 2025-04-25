from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, 
    QLabel, QTreeView,
    QSplitter, QPushButton
)
from PyQt6.QtCore import QDir, Qt
from PyQt6.QtGui import QIcon, QFileSystemModel
from pathlib import Path

class ComicsWindow(QMainWindow):
    def __init__(self, comics_path, parent=None):
        super().__init__(parent)
        self.comics_path = Path(comics_path)
        self.setWindowTitle("Explorador de Cómics")
        self.setGeometry(100, 100, 800, 600)
        
        self.init_ui()
        self.load_comics()

    def init_ui(self):
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Splitter para dividir el espacio
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Modelo del sistema de archivos
        self.model = QFileSystemModel()
        self.model.setRootPath(str(self.comics_path))
        self.model.setFilter(QDir.Filter.AllDirs | QDir.Filter.Files)
        self.model.setNameFilters(["*.cbr", "*.cbz"])
        self.model.setNameFilterDisables(False)
        
        # Vista de árbol
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(str(self.comics_path)))
        self.tree.setColumnWidth(0, 250)
        self.tree.doubleClicked.connect(self.open_comic)
        
        # Panel de vista previa
        self.preview_panel = QLabel()
        self.preview_panel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_panel.setText("Selecciona un cómic para previsualizar")
        self.preview_panel.setStyleSheet("""
            QLabel {
                background: #333;
                color: #fff;
                font-size: 16px;
                border: 1px solid #555;
            }
        """)
        
        # Añadir widgets al splitter
        splitter.addWidget(self.tree)
        splitter.addWidget(self.preview_panel)
        splitter.setSizes([300, 500])
        
        # Botones
        self.open_btn = QPushButton("Abrir Cómic")
        self.open_btn.setIcon(QIcon.fromTheme("document-open"))
        self.open_btn.clicked.connect(self.open_selected_comic)
        
        # Añadir al layout principal
        main_layout.addWidget(splitter)
        main_layout.addWidget(self.open_btn)

    def load_comics(self):
        """Carga la estructura de cómics"""
        if not self.comics_path.exists():
            print(f"Error: No se encontró la carpeta {self.comics_path}")
            return

    def open_comic(self, index):
        """Maneja la selección de un cómic"""
        path = self.model.filePath(index)
        if path.lower().endswith(('.cbr', '.cbz')):
            self.current_comic = path
            # Aquí podrías cargar una miniatura si quieres
            self.preview_panel.setText(f"Cómic seleccionado:\n{Path(path).name}")

    def open_selected_comic(self):
        """Abre el cómic seleccionado"""
        if hasattr(self, 'current_comic'):
            print(f"Abriendo cómic: {self.current_comic}")
            # Aquí implementarías la lógica para abrir el cómic
            # Por ejemplo:
            # import subprocess
            # subprocess.run(['tu_lector_de_comics', self.current_comic])