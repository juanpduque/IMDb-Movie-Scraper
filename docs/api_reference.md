# Referencia de API

## Módulo de Datos

### IMDbDataset
```python
class IMDbDataset:
    def __init__(self, input_file: str)
    def load_data(self) -> pd.DataFrame
    def filter_movies(
        self,
        genre: str = None,
        title_type: str = "movie",
        start_year: int = None,
        end_year: int = None,
        is_adult: bool = False
    ) -> pd.DataFrame
```

### MovieExporter
```python
class MovieExporter:
    def __init__(self, output_folder: str = "movie_data")
    def save_to_csv(
        self,
        dataframe: pd.DataFrame,
        genre: str = None,
        start_year: int = None,
        end_year: int = None
    ) -> None
```

## Módulo de Scraping

### MovieScraperPipeline
```python
class MovieScraperPipeline:
    def __init__(self, driver: WebDriver)
    def run_pipeline(
        self,
        movie_list: pd.DataFrame,
        dataset_name: str = None,
        start_from_id: str = None
    ) -> None
    def scrape_reviews(self, imdb_id: str) -> list[str]
```

### WebDriverManager
```python
class WebDriverManager:
    def __init__(self)
    def setup_driver(self, headless: bool = False) -> WebDriver
    def quit_driver(self) -> None
```

## Módulo de Análisis

### SentimentAnalyzer
```python
class SentimentAnalyzer:
    def __init__(self)
    def analyze_reviews(self, reviews_folder: str) -> pd.DataFrame
    def rank_movies(
        self,
        combined_df: pd.DataFrame,
        emotion_label: str = "fear"
    ) -> pd.DataFrame
```

## Módulo de Utilidades

### ProgressManager
```python
class ProgressManager:
    def __init__(
        self,
        id_filename: str = "last_scraped_id.txt",
        dataset_filename: str = "last_dataset_name.txt",
        sentiment_id_filename: str = "last_sentiment_id.txt"
    )
    def save_progress(
        self,
        last_id: str,
        dataset_name: str,
        sentiment_id: str = None
    ) -> None
    def load_progress(self) -> tuple[str, str, str]
```

## Ejemplos de Uso

### Filtrar y Exportar Películas
```python
from src.data.imdb_dataset import IMDbDataset
from src.data.movie_exporter import MovieExporter

# Cargar y filtrar datos
dataset = IMDbDataset("data/title.basics.tsv")
dataset.load_data()
horror_movies = dataset.filter_movies(genre="Horror")

# Exportar resultados
exporter = MovieExporter()
exporter.save_to_csv(horror_movies, genre="Horror")
```

### Scraping de Reseñas
```python
from src.scrapers.movie_scraper_pipeline import MovieScraperPipeline
from src.scrapers.utils.web_driver_manager import WebDriverManager

# Configurar scraping
web_driver_manager = WebDriverManager()
driver = web_driver_manager.setup_driver()
scraper = MovieScraperPipeline(driver)

# Ejecutar pipeline
scraper.run_pipeline(horror_movies, dataset_name="horror_movies")
```

### Análisis de Sentimientos
```python
from src.analysis.sentiment.sentiment_analyzer import SentimentAnalyzer

# Analizar reseñas
analyzer = SentimentAnalyzer()
results = analyzer.analyze_reviews("reviews_folder")

# Obtener ranking por emoción
scary_movies = analyzer.rank_movies(results, emotion_label="fear")
```

## Manejo de Errores

1. **IMDbDataset**:
   - `FileNotFoundError`: Archivo de entrada no encontrado
   - `ValueError`: Parámetros de filtrado inválidos

2. **MovieScraperPipeline**:
   - `WebDriverException`: Problemas con el navegador
   - `TimeoutException`: Tiempo de espera agotado

3. **SentimentAnalyzer**:
   - `ValueError`: Datos de entrada inválidos
   - `FileNotFoundError`: Archivos no encontrados 