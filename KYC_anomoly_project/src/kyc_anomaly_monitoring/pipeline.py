from __future__ import annotations

from pathlib import Path
import pandas as pd

from .config import PipelineConfig
from .data_io import load_flows, write_csv
from .features import add_core_features
from .detectors.baseline import add_baseline_scores
from .detectors.rolling import add_rolling_scores
from .detectors.time_change import add_time_change_scores
from .scoring import add_final_scores
from .reporting import write_report


def run_pipeline(config: PipelineConfig) -> pd.DataFrame:
    """Run the complete KYC anomaly monitoring pipeline and write outputs."""
    config.validate()

    df = load_flows(config.input_csv)
    df = add_core_features(df)
    df = add_baseline_scores(
        df,
        entity_column=config.entity_column,
        amount_column=config.amount_column,
        peer_group_columns=config.peer_group_columns,
        min_history=config.min_history,
    )
    df = add_rolling_scores(
        df,
        entity_column=config.entity_column,
        amount_column=config.amount_column,
        window=config.rolling_window_days,
        min_history=config.min_history,
    )
    df = add_time_change_scores(
        df,
        entity_column=config.entity_column,
        amount_column=config.amount_column,
    )
    scored = add_final_scores(df, config)

    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(scored, output_dir / "anomaly_scores.csv")
    write_csv(scored[scored["is_alert"]].copy(), output_dir / "alerts.csv")
    write_report(scored, config, output_dir / "kyc_anomaly_report.md")
    return scored
