# BIG DATA CLEANING GOD LAB

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Docker%20Compose-1D63ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Compose">
  <img src="https://img.shields.io/badge/Big%20Data%20Cleaning-111111?style=for-the-badge" alt="Big Data Cleaning">
</p>

---

## Descripcion

**BIG DATA CLEANING GOD LAB** es un laboratorio de ingenieria de datos para generar y limpiar grandes volumenes de informacion transaccional con errores reales: duplicados, datos faltantes, emails mal formateados y valores atipicos.

El proyecto esta diseñado para ser:

- **Professional**: Flujo ETL reproducible con validaciones de calidad
- **Modular**: Generacion, limpieza y reporte separados por componentes
- **Escalable**: Procesamiento por lotes para millones de filas
- **Listo para produccion**: Docker, pruebas y salida analitica verificable

---

## Arquitectura del Sistema

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                     BIG DATA CLEANING GOD LAB                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                  │
│   │ Data        │────▶│ Python ETL  │────▶│  Curated    │                  │
│   │ Generator   │     │  Cleaner    │     │ SQLite/CSV  │                  │
│   │ (Raw CSV)   │     │ (Rules+DQ)  │     │   Layer     │                  │
│   └─────────────┘     └──────┬──────┘     └──────┬──────┘                  │
│                              │                    │                         │
│                              ▼                    ▼                         │
│                     ┌────────────────┐    ┌────────────────┐                │
│                     │ Quality Report │    │ Segment Metrics│                │
│                     │    JSON        │    │  Country/Chan  │                │
│                     └────────────────┘    └────────────────┘                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Flujo de Datos

1. **Extract/Generate**: Se generan CSV crudos con datos sucios simulando produccion real.
2. **Transform/Clean**: Se normaliza texto, fechas, cantidades y correos.
3. **Deduplicate**: Se elimina duplicidad por `event_id` con clave unica en SQLite.
4. **Load Curated**: Se persiste dataset curado en `curated.db` y `curated_events.csv`.
5. **Analyze**: Se calculan top segmentos de revenue por pais/canal y calidad final.

---

## Stack Tecnologico

| Componente | Version | Descripcion |
|------------|---------|-------------|
| Python | 3.11+ | Motor principal del pipeline |
| SQLite | stdlib | Curado, deduplicacion y analitica SQL |
| Docker | latest | Contenerizacion del flujo |
| Docker Compose | latest | Orquestacion local |
| unittest | stdlib | Test end-to-end del pipeline |

---

## Estructura del Proyecto

```text
Proyectos/
│
├── docker-compose.yml                 # Orquestacion del servicio
├── Dockerfile                         # Imagen de ejecucion del pipeline
├── main.py                            # CLI principal (generate/clean/run-all)
├── requirements.txt                   # Dependencias (stdlib only)
│
├── src/
│   └── bigdata_god/
│       ├── generator.py               # Generador de datos sucios a gran escala
│       └── pipeline.py                # Limpieza, deduplicacion y reporte
│
├── tests/
│   └── test_pipeline_smoke.py         # Prueba de humo end-to-end
│
├── data/
│   ├── raw/                           # Archivos crudos generados
│   └── curated/                       # curated.db y curated_events.csv
│
└── reports/
    └── quality_report.json            # Reporte final de calidad
```

---

## Requisitos Previos

- Docker Engine 20.10+
- Docker Compose 2.0+
- Python 3.11+ (si ejecutas sin Docker)
- 4GB RAM disponibles
- 5GB espacio en disco

---

## Instalacion y Configuracion

### 1. Clonar el repositorio

```bash
git clone https://github.com/ieharo1/Proyectos.git
cd Proyectos
```

### 2. Ejecutar en local (sin Docker)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py run-all --rows 1000000 --partitions 20
```

### 3. Ejecutar con Docker

```bash
docker compose up --build
```

---

## Uso del Pipeline

### Como funciona (paso a paso)

1. `generate` crea particiones CSV con ruido de calidad de datos.
2. `clean` aplica validaciones y normalizaciones de negocio.
3. Se inserta en SQLite con `INSERT OR IGNORE` para deduplicar.
4. Se exporta capa curada a CSV para consumo externo.
5. Se genera `quality_report.json` con KPIs de limpieza.

### Comandos principales

```bash
# Flujo completo
python main.py run-all --rows 1000000 --partitions 20

# Solo generacion de datos sucios
python main.py generate --output data/raw --rows 3000000 --partitions 36

# Solo limpieza y reporte
python main.py clean --input-glob "data/raw/*.csv" --curated data/curated --report reports/quality_report.json
```

---

## Verificar que Todo Funciona

```bash
# Test de humo end-to-end
python -m unittest discover -s tests -p "test_*.py" -v

# Ver artefactos generados
dir data\curated
type reports\quality_report.json
```

Se considera correcto cuando:

- `quality_report.json` existe y muestra `raw_rows > 0`
- `curated_rows > 0`
- existe `data/curated/curated.db`
- existe `data/curated/curated_events.csv`

---

## Solucion de Problemas

### Docker no levanta

```bash
docker compose logs
docker compose down
docker compose up --build
```

### No aparecen archivos curados

1. Verifica que existan archivos en `data/raw`.
2. Ejecuta `python main.py clean --input-glob "data/raw/*.csv"`.
3. Revisa `reports/quality_report.json` para confirmar filas procesadas.

---

## Desarrollado por Isaac Esteban Haro Torres

**Ingeniero en Sistemas · Full Stack · Automatización · Data**

-  Email: zackharo1@gmail.com
-  WhatsApp: 098805517
-  GitHub: https://github.com/ieharo1
-  Portafolio: https://ieharo1.github.io/portafolio-isaac.haro/

---

## Licencia

© 2026 Isaac Esteban Haro Torres - Todos los derechos reservados.

---
