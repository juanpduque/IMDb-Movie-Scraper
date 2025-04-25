import os
from pathlib import Path

# Obtener el directorio raíz del proyecto
ROOT_DIR = Path(__file__).parent.parent

# Rutas de datos
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
RESULTS_DIR = DATA_DIR / "results"

# Rutas de logs
LOGS_DIR = ROOT_DIR / "logs"

# Rutas de archivos específicos
MOVIE_DATA_DIR = RAW_DATA_DIR / "movie_data"
REVIEWS_DIR = RAW_DATA_DIR / "reviews"
MOVIE_EMOTIONS_DIR = RAW_DATA_DIR / "movie_emotions"

# Crear directorios si no existen
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, RESULTS_DIR, 
                 LOGS_DIR, MOVIE_DATA_DIR, REVIEWS_DIR, MOVIE_EMOTIONS_DIR]:
    directory.mkdir(parents=True, exist_ok=True) 