from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.bigdata_god.generator import generate_dirty_dataset
from src.bigdata_god.pipeline import run_cleaning_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="BigData God Cleaning: generate massive noisy data and clean it at scale."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="Generate dirty CSV partitions.")
    gen.add_argument("--output", default="data/raw", help="Output folder for raw CSV files.")
    gen.add_argument("--rows", type=int, default=1_000_000, help="Total rows to generate.")
    gen.add_argument("--partitions", type=int, default=20, help="Number of CSV files to create.")
    gen.add_argument("--seed", type=int, default=42, help="Random seed.")

    clean = sub.add_parser("clean", help="Run distributed cleaning and produce parquet + report.")
    clean.add_argument("--input-glob", default="data/raw/*.csv", help="Glob for raw CSV files.")
    clean.add_argument("--curated", default="data/curated", help="Output folder for curated parquet.")
    clean.add_argument("--report", default="reports/quality_report.json", help="Path for report JSON.")

    run = sub.add_parser("run-all", help="Generate then clean in one command.")
    run.add_argument("--raw-output", default="data/raw")
    run.add_argument("--rows", type=int, default=1_000_000)
    run.add_argument("--partitions", type=int, default=20)
    run.add_argument("--seed", type=int, default=42)
    run.add_argument("--curated", default="data/curated")
    run.add_argument("--report", default="reports/quality_report.json")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "generate":
        files = generate_dirty_dataset(args.output, args.rows, args.partitions, args.seed)
        print(f"Generated {len(files)} files in {args.output}")
        return

    if args.command == "clean":
        report = run_cleaning_pipeline(args.input_glob, args.curated, args.report)
        print(json.dumps(report, indent=2))
        return

    if args.command == "run-all":
        generate_dirty_dataset(args.raw_output, args.rows, args.partitions, args.seed)
        report = run_cleaning_pipeline(
            str(Path(args.raw_output) / "*.csv"),
            args.curated,
            args.report,
        )
        print(json.dumps(report, indent=2))
        return

    parser.error("Unsupported command")


if __name__ == "__main__":
    main()

