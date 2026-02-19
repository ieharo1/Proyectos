from __future__ import annotations

import csv
import math
import random
from datetime import datetime, timedelta
from pathlib import Path


COUNTRIES = ["US", "MX", "ES", "CO", "AR", "CL", "PE", "EC"]
CHANNELS = ["web", "app", "phone", "store"]
PRODUCTS = ["cloud_etl", "lakehouse", "streaming", "batch_orchestrator", "gpu_pipeline", "fraud_detector"]


def _random_timestamp(rng: random.Random) -> str:
    base = datetime(2025, 1, 1)
    offset_seconds = rng.randint(0, 365 * 24 * 3600)
    return (base + timedelta(seconds=offset_seconds)).isoformat()


def _build_row(rng: random.Random, partition_index: int, row_index: int) -> dict[str, str]:
    customer_id = rng.randint(100_000, 999_999)
    email = f"client_{customer_id}@bigcorp.ai"
    if rng.random() < 0.09:
        email = email.replace("@", " at ")

    amount = round(rng.lognormvariate(3.8, 0.6), 2)
    if rng.random() < 0.025:
        amount = round(amount * rng.uniform(12, 45), 2)

    country = rng.choice(COUNTRIES)
    if rng.random() < 0.06:
        country = ""

    return {
        "event_id": f"evt_{partition_index}_{row_index}",
        "customer_id": str(customer_id),
        "event_ts": _random_timestamp(rng),
        "country": country,
        "channel": rng.choice(CHANNELS),
        "product": rng.choice(PRODUCTS),
        "amount_usd": str(amount),
        "quantity": str(rng.randint(1, 7)),
        "email": email,
    }


def generate_dirty_dataset(output_dir: str | Path, total_rows: int, partitions: int, seed: int = 42) -> list[Path]:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if total_rows <= 0:
        raise ValueError("total_rows must be > 0")
    if partitions <= 0:
        raise ValueError("partitions must be > 0")

    rng = random.Random(seed)
    rows_per_partition = math.ceil(total_rows / partitions)
    files: list[Path] = []

    for idx in range(partitions):
        start = idx * rows_per_partition
        end = min(total_rows, (idx + 1) * rows_per_partition)
        if start >= end:
            break

        file_path = output_path / f"raw_events_{idx:03d}.csv"
        with file_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "event_id",
                    "customer_id",
                    "event_ts",
                    "country",
                    "channel",
                    "product",
                    "amount_usd",
                    "quantity",
                    "email",
                ],
            )
            writer.writeheader()
            for row_idx in range(start, end):
                row = _build_row(rng, idx, row_idx - start)
                writer.writerow(row)
                if rng.random() < 0.02:
                    writer.writerow(row)
        files.append(file_path)

    return files
