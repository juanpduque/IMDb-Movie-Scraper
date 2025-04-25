import os
import pandas as pd
import pytest
from pathlib import Path
from src.analysis.sentiment.sentiment_analyzer import SentimentAnalyzer

# Configuración de rutas de prueba
TEST_ROOT = Path(__file__).parent
TEST_DATA_DIR = TEST_ROOT / "data"
TEST_RAW_DATA_DIR = TEST_DATA_DIR / "raw"
TEST_REVIEWS_DIR = TEST_RAW_DATA_DIR / "reviews"

@pytest.fixture
def analyzer():
    """Fixture que proporciona una instancia de SentimentAnalyzer."""
    return SentimentAnalyzer(device=-1)  # Usar CPU para pruebas

@pytest.fixture
def sample_reviews():
    """Fixture que proporciona datos de prueba para reseñas."""
    return pd.DataFrame({
        'Review': [
            "This movie was absolutely terrifying!",
            "I couldn't sleep after watching this.",
            "Not scary at all, very disappointing.",
            "The atmosphere was creepy and unsettling.",
            "A masterpiece of horror cinema."
        ]
    })

def test_analyze_file(analyzer, tmp_path):
    """Test para la función analyze_file."""
    # Crear archivo de prueba
    test_file = tmp_path / "test_reviews.csv"
    sample_reviews = pd.DataFrame({
        'Review': ["This movie was absolutely terrifying!"]
    })
    sample_reviews.to_csv(test_file, index=False)
    
    # Crear directorio de salida
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    
    # Ejecutar análisis
    analyzer.analyze_file(test_file, output_dir)
    
    # Verificar que se creó el archivo de salida
    output_files = list(output_dir.glob("*.csv"))
    assert len(output_files) == 1
    
    # Verificar contenido del archivo de salida
    output_df = pd.read_csv(output_files[0])
    assert 'Review' in output_df.columns
    assert 'Emotion' in output_df.columns
    assert 'Score' in output_df.columns

def test_aggregate_results(analyzer, tmp_path):
    """Test para la función aggregate_results."""
    # Crear archivos de prueba
    test_dir = tmp_path / "test_emotions"
    test_dir.mkdir()
    
    # Crear dos archivos de emociones
    emotions1 = pd.DataFrame({
        'Review': ["Scary movie!"],
        'Emotion': ["fear"],
        'Score': [0.9]
    })
    emotions1.to_csv(test_dir / "emotions_tt0000001.csv", index=False)
    
    emotions2 = pd.DataFrame({
        'Review': ["Not scary"],
        'Emotion': ["neutral"],
        'Score': [0.5]
    })
    emotions2.to_csv(test_dir / "emotions_tt0000002.csv", index=False)
    
    # Ejecutar agregación
    result = analyzer.aggregate_results(test_dir)
    
    # Verificar resultados
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert 'imbd_id' in result.columns

def test_rank_movies(analyzer):
    """Test para la función rank_movies."""
    # Crear datos de prueba
    test_data = pd.DataFrame({
        'imbd_id': ['tt0000001', 'tt0000001', 'tt0000002'],
        'Emotion': ['fear', 'fear', 'neutral'],
        'Score': [0.9, 0.8, 0.5]
    })
    
    # Ejecutar ranking
    result = analyzer.rank_movies(test_data, emotion_label="fear")
    
    # Verificar resultados
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1  # Solo una película con emoción "fear"
    assert result.iloc[0]['Average_Score'] > 0.8  # Score promedio debería ser alto

def test_error_handling(analyzer, tmp_path):
    """Test para el manejo de errores."""
    # Intentar analizar un archivo que no existe
    with pytest.raises(Exception):
        analyzer.analyze_file("non_existent_file.csv", tmp_path)
    
    # Intentar agregar resultados de un directorio vacío
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    result = analyzer.aggregate_results(empty_dir)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0 