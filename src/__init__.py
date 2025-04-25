# src/__init__.py

# Importing classes for easier access when using the package
from .data.imdb_dataset import IMDbDataset
from .data.movie_exporter import MovieExporter
from .scrapers.movie_scraper_pipeline import MovieScraperPipeline
from .scrapers.utils.web_driver_manager import WebDriverManager

__all__ = [
    'IMDbDataset',
    'MovieExporter',
    'MovieScraperPipeline',
    'WebDriverManager'
]
