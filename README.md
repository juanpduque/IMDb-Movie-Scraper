# IMDb Movie Scraper

Un scraper para extraer y analizar reseñas de películas de IMDb, con enfoque en análisis de sentimientos y emociones.

## Estructura del Proyecto

```
src/
├── scrapers/          # Módulo de scraping
│   ├── utils/         # Utilidades para scraping
│   ├── movie_scraper_pipeline.py
│   ├── numberReviews.py
│   └── main.py
├── data/              # Módulo de manejo de datos
│   ├── imdb_dataset.py
│   └── movie_exporter.py
└── utils/             # Utilidades generales
    └── progress_manager.py
```

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd IMDb-Movie-Scraper
```

2. Crear y activar entorno virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # En Unix/macOS
# o
.venv\Scripts\activate  # En Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso Básico

1. Filtrar películas:
```python
from src.data.imdb_dataset import IMDbDataset

dataset = IMDbDataset("data/title.basics.tsv")
dataset.load_data()
horror_movies = dataset.filter_movies(genre="Horror")
```

2. Scraping de reseñas:
```python
from src.scrapers.movie_scraper_pipeline import MovieScraperPipeline
from src.scrapers.utils.web_driver_manager import WebDriverManager

web_driver_manager = WebDriverManager()
driver = web_driver_manager.setup_driver()
scraper = MovieScraperPipeline(driver)
scraper.run_pipeline(horror_movies)
```

3. Análisis de sentimientos:
```python
from src.analysis.sentiment.sentiment_analyzer import SentimentAnalyzer

analyzer = SentimentAnalyzer()
results = analyzer.analyze_reviews("reviews_folder")
```

## Requisitos

- Python 3.8+
- Chrome/Chromium instalado
- Dependencias listadas en `requirements.txt`

## Documentación Adicional

Para más detalles sobre la arquitectura, estructura de datos y API, consulta la documentación en la carpeta `docs/`:

- [Arquitectura](docs/architecture.md)
- [Estructura de Datos](docs/data_structure.md)
- [Referencia de API](docs/api_reference.md) 