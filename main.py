import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from windows.main_window import ComicApp

def main():
    try:
        # Configuración básica
        app = QApplication(sys.argv)
        app.setFont(QFont("Arial", 12))

        # Crear ventana principal
        window = ComicApp()
        window.show()

        sys.exit(app.exec())
    except Exception as e:
        print(f"[ERROR CRÍTICO] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Verificar rutas antes de ejecutar
    base_path = Path(__file__).parent.absolute()
    print(f"[INICIO] Directorio base: {base_path}")
    
    # Ejecutar aplicación
    main()