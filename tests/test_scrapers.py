import pytest
import pandas as pd
from pathlib import Path
from src.data.imdb_dataset import IMDbDataset
from src.scrapers.numberReviews import get_reviews_count, scrape_review


# Configuración de rutas de prueba
TEST_ROOT = Path(__file__).parent
TEST_DATA_DIR = TEST_ROOT / "data"
TEST_RAW_DATA_DIR = TEST_DATA_DIR / "raw"
TEST_MOVIE_DATA_DIR = TEST_RAW_DATA_DIR / "movie_data"


@pytest.fixture
def sample_movie_data(tmp_path):
    """Fixture que proporciona datos de prueba para películas."""
    test_file = tmp_path / "test_movies.tsv"
    df = pd.DataFrame({
        'tconst': ['tt0000001', 'tt0000002', 'tt0000003'],
        'titleType': ['movie', 'movie', 'movie'],
        'primaryTitle': ['Test Movie 1', 'Test Movie 2', 'Test Movie 3'],
        'genres': ['Action', 'Horror', 'Comedy']
    })
    df.to_csv(test_file, sep='\t', index=False)
    return test_file


def test_filter_movies(sample_movie_data):
    """Test para la función filter_movies de IMDbDataset."""
    # Crear instancia de IMDbDataset
    dataset = IMDbDataset(sample_movie_data)
    dataset.load_data()
    
    # Filtrar por género
    filtered_movies = dataset.filter_movies(genre="Horror")
    
    # Verificar resultados
    assert len(filtered_movies) == 1
    assert filtered_movies.iloc[0]['tconst'] == 'tt0000002'
    assert filtered_movies.iloc[0]['genres'] == 'Horror'


def test_get_reviews_count():
    """Test para la función get_reviews_count."""
    # Este test asume que tenemos acceso a IMDb
    # En un entorno real, deberíamos mockear las llamadas a la API
    imdb_id = "tt0111161"  # The Shawshank Redemption
    count = get_reviews_count(imdb_id)
    
    # Verificar que el resultado es un número
    assert isinstance(count, int)
    assert count >= 0


def test_scrape_review(tmp_path):
    """Test para la función scrape_review."""
    output_file = tmp_path / "reviews.csv"
    imdb_id = "tt0111161"  # The Shawshank Redemption
    
    # Ejecutar scraping
    result = scrape_review(imdb_id, output_file)
    
    # Verificar que se creó el archivo
    assert output_file.exists()
    
    # Verificar que el resultado es el IMDb ID
    assert result == imdb_id


def test_error_handling(tmp_path):
    """Test para el manejo de errores en las funciones de scraping."""
    # Test para extract_id_column con archivo inexistente
    with pytest.raises(Exception):
        extract_id_column("non_existent_file.tsv", tmp_path / "output.tsv")
    
    # Test para get_reviews_count con ID inválido
    invalid_count = get_reviews_count("invalid_id")
    assert invalid_count == 0  # Debería retornar 0 para IDs inválidos 