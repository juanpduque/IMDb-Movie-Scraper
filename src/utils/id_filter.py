"""
Módulo para el filtrado y comparación de IDs de películas.
Proporciona funciones unificadas para manejar diferentes casos de filtrado de IDs.
"""

import pandas as pd
from typing import Set, Tuple
import logging
import os

def compare_ids(
    file1: str,
    file2: str,
    id_column1: str = 'tconst',
    id_column2: str = 'tconst',
    sep1: str = '\t',
    sep2: str = '\t'
) -> Tuple[Set[str], Set[str], Set[str]]:
    """
    Compara IDs entre dos archivos y retorna los conjuntos de IDs únicos y su diferencia.
    
    Args:
        file1: Ruta al primer archivo de IDs
        file2: Ruta al segundo archivo de IDs
        id_column1: Nombre de la columna de ID en el primer archivo
        id_column2: Nombre de la columna de ID en el segundo archivo
        sep1: Separador del primer archivo
        sep2: Separador del segundo archivo
    
    Returns:
        Tuple con:
        - IDs únicos del primer archivo
        - IDs únicos del segundo archivo
        - IDs que están en el primer archivo pero no en el segundo
    """
    try:
        # Leer los archivos
        df1 = pd.read_csv(file1, sep=sep1, dtype=str)
        df2 = pd.read_csv(file2, sep=sep2, dtype=str)
        
        # Extraer IDs únicos
        ids1 = set(df1[id_column1].str.strip().unique())
        ids2 = set(df2[id_column2].str.strip().unique())
        
        # Calcular diferencia
        difference = ids1 - ids2
        
        logging.info(f"Total IDs en {file1}: {len(ids1)}")
        logging.info(f"Total IDs en {file2}: {len(ids2)}")
        logging.info(f"IDs únicos en {file1} pero no en {file2}: {len(difference)}")
        
        return ids1, ids2, difference
        
    except Exception as e:
        logging.error(f"Error al comparar IDs: {e}")
        raise

def filter_and_save_ids(
    source_file: str,
    filter_file: str,
    output_file: str = None,
    source_id_column: str = 'tconst',
    filter_id_column: str = 'tconst',
    source_sep: str = '\t',
    filter_sep: str = '\t',
    find_missing: bool = True
) -> None:
    """
    Filtra IDs de un archivo fuente basado en un archivo de filtro y guarda el resultado.
    
    Args:
        source_file: Archivo fuente con los IDs a filtrar
        filter_file: Archivo con los IDs de filtro
        output_file: Archivo donde guardar los resultados. Si es None, se genera automáticamente
        source_id_column: Columna de ID en el archivo fuente
        filter_id_column: Columna de ID en el archivo de filtro
        source_sep: Separador del archivo fuente
        filter_sep: Separador del archivo de filtro
        find_missing: Si True, encuentra IDs en source pero no en filter.
                     Si False, encuentra IDs que están en ambos.
    """
    try:
        # Leer los archivos
        source_df = pd.read_csv(source_file, sep=source_sep, dtype=str)
        filter_df = pd.read_csv(filter_file, sep=filter_sep, dtype=str)
        
        # Extraer IDs
        source_ids = set(source_df[source_id_column].str.strip())
        filter_ids = set(filter_df[filter_id_column].str.strip())
        
        # Filtrar según el modo
        if find_missing:
            filtered_ids = source_ids - filter_ids
            logging.info(f"Encontrados {len(filtered_ids)} IDs en {source_file} que no están en {filter_file}")
        else:
            filtered_ids = source_ids.intersection(filter_ids)
            logging.info(f"Encontrados {len(filtered_ids)} IDs comunes entre {source_file} y {filter_file}")
        
        # Si no se especifica output_file, generar uno automáticamente
        if output_file is None:
            source_name = os.path.basename(source_file).split('.')[0]
            filter_name = os.path.basename(filter_file).split('.')[0]
            output_file = os.path.join(
                "data/processed/id_differences",
                f"difference_{source_name}_vs_{filter_name}.tsv"
            )
        
        # Asegurar que el directorio existe
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Crear y guardar DataFrame con resultados
        result_df = pd.DataFrame(list(filtered_ids), columns=[source_id_column])
        result_df.to_csv(output_file, sep='\t', index=False)
        logging.info(f"Resultados guardados en {output_file}")
        
    except Exception as e:
        logging.error(f"Error al filtrar y guardar IDs: {e}")
        raise

def main():
    """Ejemplo de uso de las funciones de filtrado."""
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Ejemplo 1: Encontrar películas sin reseñas
    filter_and_save_ids(
        source_file="data/title_types/movie.tsv",
        filter_file="data/unique_review_counts.csv",
        output_file="data/movies_without_reviews.tsv",
        filter_id_column="IMDb ID",
        find_missing=True
    )
    
    # Ejemplo 2: Encontrar películas con reseñas
    filter_and_save_ids(
        source_file="data/title_types/movie.tsv",
        filter_file="data/unique_review_counts.csv",
        output_file="data/movies_with_reviews.tsv",
        filter_id_column="IMDb ID",
        find_missing=False
    )

if __name__ == "__main__":
    main() 