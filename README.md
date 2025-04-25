# IMDb Movie Scraper

Un scraper para extraer y analizar datos de películas de IMDb.

## Estructura del Proyecto

```
IMDb-Movie-Scraper/
├── src/                    # Código fuente principal
│   ├── scrapers/          # Scripts de scraping
│   ├── analysis/          # Scripts de análisis
│   ├── utils/             # Utilidades y funciones auxiliares
│   └── visualization/     # Scripts de visualización
├── data/                  # Datos procesados
│   ├── raw/              # Datos crudos
│   ├── processed/        # Datos procesados
│   └── results/          # Resultados finales
├── logs/                 # Archivos de registro
├── config/              # Archivos de configuración
├── tests/               # Tests unitarios
├── docs/                # Documentación
├── requirements.txt     # Dependencias
└── README.md           # Documentación principal
```

## Instalación

1. Clonar el repositorio
2. Crear un entorno virtual: `python -m venv .venv`
3. Activar el entorno virtual: `source .venv/bin/activate` (Linux/Mac) o `.venv\Scripts\activate` (Windows)
4. Instalar dependencias: `pip install -r requirements.txt`

## Uso

Los scripts principales se encuentran en el directorio `src/`:

- `scrapers/`: Contiene los scripts para extraer datos de IMDb
- `analysis/`: Contiene los scripts para analizar los datos extraídos
- `utils/`: Contiene utilidades y funciones auxiliares
- `visualization/`: Contiene scripts para generar visualizaciones

## Contribución

Las contribuciones son bienvenidas. Por favor, asegúrate de seguir la estructura del proyecto y documentar cualquier cambio significativo.

