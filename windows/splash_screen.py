from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QMovie

class SplashScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.SplashScreen | Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(600, 600)
        
        layout = QVBoxLayout(self)
        self.label = QLabel("Cargando tema...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Opcional: Añadir un GIF de carga
        self.movie = QMovie("loading.gif")  # Asegúrate de tener este archivo
        self.movie_label = QLabel()
        self.movie_label.setMovie(self.movie)
        
        layout.addWidget(self.movie_label)
        layout.addWidget(self.label)
        self.movie.start()

    def show_for(self, duration_ms: int):
        self.show()
        QTimer.singleShot(duration_ms, self.close)