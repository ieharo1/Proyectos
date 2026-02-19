from __future__ import annotations

import csv
import glob
import json
import sqlite3
from datetime import datetime
from pathlib import Path


def _normalize_row(row: dict[str, str]) -> dict[str, str] | None:
    event_id = (row.get("event_id") or "").strip()
    customer_id = (row.get("customer_id") or "").strip()
    event_ts = (row.get("event_ts") or "").strip()
    country = (row.get("country") or "UNKNOWN").strip().upper()
    channel = (row.get("channel") or "").strip().lower()
    product = (row.get("product") or "").strip().lower()
    email = (row.get("email") or "").strip().lower().replace(" at ", "@")

    if not event_id or not customer_id:
        return None

    try:
        customer_value = int(float(customer_id))
        datetime.fromisoformat(event_ts)
        amount = float(row.get("amount_usd", "0"))
        quantity = int(float(row.get("quantity", "0")))
    except (TypeError, ValueError):
        return None

    if amount <= 0:
        amount = 0.01
    if quantity < 1:
        quantity = 1
    if quantity > 30:
        quantity = 30

    return {
        "event_id": event_id,
        "customer_id": str(customer_value),
        "event_ts": event_ts,
        "country": country if country else "UNKNOWN",
        "channel": channel,
        "product": product,
        "amount_usd": f"{amount:.2f}",
        "quantity": str(quantity),
        "email": email,
    }


def run_cleaning_pipeline(input_glob: str, curated_path: str | Path, report_path: str | Path) -> dict:
    files = sorted(glob.glob(input_glob))
    if not files:
        raise FileNotFoundError(f"No files matched input pattern: {input_glob}")

    curated = Path(curated_path)
    curated.mkdir(parents=True, exist_ok=True)
    db_path = curated / "curated.db"
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE curated_events (
            event_id TEXT PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            event_ts TEXT NOT NULL,
            country TEXT NOT NULL,
            channel TEXT NOT NULL,
            product TEXT NOT NULL,
            amount_usd REAL NOT NULL,
            quantity INTEGER NOT NULL,
            email TEXT NOT NULL
        )
        """
    )

    raw_rows = 0
    invalid_rows = 0
    inserted_rows = 0

    batch: list[tuple] = []
    batch_size = 50_000

    for file in files:
        with Path(file).open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                raw_rows += 1
                normalized = _normalize_row(row)
                if normalized is None:
                    invalid_rows += 1
                    continue
                batch.append(
                    (
                        normalized["event_id"],
                        int(normalized["customer_id"]),
                        normalized["event_ts"],
                        normalized["country"],
                        normalized["channel"],
                        normalized["product"],
                        float(normalized["amount_usd"]),
                        int(normalized["quantity"]),
                        normalized["email"],
                    )
                )
                if len(batch) >= batch_size:
                    conn.executemany(
                        """
                        INSERT OR IGNORE INTO curated_events
                        (event_id, customer_id, event_ts, country, channel, product, amount_usd, quantity, email)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        batch,
                    )
                    inserted_rows += conn.total_changes - inserted_rows
                    batch.clear()

    if batch:
        conn.executemany(
            """
            INSERT OR IGNORE INTO curated_events
            (event_id, customer_id, event_ts, country, channel, product, amount_usd, quantity, email)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            batch,
        )
        inserted_rows += conn.total_changes - inserted_rows
        batch.clear()

    curated_csv = curated / "curated_events.csv"
    with curated_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            ["event_id", "customer_id", "event_ts", "country", "channel", "product", "amount_usd", "quantity", "email"]
        )
        for record in conn.execute(
            "SELECT event_id, customer_id, event_ts, country, channel, product, amount_usd, quantity, email FROM curated_events"
        ):
            writer.writerow(record)

    top_segments_rows = conn.execute(
        """
        SELECT
            country,
            channel,
            COUNT(*) AS events,
            ROUND(SUM(amount_usd), 2) AS revenue_usd,
            ROUND(AVG(amount_usd), 2) AS avg_ticket
        FROM curated_events
        GROUP BY country, channel
        ORDER BY revenue_usd DESC
        LIMIT 10
        """
    ).fetchall()

    conn.close()

    removed_rows = raw_rows - inserted_rows
    report = {
        "raw_rows": raw_rows,
        "curated_rows": inserted_rows,
        "invalid_rows": invalid_rows,
        "rows_removed": removed_rows,
        "removal_ratio": round((removed_rows / raw_rows) if raw_rows else 0.0, 4),
        "artifacts": {
            "sqlite_db": str(db_path),
            "curated_csv": str(curated_csv),
        },
        "top_segments": [
            {
                "country": row[0],
                "channel": row[1],
                "events": row[2],
                "revenue_usd": row[3],
                "avg_ticket": row[4],
            }
            for row in top_segments_rows
        ],
    }

    report_file = Path(report_path)
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
