from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt

class ShadowLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._shadow_color = QColor(0, 0, 0, 150)  # Color de sombra predeterminado
        self._text_color = QColor("#ffffff")        # Color de texto predeterminado
        self._shadow_offset = 2                    # Desplazamiento de sombra

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        
        # Dibuja sombra
        painter.setPen(self._shadow_color)
        painter.drawText(
            self.rect().translated(self._shadow_offset, self._shadow_offset),
            self.alignment(),
            self.text()
        )
        
        # Dibuja texto principal
        painter.setPen(self._text_color)
        painter.drawText(self.rect(), self.alignment(), self.text())

    def setShadowColor(self, color):
        if isinstance(color, str):
            self._shadow_color = QColor(color)
        else:
            self._shadow_color = color
        self.update()

    def setTextColor(self, color):
        if isinstance(color, str):
            self._text_color = QColor(color)
        else:
            self._text_color = color
        self.update()