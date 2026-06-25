from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .config import PipelineConfig
from .pipeline import run_pipeline


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run KYC cross-border financial-flow anomaly monitoring.")
    parser.add_argument("--config", default="configs/sample_config.json", help="Path to JSON config file.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    config_path = Path(args.config)
    config = PipelineConfig.from_json(config_path)
    scored = run_pipeline(config)
    alerts = int(scored["is_alert"].sum())
    print(f"Reviewed {len(scored):,} transactions")
    print(f"Generated {alerts:,} alerts")
    print(f"Outputs written to: {Path(config.output_dir).resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
