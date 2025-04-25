import os
from pathlib import Path
import random
from PyQt6.QtCore import QFile, QTextStream
from PyQt6.QtGui import QFont

class ThemeManager:
    def __init__(self, app_dir: str):
        # Convertir a Path y asegurar rutas absolutas
        self.app_dir = Path(app_dir).absolute()
        self.themes_dir = self.app_dir / 'themes' / 'temas'
        self.img_dir = self.app_dir / 'logos'
        self.heroes_dir = self.img_dir / 'Heroes'
        self.villains_dir = self.img_dir / 'Villanos'

        # Fuentes predefinidas
        self.available_fonts = {
            "Bangers": "Bangers-Regular.ttf",
            "Arial": "Arial.ttf",
            "Roboto": "Roboto-Medium.ttf"
        }

        # Validar existencia de directorios
        if not self.themes_dir.exists():
            raise FileNotFoundError(f"No se encontró el directorio de temas: {self.themes_dir}")
        if not self.img_dir.exists():
            print(f"[ADVERTENCIA] No se encontró el directorio de logos: {self.img_dir}")

        # Inicialización segura
        self.themes = self._discover_themes()
        self.current_theme = list(self.themes.keys())[0] if self.themes else None

    def get_font(self, font_name: str, size: int = 12, bold: bool = False) -> QFont:
        """
        Obtiene una fuente configurada
        Args:
            font_name: Nombre de la fuente (Bangers, Arial, etc.)
            size: Tamaño de la fuente
            bold: Si la fuente es negrita
        Returns:
            QFont configurada
        """
        font = QFont(font_name, size)
        font.setBold(bold)

        # Verificar si la fuente está disponible
        if font_name not in self.available_fonts:
            print(f"Advertencia: Fuente {font_name} no encontrada. Usando Arial")
            font = QFont("Arial", size)
            font.setBold(bold)
            
        return font

    def _discover_themes(self) -> dict:
        """Descubre todos los temas .qss disponibles"""
        themes = {}
        try:
            for file in self.themes_dir.glob('*.qss'):
                theme_name = file.stem
                themes[theme_name] = {
                    'name': theme_name.capitalize(),
                    'path': str(file),
                    'config': self._get_theme_config(theme_name)
                }
        except Exception as e:
            print(f"Error al descubrir temas: {e}")
        return themes

    def _get_theme_config(self, theme_name: str) -> dict:
        """Configuración específica para cada tema"""
        return {
            'Claro': {
                'dc_logo': 'DC_comics.png',
                'hero_mode': 'random',
                'villain_mode': 'random'
            },
            'Batman': {
                'dc_logo': 'DC_Batman.png',
                'hero_mode': 'specific',
                'hero_image': 'Batman.png',
                'villain_mode': 'specific',
                'villain_image': 'Joker.png'
            },
            'Superman': {
                'dc_logo': 'DC_Superman.png',
                'hero_mode': 'specific',
                'hero_image': 'Superman.png',
                'villain_mode': 'specific',
                'villain_image': 'Doomsday.png'
            }
        }.get(theme_name, {})

    def get_theme_qss(self, theme_name: str) -> str:
        """Carga el contenido QSS de un tema"""
        if theme_name in self.themes:
            try:
                file = QFile(self.themes[theme_name]['path'])
                if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
                    return QTextStream(file).readAll()
            except Exception as e:
                print(f"Error cargando QSS: {e}")
        return ""

    def get_logo_paths(self, theme_name: str) -> dict:
        """Obtiene rutas de logos para un tema"""
        if theme_name not in self.themes:
            return {}

        config = self.themes[theme_name]['config']
        paths = {}
        
        # Logo DC
        if 'dc_logo' in config:
            dc_path = self.img_dir / config['dc_logo']
            if dc_path.exists():
                paths['dc'] = str(dc_path)

        # Héroe
        if config.get('hero_mode') == 'specific' and 'hero_image' in config:
            hero_path = self.heroes_dir / config['hero_image']
            if hero_path.exists():
                paths['hero'] = str(hero_path)
        elif config.get('hero_mode') == 'random':
            if self.heroes_dir.exists():
                heroes = list(self.heroes_dir.glob('*.png')) + list(self.heroes_dir.glob('*.jpg'))
                if heroes:
                    paths['hero'] = str(random.choice(heroes))

        # Villano (misma lógica que héroe)
        if config.get('villain_mode') == 'specific' and 'villain_image' in config:
            villain_path = self.villains_dir / config['villain_image']
            if villain_path.exists():
                paths['villain'] = str(villain_path)
        elif config.get('villain_mode') == 'random':
            if self.villains_dir.exists():
                villains = list(self.villains_dir.glob('*.png')) + list(self.villains_dir.glob('*.jpg'))
                if villains:
                    paths['villain'] = str(random.choice(villains))

        return paths
    