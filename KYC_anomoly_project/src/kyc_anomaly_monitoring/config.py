from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Dict


@dataclass
class Thresholds:
    alert_score: float = 60.0
    high_score: float = 75.0
    critical_score: float = 90.0
    robust_z_alert: float = 3.5
    rolling_ratio_alert: float = 4.0
    period_change_alert: float = 2.5
    high_value_amount: float = 250_000.0


@dataclass
class Weights:
    baseline: float = 0.35
    rolling: float = 0.30
    time_change: float = 0.20
    risk_context: float = 0.15


@dataclass
class PipelineConfig:
    input_csv: str = "data/sample_flows.csv"
    output_dir: str = "output"
    date_column: str = "transaction_date"
    entity_column: str = "sender_id"
    amount_column: str = "amount_usd"
    corridor_columns: list[str] = field(default_factory=lambda: ["origin_country", "destination_country"])
    peer_group_columns: list[str] = field(default_factory=lambda: ["customer_segment", "origin_country", "destination_country"])
    rolling_window_days: int = 30
    min_history: int = 5
    thresholds: Thresholds = field(default_factory=Thresholds)
    weights: Weights = field(default_factory=Weights)
    high_risk_countries: list[str] = field(default_factory=lambda: ["IRN", "PRK", "SYR"])
    elevated_risk_countries: list[str] = field(default_factory=lambda: ["RUS", "BLR", "MMR"])

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> "PipelineConfig":
        thresholds = Thresholds(**raw.get("thresholds", {}))
        weights = Weights(**raw.get("weights", {}))
        kwargs = {k: v for k, v in raw.items() if k not in {"thresholds", "weights"}}
        return cls(**kwargs, thresholds=thresholds, weights=weights)

    @classmethod
    def from_json(cls, path: str | Path) -> "PipelineConfig":
        with Path(path).open("r", encoding="utf-8") as f:
            return cls.from_dict(json.load(f))

    def validate(self) -> None:
        total_weight = (
            self.weights.baseline
            + self.weights.rolling
            + self.weights.time_change
            + self.weights.risk_context
        )
        if not 0.99 <= total_weight <= 1.01:
            raise ValueError(f"Weights should sum to approximately 1.0, got {total_weight:.3f}")
        if self.rolling_window_days < 2:
            raise ValueError("rolling_window_days must be at least 2")
        if self.min_history < 1:
            raise ValueError("min_history must be at least 1")
