# BIG DATA QUALITY ENGINE

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Data%20Quality-Pipeline-black?style=for-the-badge" alt="Data Quality">
  <img src="https://img.shields.io/badge/ETL-Batch%20Processing-0A7E8C?style=for-the-badge" alt="ETL Batch">
</p>

---

## Descripcion

**BIG DATA QUALITY ENGINE** es un proyecto de ingeniería de datos enfocado en limpieza masiva y curación de eventos transaccionales. El sistema genera datasets grandes con ruido realista, ejecuta reglas de calidad en lotes, deduplica registros por clave de negocio y produce artefactos listos para analítica.

Este laboratorio está orientado a portafolio profesional en Big Data porque demuestra:

- Diseño ETL reproducible de punta a punta.
- Control de calidad de datos con reglas explícitas.
- Procesamiento de alto volumen en particiones CSV.
- Persistencia curada para explotación analítica.

---

## Arquitectura

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                        BIG DATA QUALITY ENGINE                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Generator CLI           Cleaner Pipeline             Curated Layer          │
│  (main.py generate)      (main.py clean)             (SQLite + CSV + JSON)  │
│                                                                              │
│  raw_events_*.csv  ───▶  Normalization Rules  ───▶   data/curated/curated.db│
│                          Type Validation              data/curated/*.csv     │
│                          Dedup by event_id            reports/quality_report  │
│                          Outlier control                                          │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Flujo funcional

1. **Generate**: crea millones de registros con nulos, duplicados y formatos corruptos.
2. **Clean**: corrige emails, normaliza campos, valida fechas/números y filtra inválidos.
3. **Deduplicate**: aplica unicidad por `event_id` en SQLite (`PRIMARY KEY`).
4. **Curate**: exporta dataset limpio a SQLite y CSV.
5. **Report**: calcula KPIs de calidad y top segmentos por revenue.

---

## Stack Tecnologico

| Componente | Version | Rol |
|------------|---------|-----|
| Python | 3.11+ | Implementación del pipeline y CLI |
| SQLite | stdlib | Almacenamiento curado y agregaciones SQL |
| Docker | latest | Ejecución portable en contenedor |
| Docker Compose | latest | Orquestación local |
| unittest | stdlib | Pruebas de humo end-to-end |

---

## Estructura del Proyecto

```text
Proyectos/
├── main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── src/
│   └── bigdata_god/
│       ├── generator.py
│       └── pipeline.py
├── tests/
│   └── test_pipeline_smoke.py
├── data/
│   ├── raw/
│   └── curated/
└── reports/
```

---

## Requisitos Previos

- Docker Engine 20.10+
- Docker Compose 2.0+
- Python 3.11+ (ejecución local)
- 4 GB RAM mínimo

---

## Instalacion y Ejecucion

### Opcion 1: Local

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py run-all --rows 1000000 --partitions 20
```

### Opcion 2: Docker

```bash
docker compose up --build
```

---

## Uso del CLI

```bash
# 1) Generar datos sucios masivos
python main.py generate --output data/raw --rows 3000000 --partitions 36 --seed 42

# 2) Ejecutar limpieza y curacion
python main.py clean --input-glob "data/raw/*.csv" --curated data/curated --report reports/quality_report.json

# 3) Flujo completo en un comando
python main.py run-all --raw-output data/raw --rows 3000000 --partitions 36 --curated data/curated --report reports/quality_report.json
```

---

## Regla de Calidad Aplicadas

- Estandarizacion de `country`, `channel`, `product`.
- Normalizacion de email (`" at "` -> `"@"`).
- Validacion de timestamps ISO.
- Control de rangos para `amount_usd` y `quantity`.
- Descarte de filas inválidas.
- Eliminacion de duplicados por `event_id`.

---

## Artefactos de Salida

- `data/curated/curated.db` -> base curada con llave única por evento.
- `data/curated/curated_events.csv` -> export tabular para consumo directo.
- `reports/quality_report.json` -> métricas de calidad, volumen y segmentos top.

---

## Verificacion Tecnica

```bash
# prueba automatica
python -m unittest discover -s tests -p "test_*.py" -v

# inspeccionar reporte
type reports\quality_report.json
```

Criterios de éxito:

- `raw_rows > 0`
- `curated_rows > 0`
- `rows_removed >= 0`
- `top_segments` con resultados

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
