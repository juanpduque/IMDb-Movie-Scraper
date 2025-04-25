from pathlib import Path

# Obtener el directorio raíz de las pruebas
TEST_ROOT = Path(__file__).parent.parent

# Rutas de datos de prueba
TEST_DATA_DIR = TEST_ROOT / "data"
TEST_RAW_DATA_DIR = TEST_DATA_DIR / "raw"
TEST_PROCESSED_DATA_DIR = TEST_DATA_DIR / "processed"
TEST_RESULTS_DIR = TEST_DATA_DIR / "results"

# Rutas de archivos de prueba específicos
TEST_MOVIE_DATA_DIR = TEST_RAW_DATA_DIR / "movie_data"
TEST_REVIEWS_DIR = TEST_RAW_DATA_DIR / "reviews"
TEST_MOVIE_EMOTIONS_DIR = TEST_RAW_DATA_DIR / "movie_emotions"

# Crear directorios si no existen
for directory in [TEST_DATA_DIR, TEST_RAW_DATA_DIR, TEST_PROCESSED_DATA_DIR, 
                 TEST_RESULTS_DIR, TEST_MOVIE_DATA_DIR, TEST_REVIEWS_DIR, 
                 TEST_MOVIE_EMOTIONS_DIR]:
    directory.mkdir(parents=True, exist_ok=True) 