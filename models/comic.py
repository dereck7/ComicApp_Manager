from dataclasses import dataclass
from typing import Optional

@dataclass
class Comic:
    title: str
    file_path: str
    character: str
    cover_path: Optional[str] = None
    read: bool = False
    rating: int = 0

    def get_cover_or_default(self, default: str = "") -> str:
        """Devuelve la portada o una imagen por defecto"""
        return self.cover_path if self.cover_path else default