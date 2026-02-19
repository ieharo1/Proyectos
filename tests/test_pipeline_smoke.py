import tempfile
import unittest
from pathlib import Path

from src.bigdata_god.generator import generate_dirty_dataset
from src.bigdata_god.pipeline import run_cleaning_pipeline


class PipelineSmokeTest(unittest.TestCase):
    def test_end_to_end_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            raw_dir = temp_path / "raw"
            curated_dir = temp_path / "curated"
            report_file = temp_path / "report.json"

            files = generate_dirty_dataset(raw_dir, total_rows=20_000, partitions=4, seed=123)
            self.assertEqual(len(files), 4)

            report = run_cleaning_pipeline(str(raw_dir / "*.csv"), curated_dir, report_file)
            self.assertGreater(report["raw_rows"], 0)
            self.assertGreater(report["curated_rows"], 0)
            self.assertTrue(report_file.exists())
            self.assertTrue((curated_dir / "curated.db").exists())


if __name__ == "__main__":
    unittest.main()
