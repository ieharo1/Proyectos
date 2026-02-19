# BIGDATA GOD CLEANING

Proyecto de ingeniería de datos **nivel portafolio profesional** para limpieza masiva de datos sucios con Python y Docker.

## Objetivo

Simular un entorno real de Big Data:

- Generar millones de eventos transaccionales con ruido, nulos, outliers y duplicados.
- Limpiar y normalizar datos en procesamiento por lotes de alta escala.
- Guardar dataset curado en SQLite + CSV.
- Crear reporte automático de calidad y segmentos top de negocio.

## Stack técnico

- Python 3.12
- SQLite (curado + deduplicación con índice único)
- CSV por lotes + agregaciones SQL
- Docker + Docker Compose
- Unittest (test de humo end-to-end)

## Arquitectura funcional

1. `generate`: crea datos sintéticos sucios en múltiples CSV.
2. `clean`: aplica reglas robustas de calidad:
   - normalización de texto y emails
   - parseo estricto de timestamps
   - eliminación de registros inválidos
   - deduplicación por `event_id` (clave única en SQLite)
   - control de outliers y rangos inválidos
3. `run-all`: flujo completo de punta a punta.
4. reporte JSON con:
   - filas crudas vs curadas
   - ratio de depuración
   - top 10 segmentos país/canal por revenue

## Estructura

```text
bigdata-god-cleaning/
  main.py
  requirements.txt
  Dockerfile
  docker-compose.yml
  src/bigdata_god/
    generator.py
    pipeline.py
  tests/
    test_pipeline_smoke.py
```

## Ejecución local

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py run-all --rows 1000000 --partitions 20
```

Salida esperada:

- `data/curated/curated.db`
- `data/curated/curated_events.csv`
- `reports/quality_report.json`

## Ejecución con Docker

```bash
docker compose up --build
```

## Test automático

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## Ejemplos de comandos potentes

```bash
python main.py generate --rows 5000000 --partitions 60
python main.py clean --input-glob "data/raw/*.csv" --curated data/curated --report reports/quality_report.json
python main.py run-all --rows 3000000 --partitions 36
```

## Autor y derechos

- Autor: **Nabetse**
- Propiedad intelectual: **Todos los derechos reservados por Nabetse.**
- Uso de este proyecto: requiere autorización explícita del autor.

---

Proyecto diseñado para demostrar capacidades reales de:

- Data Engineering
- Data Quality
- Procesamiento distribuido
- Diseño reproducible con Docker
