import os
from typing import List

def get_files_by_extension(directory: str, extensions: List[str]) -> List[str]:
    """Obtiene archivos por extensión"""
    return [
        os.path.join(root, file)
        for root, _, files in os.walk(directory)
        for file in files
        if file.lower().endswith(tuple(extensions))
    ]