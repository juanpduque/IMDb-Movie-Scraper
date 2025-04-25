import pytest
import pandas as pd
from pathlib import Path
import os
from src.data.imdb_dataset import IMDbDataset

# Definir rutas de prueba
TEST_MOVIE_DATA_DIR = Path("test_data/movies")
TEST_REVIEWS_DIR = Path("test_data/reviews")
TEST_PROCESSED_DATA_DIR = Path("test_data/processed")
TEST_RESULTS_DIR = Path("test_data/results")

def test_data_loading():
    """Test that data loading works correctly."""
    # Create test data
    test_data = pd.DataFrame({
        'tconst': ['tt1', 'tt2', 'tt3'],
        'primaryTitle': ['Movie1', 'Movie2', 'Movie3'],
        'startYear': [2000, 2001, 2002],
        'genres': ['Action', 'Comedy', 'Drama']
    })
    
    # Save test data
    test_data.to_csv('test_data.tsv', sep='\t', index=False)
    
    # Test loading
    dataset = IMDbDataset('test_data.tsv')
    loaded_data = dataset.load_data()
    
    # Clean up
    os.remove('test_data.tsv')
    
    # Verify data was loaded correctly
    assert not loaded_data.empty
    assert len(loaded_data) == 3
    assert list(loaded_data.columns) == [
        'tconst', 'primaryTitle', 'startYear', 'genres'
    ]

def test_directory_structure():
    """Test that the pipeline creates the correct directory structure."""
    # Create test directories
    test_dirs = ['raw_data', 'processed_data', 'results']
    for dir_name in test_dirs:
        os.makedirs(dir_name, exist_ok=True)
    
    # Verify directories exist
    for dir_name in test_dirs:
        assert os.path.exists(dir_name)
        assert os.path.isdir(dir_name)
    
    # Clean up
    for dir_name in test_dirs:
        os.rmdir(dir_name)

if __name__ == "__main__":
    test_data_loading()
    test_directory_structure() 