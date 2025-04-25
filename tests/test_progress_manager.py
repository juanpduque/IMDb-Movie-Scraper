import os
import pytest
from src.utils.progress_manager import ProgressManager


@pytest.fixture
def temp_progress_files(tmp_path):
    """Fixture que proporciona archivos temporales para las pruebas."""
    return {
        'id_file': str(tmp_path / "last_scraped_id.txt"),
        'dataset_file': str(tmp_path / "last_dataset_name.txt"),
        'sentiment_file': str(tmp_path / "last_sentiment_id.txt")
    }


@pytest.fixture
def progress_manager(temp_progress_files):
    """Fixture que proporciona una instancia de ProgressManager."""
    return ProgressManager(
        id_filename=temp_progress_files['id_file'],
        dataset_filename=temp_progress_files['dataset_file'],
        sentiment_id_filename=temp_progress_files['sentiment_file']
    )


def test_save_progress_basic(progress_manager):
    """Test básico de guardado de progreso."""
    progress_manager.save_progress("tt0000001", "test_dataset")
    
    # Verificar que los archivos existen
    assert os.path.exists(progress_manager.id_filename)
    assert os.path.exists(progress_manager.dataset_filename)
    
    # Verificar contenido
    with open(progress_manager.id_filename, 'r') as f:
        assert f.read().strip() == "tt0000001"
    with open(progress_manager.dataset_filename, 'r') as f:
        assert f.read().strip() == "test_dataset"


def test_save_progress_with_sentiment(progress_manager):
    """Test de guardado incluyendo ID de sentimiento."""
    progress_manager.save_progress(
        "tt0000001",
        "test_dataset",
        sentiment_id="tt0000002"
    )
    
    # Verificar archivo de sentimiento
    assert os.path.exists(progress_manager.sentiment_id_filename)
    with open(progress_manager.sentiment_id_filename, 'r') as f:
        assert f.read().strip() == "tt0000002"


def test_load_progress_no_files(progress_manager):
    """Test de carga cuando no existen archivos."""
    last_id, dataset_name, sentiment_id = progress_manager.load_progress()
    assert last_id is None
    assert dataset_name is None
    assert sentiment_id is None


def test_load_progress_with_data(progress_manager):
    """Test de carga con datos existentes."""
    # Guardar datos primero
    progress_manager.save_progress(
        "tt0000001",
        "test_dataset",
        sentiment_id="tt0000002"
    )
    
    # Cargar y verificar
    last_id, dataset_name, sentiment_id = progress_manager.load_progress()
    assert last_id == "tt0000001"
    assert dataset_name == "test_dataset"
    assert sentiment_id == "tt0000002"


def test_read_file_nonexistent(progress_manager):
    """Test de lectura de archivo inexistente."""
    result = progress_manager._read_file("nonexistent_file.txt")
    assert result is None 