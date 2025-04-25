# Estructura de Datos

## Estructura de Directorios

```
data/
├── title.basics.tsv       # Datos básicos de IMDb
├── movie_data/           # Películas filtradas
│   └── movies_*.csv      # Archivos de películas filtradas
├── reviews/              # Reseñas extraídas
│   └── reviews_*.csv     # Archivos de reseñas por película
└── movie_emotions/       # Análisis de emociones
    └── emotions_*.csv    # Archivos de emociones por película
```

## Formatos de Archivos

### 1. title.basics.tsv
Formato TSV de IMDb con las siguientes columnas:
- `tconst`: ID único de IMDb
- `titleType`: Tipo de título (movie, short, etc.)
- `primaryTitle`: Título principal
- `originalTitle`: Título original
- `isAdult`: Indicador de contenido adulto
- `startYear`: Año de inicio
- `endYear`: Año de fin
- `runtimeMinutes`: Duración en minutos
- `genres`: Géneros separados por comas

### 2. Archivos de Películas Filtradas (CSV)
Formato CSV con las siguientes columnas:
- `imdb_id`: ID de IMDb
- `title`: Título de la película
- `year`: Año de lanzamiento
- `genres`: Géneros separados por comas
- `rating`: Calificación de IMDb
- `votes`: Número de votos

### 3. Archivos de Reseñas (CSV)
Formato CSV con las siguientes columnas:
- `review_id`: ID único de la reseña
- `imdb_id`: ID de la película
- `review_text`: Texto de la reseña
- `rating`: Calificación del usuario
- `date`: Fecha de la reseña

### 4. Archivos de Emociones (CSV)
Formato CSV con las siguientes columnas:
- `imdb_id`: ID de la película
- `review_id`: ID de la reseña
- `emotion`: Emoción detectada
- `score`: Puntuación de la emoción
- `confidence`: Nivel de confianza

## Ejemplos de Datos

### Ejemplo de title.basics.tsv
```tsv
tconst  titleType    primaryTitle    originalTitle    isAdult    startYear    endYear    runtimeMinutes    genres
tt0000001    short    Carmencita    Carmencita    0    1894    \N    1    Documentary,Short
tt0000002    short    Le clown et ses chiens    Le clown et ses chiens    0    1892    \N    5    Animation,Short
```

### Ejemplo de Archivo de Reseñas
```csv
review_id,imdb_id,review_text,rating,date
1,tt0111161,"Excelente película...",10,2023-01-15
2,tt0111161,"Muy buena...",9,2023-01-16
```

### Ejemplo de Archivo de Emociones
```csv
imdb_id,review_id,emotion,score,confidence
tt0111161,1,fear,0.85,0.92
tt0111161,2,joy,0.78,0.89
```

## Consideraciones de Almacenamiento

1. **Formato TSV para Datos Brutos**:
   - Mejor rendimiento para grandes volúmenes
   - Compatibilidad con IMDb

2. **Formato CSV para Datos Procesados**:
   - Fácil de leer y procesar
   - Compatibilidad con herramientas de análisis

3. **Estructura de Directorios**:
   - Separación clara por tipo de dato
   - Fácil navegación y mantenimiento 