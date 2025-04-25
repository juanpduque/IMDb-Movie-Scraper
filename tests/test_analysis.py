import pytest
import pandas as pd
from pathlib import Path
from src.analysis.metrics.balance_score import analyze_scariest_movies_with_review_balance
from src.analysis.metrics.merge_analisis import analyze_scariest_movies
from src.analysis.utils.count_reviews import count_reviews_in_folder
from src.analysis.utils.check_review_data import get_imdb_ids_from_folder
from src.analysis.sentiment.check_emotions_data import get_imdb_ids_from_emotions_folder


# Configuración de rutas de prueba
TEST_ROOT = Path(__file__).parent
TEST_DATA_DIR = TEST_ROOT / "data"
TEST_RAW_DATA_DIR = TEST_DATA_DIR / "raw"
TEST_PROCESSED_DATA_DIR = TEST_DATA_DIR / "processed"


@pytest.fixture
def sample_review_data(tmp_path):
    """Fixture que proporciona datos de prueba para reseñas."""
    review_dir = tmp_path / "reviews"
    review_dir.mkdir()
    
    # Crear archivos de prueba
    df1 = pd.DataFrame({
        'review_text': ['Scary movie!', 'Very frightening'],
        'rating': [8, 9],
        'date': ['2023-01-01', '2023-01-02']
    })
    df1.to_csv(review_dir / "reviews_tt0000001.csv", index=False)
    
    df2 = pd.DataFrame({
        'review_text': ['Not scary', 'Boring'],
        'rating': [3, 2],
        'date': ['2023-01-03', '2023-01-04']
    })
    df2.to_csv(review_dir / "reviews_tt0000002.csv", index=False)
    
    return review_dir


@pytest.fixture
def sample_emotion_data(tmp_path):
    """Fixture que proporciona datos de prueba para emociones."""
    emotion_dir = tmp_path / "emotions"
    emotion_dir.mkdir()
    
    # Crear archivos de prueba
    df1 = pd.DataFrame({
        'Review': ['Scary movie!'],
        'Emotion': ['fear'],
        'Score': [0.9]
    })
    df1.to_csv(emotion_dir / "emotions_tt0000001.csv", index=False)
    
    df2 = pd.DataFrame({
        'Review': ['Not scary'],
        'Emotion': ['neutral'],
        'Score': [0.5]
    })
    df2.to_csv(emotion_dir / "emotions_tt0000002.csv", index=False)
    
    return emotion_dir


def test_count_reviews_in_folder(sample_review_data):
    """Test para la función count_reviews_in_folder."""
    result = count_reviews_in_folder(sample_review_data)
    
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert 'IMDb_ID' in result.columns
    assert 'Review_Count' in result.columns
    assert result['Review_Count'].sum() == 4


def test_get_imdb_ids_from_folder(sample_review_data):
    """Test para la función get_imdb_ids_from_folder."""
    result = get_imdb_ids_from_folder(sample_review_data)
    
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert 'IMDb_ID' in result.columns
    assert set(result['IMDb_ID']) == {'tt0000001', 'tt0000002'}


def test_get_imdb_ids_from_emotions_folder(sample_emotion_data):
    """Test para la función get_imdb_ids_from_emotions_folder."""
    result = get_imdb_ids_from_emotions_folder(sample_emotion_data)
    
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert 'IMDb_ID' in result.columns
    assert set(result['IMDb_ID']) == {'tt0000001', 'tt0000002'}


def test_analyze_scariest_movies(tmp_path):
    """Test para la función analyze_scariest_movies."""
    # Crear archivos de prueba
    score_file = tmp_path / "scores.csv"
    metadata_file = tmp_path / "metadata.csv"
    output_file = tmp_path / "results.csv"
    
    # Crear datos de prueba
    scores_df = pd.DataFrame({
        'imdb_id': ['tt0000001', 'tt0000002'],
        'Average_Score': [8.5, 6.0]
    })
    scores_df.to_csv(score_file, index=False)
    
    metadata_df = pd.DataFrame({
        'imdb_id': ['tt0000001', 'tt0000002'],
        'primaryTitle': ['Scary Movie 1', 'Scary Movie 2'],
        'genres': ['Horror', 'Horror']
    })
    metadata_df.to_csv(metadata_file, index=False)
    
    # Ejecutar análisis
    result = analyze_scariest_movies(score_file, metadata_file, output_file)
    
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert result.iloc[0]['Average_Score'] > result.iloc[1]['Average_Score']


def test_analyze_scariest_movies_with_review_balance(tmp_path):
    """Test para la función analyze_scariest_movies_with_review_balance."""
    # Crear archivos de prueba
    score_file = tmp_path / "scores.csv"
    avg_score_file = tmp_path / "avg_scores.csv"
    metadata_file = tmp_path / "metadata.csv"
    output_file = tmp_path / "results.csv"
    
    # Crear datos de prueba
    scores_df = pd.DataFrame({
        'imdb_id': ['tt0000001', 'tt0000002'],
        'Review_Count': [100, 50]
    })
    scores_df.to_csv(score_file, index=False)
    
    avg_scores_df = pd.DataFrame({
        'imdb_id': ['tt0000001', 'tt0000002'],
        'Average_Score': [8.5, 9.0]
    })
    avg_scores_df.to_csv(avg_score_file, index=False)
    
    metadata_df = pd.DataFrame({
        'imdb_id': ['tt0000001', 'tt0000002'],
        'primaryTitle': ['Scary Movie 1', 'Scary Movie 2'],
        'genres': ['Horror', 'Horror']
    })
    metadata_df.to_csv(metadata_file, index=False)
    
    # Ejecutar análisis
    result = analyze_scariest_movies_with_review_balance(
        score_file, avg_score_file, metadata_file, output_file
    )
    
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert 'Weighted_Score' in result.columns 