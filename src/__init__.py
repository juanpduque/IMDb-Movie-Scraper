# src/__init__.py

# Importing classes for easier access when using the package
from .imdb_dataset import IMDbDataset
from .movie_exporter import MovieExporter
from .movie_scraper_pipeline import MovieScraperPipeline
from .web_driver_manager import WebDriverManager

__all__ = [
    'IMDbDataset',
    'MovieExporter',
    'MovieScraperPipeline',
    'WebDriverManager'
]
