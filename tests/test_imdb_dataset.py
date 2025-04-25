import pytest
import pandas as pd
from src.data.imdb_dataset import IMDbDataset


@pytest.fixture
def sample_data():
    """Fixture que proporciona datos de prueba."""
    return pd.DataFrame({
        'tconst': ['tt0000001', 'tt0000002', 'tt0000003'],
        'titleType': ['movie', 'tvSeries', 'movie'],
        'primaryTitle': ['Movie 1', 'Series 1', 'Movie 2']
    })


@pytest.fixture
def dataset_file(tmp_path, sample_data):
    """Fixture que proporciona un archivo de dataset temporal."""
    file_path = tmp_path / "test_dataset.tsv"
    sample_data.to_csv(file_path, sep='\t', index=False)
    return file_path


@pytest.fixture
def imdb_dataset(dataset_file):
    """Fixture que proporciona una instancia de IMDbDataset."""
    dataset = IMDbDataset(dataset_file)
    return dataset


def test_init():
    """Test del constructor."""
    dataset = IMDbDataset("test_file.tsv")
    assert dataset.input_file == "test_file.tsv"
    assert dataset.data is None


def test_load_data_success(imdb_dataset, sample_data):
    """Test de carga exitosa de datos."""
    imdb_dataset.load_data()
    assert imdb_dataset.data is not None
    pd.testing.assert_frame_equal(imdb_dataset.data, sample_data)


def test_load_data_failure():
    """Test de carga fallida de datos."""
    dataset = IMDbDataset("nonexistent_file.tsv")
    dataset.load_data()
    assert dataset.data is None


def test_filter_data_success(imdb_dataset, sample_data):
    """Test de filtrado exitoso de datos."""
    imdb_dataset.load_data()
    filtered = imdb_dataset.filter_data('titleType', 'movie')
    
    expected = sample_data[sample_data['titleType'] == 'movie']
    pd.testing.assert_frame_equal(filtered, expected)


def test_filter_data_no_matches(imdb_dataset):
    """Test de filtrado sin coincidencias."""
    imdb_dataset.load_data()
    filtered = imdb_dataset.filter_data('titleType', 'nonexistent')
    assert len(filtered) == 0


def test_filter_data_no_data(imdb_dataset):
    """Test de filtrado sin datos cargados."""
    filtered = imdb_dataset.filter_data('titleType', 'movie')
    assert filtered is None 