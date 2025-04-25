# Arquitectura del Sistema

## Diagrama de Componentes

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  IMDb Dataset   │────▶│  Movie Scraper  │────▶│ Sentiment       │
│                 │     │                 │     │  Analyzer       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Movie Exporter │     │  Web Driver     │     │  Progress       │
│                 │     │  Manager        │     │  Manager        │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Flujo de Datos

1. **Extracción de Datos**:
   - `IMDbDataset` carga y filtra datos de IMDb
   - `MovieExporter` guarda los datos filtrados

2. **Scraping**:
   - `WebDriverManager` configura el navegador
   - `MovieScraperPipeline` extrae reseñas
   - `ProgressManager` registra el progreso

3. **Análisis**:
   - `SentimentAnalyzer` procesa las reseñas
   - Genera análisis de emociones
   - Guarda resultados

## Módulos Principales

### 1. Módulo de Datos (`src/data/`)
- **IMDbDataset**: Manejo y filtrado de datos de IMDb
- **MovieExporter**: Exportación de datos a archivos

### 2. Módulo de Scraping (`src/scrapers/`)
- **MovieScraperPipeline**: Pipeline principal de scraping
- **WebDriverManager**: Gestión del navegador
- **Utils**: Utilidades para scraping

### 3. Módulo de Análisis (`src/analysis/`)
- **SentimentAnalyzer**: Análisis de sentimientos
- **Metrics**: Cálculo de métricas
- **Utils**: Utilidades de análisis

### 4. Módulo de Utilidades (`src/utils/`)
- **ProgressManager**: Gestión del progreso
- Otras utilidades generales

## Decisiones de Diseño

1. **Separación de Responsabilidades**:
   - Cada módulo tiene una responsabilidad clara
   - Las utilidades están separadas por contexto

2. **Manejo de Estado**:
   - `ProgressManager` centraliza el seguimiento
   - Estado persistente entre ejecuciones

3. **Extensibilidad**:
   - Módulos independientes
   - Fácil de agregar nuevas funcionalidades

## Consideraciones de Rendimiento

1. **Scraping**:
   - Modo headless para mejor rendimiento
   - Manejo de errores y reintentos

2. **Procesamiento**:
   - Procesamiento por lotes
   - Guardado incremental

3. **Almacenamiento**:
   - Archivos TSV para datos brutos
   - CSV para datos procesados 