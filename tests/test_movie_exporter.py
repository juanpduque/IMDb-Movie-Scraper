import os
import pytest
import pandas as pd
from src.data.movie_exporter import MovieExporter


@pytest.fixture
def sample_data():
    """Fixture que proporciona datos de prueba."""
    return pd.DataFrame({
        "title": ["Movie1", "Movie2", "Movie3"],
        "genre": ["Action", "Comedy", "Drama"],
        "year": [2001, 2002, 2003]
    })


@pytest.fixture
def exporter(tmp_path):
    """Fixture que proporciona una instancia de MovieExporter."""
    output_folder = tmp_path / "movie_data"
    return MovieExporter(output_folder=str(output_folder))


def test_init_creates_output_folder(tmp_path):
    """Test que verifica que el constructor crea el directorio de salida."""
    output_folder = tmp_path / "movie_data"
    MovieExporter(output_folder=str(output_folder))
    assert output_folder.exists()
    assert output_folder.is_dir()


def test_save_to_csv_basic(exporter, sample_data):
    """Test básico de guardado de datos."""
    exporter.save_to_csv(sample_data)
    output_file = os.path.join(exporter.output_folder, "movies.csv")
    assert os.path.exists(output_file)
    
    # Verificar contenido
    saved_data = pd.read_csv(output_file)
    pd.testing.assert_frame_equal(saved_data, sample_data)


def test_save_to_csv_with_filters(exporter, sample_data):
    """Test de guardado con filtros de género y años."""
    exporter.save_to_csv(
        sample_data,
        genre="Action",
        start_year=2000,
        end_year=2005
    )
    expected_filename = "movies_genre_Action_start_2000_end_2005.csv"
    output_file = os.path.join(exporter.output_folder, expected_filename)
    assert os.path.exists(output_file)


def test_save_empty_dataframe(exporter):
    """Test que verifica el comportamiento con un DataFrame vacío."""
    empty_df = pd.DataFrame()
    exporter.save_to_csv(empty_df)
    
    # Verificar que no se creó ningún archivo
    assert len(os.listdir(exporter.output_folder)) == 0


def test_save_with_special_characters(exporter, sample_data):
    """Test que verifica el manejo de caracteres especiales."""
    exporter.save_to_csv(sample_data, genre="Sci-Fi/Horror")
    expected_filename = "movies_genre_Sci-Fi_Horror.csv"
    output_file = os.path.join(exporter.output_folder, expected_filename)
    assert os.path.exists(output_file) 