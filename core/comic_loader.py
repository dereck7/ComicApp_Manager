import os
from pathlib import Path
from typing import List
from models.comic import Comic

class ComicLoader:
    def __init__(self, comics_root: str):
        self.root = Path(comics_root)
        
    def load_category(self, category: str) -> List[Comic]:
        """Carga cómics de una categoría específica"""
        category_map = {
            "heroes": "01_Heroes",
            "villains": "02_Villanos"
        }
        comics = []
        category_path = self.root / category_map.get(category, "")
        
        if category_path.exists():
            for char_dir in category_path.iterdir():
                if char_dir.is_dir():
                    for comic_file in char_dir.glob("**/*.cbr"):
                        comics.append(
                            Comic(
                                title=comic_file.stem,
                                file_path=str(comic_file),
                                character=char_dir.name,
                                cover_path=self._find_cover(char_dir, comic_file)
                            )
                        )
        return comics
    
    def _find_cover(self, char_dir: Path, comic_file: Path) -> str:
        """Busca imagen de portada correspondiente"""
        possible_names = [
            f"{comic_file.stem}.jpg",
            f"{comic_file.stem}.png",
            "cover.jpg"
        ]
        
        for name in possible_names:
            cover = char_dir / name
            if cover.exists():
                return str(cover)
        return ""