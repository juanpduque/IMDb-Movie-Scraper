"""Pruebas para el módulo de filtrado de IDs."""

import os
import tempfile
import pandas as pd
import pytest
import sys
from pathlib import Path

# Agregar el directorio raíz al path de Python
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

from src.utils.id_filter import compare_ids, filter_and_save_ids

@pytest.fixture
def sample_data():
    """Crear datos de prueba."""
    # Crear directorio temporal
    temp_dir = tempfile.mkdtemp()
    
    # Crear archivo 1 con IDs
    file1_path = os.path.join(temp_dir, "file1.tsv")
    df1 = pd.DataFrame({
        'tconst': ['tt1', 'tt2', 'tt3', 'tt4'],
        'title': ['Movie1', 'Movie2', 'Movie3', 'Movie4']
    })
    df1.to_csv(file1_path, sep='\t', index=False)
    
    # Crear archivo 2 con IDs
    file2_path = os.path.join(temp_dir, "file2.tsv")
    df2 = pd.DataFrame({
        'tconst': ['tt2', 'tt3', 'tt5'],
        'title': ['Movie2', 'Movie3', 'Movie5']
    })
    df2.to_csv(file2_path, sep='\t', index=False)
    
    # Crear archivo con IDs de reseñas
    reviews_path = os.path.join(temp_dir, "reviews.csv")
    df_reviews = pd.DataFrame({
        'IMDb ID': ['tt2', 'tt3'],
        'count': [10, 15]
    })
    df_reviews.to_csv(reviews_path, sep=',', index=False)
    
    return {
        'file1': file1_path,
        'file2': file2_path,
        'reviews': reviews_path,
        'temp_dir': temp_dir
    }

def test_compare_ids(sample_data):
    """Prueba la función compare_ids."""
    ids1, ids2, difference = compare_ids(
        sample_data['file1'],
        sample_data['file2']
    )
    
    # Verificar resultados
    assert len(ids1) == 4  # Total IDs en file1
    assert len(ids2) == 3  # Total IDs en file2
    assert len(difference) == 2  # IDs únicos en file1
    assert 'tt1' in difference
    assert 'tt4' in difference

def test_filter_and_save_ids_missing(sample_data):
    """Prueba filter_and_save_ids en modo find_missing=True."""
    output_file = os.path.join(sample_data['temp_dir'], "missing.tsv")
    
    filter_and_save_ids(
        source_file=sample_data['file1'],
        filter_file=sample_data['file2'],
        output_file=output_file,
        find_missing=True
    )
    
    # Verificar archivo de salida
    result_df = pd.read_csv(output_file, sep='\t')
    assert len(result_df) == 2
    assert 'tt1' in result_df['tconst'].values
    assert 'tt4' in result_df['tconst'].values

def test_filter_and_save_ids_common(sample_data):
    """Prueba filter_and_save_ids en modo find_missing=False."""
    output_file = os.path.join(sample_data['temp_dir'], "common.tsv")
    
    filter_and_save_ids(
        source_file=sample_data['file1'],
        filter_file=sample_data['file2'],
        output_file=output_file,
        find_missing=False
    )
    
    # Verificar archivo de salida
    result_df = pd.read_csv(output_file, sep='\t')
    assert len(result_df) == 2
    assert 'tt2' in result_df['tconst'].values
    assert 'tt3' in result_df['tconst'].values

def test_filter_and_save_ids_with_reviews(sample_data):
    """Prueba filter_and_save_ids con archivo de reseñas."""
    output_file = os.path.join(sample_data['temp_dir'], "with_reviews.tsv")
    
    filter_and_save_ids(
        source_file=sample_data['file1'],
        filter_file=sample_data['reviews'],
        output_file=output_file,
        filter_id_column="IMDb ID",
        filter_sep=',',
        find_missing=False
    )
    
    # Verificar archivo de salida
    result_df = pd.read_csv(output_file, sep='\t')
    assert len(result_df) == 2
    assert 'tt2' in result_df['tconst'].values
    assert 'tt3' in result_df['tconst'].values

def test_error_handling():
    """Prueba el manejo de errores."""
    with pytest.raises(Exception):
        compare_ids("nonexistent_file1.tsv", "nonexistent_file2.tsv")
    
    with pytest.raises(Exception):
        filter_and_save_ids(
            "nonexistent_file1.tsv",
            "nonexistent_file2.tsv",
            "output.tsv"
        ) 