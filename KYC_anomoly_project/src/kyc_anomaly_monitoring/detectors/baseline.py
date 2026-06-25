from __future__ import annotations

import numpy as np
import pandas as pd


def _mad(values: pd.Series) -> float:
    median = values.median()
    mad = (values - median).abs().median()
    return float(mad) if pd.notna(mad) else 0.0


def _robust_z(value: pd.Series, median: pd.Series, mad: pd.Series) -> pd.Series:
    scale = mad.replace(0, np.nan)
    z = 0.6745 * (value - median) / scale
    return z.replace([np.inf, -np.inf], np.nan).fillna(0.0).abs()


def _score_from_z(z: pd.Series) -> pd.Series:
    return (z.clip(lower=0, upper=10) / 10 * 100).round(2)


def add_baseline_scores(
    df: pd.DataFrame,
    entity_column: str = "sender_id",
    amount_column: str = "amount_usd",
    peer_group_columns: list[str] | None = None,
    min_history: int = 5,
) -> pd.DataFrame:
    """Compare transactions with customer/corridor and peer-group historical baselines.

    The method uses robust statistics so that a few very large transactions do not dominate the
    baseline. For production monitoring, run this on a fixed approved lookback window or a fitted
    baseline table rather than on the same batch under review.
    """
    out = df.copy()
    peer_group_columns = peer_group_columns or ["customer_segment", "origin_country", "destination_country"]

    entity_group = [entity_column, "corridor"]
    entity_stats = out.groupby(entity_group)[amount_column].agg(
        entity_baseline_count="count",
        entity_baseline_median="median",
        entity_baseline_mad=_mad,
    ).reset_index()
    out = out.merge(entity_stats, on=entity_group, how="left")

    peer_stats = out.groupby(peer_group_columns)[amount_column].agg(
        peer_baseline_count="count",
        peer_baseline_median="median",
        peer_baseline_mad=_mad,
    ).reset_index()
    out = out.merge(peer_stats, on=peer_group_columns, how="left")

    out["entity_baseline_z"] = _robust_z(
        out[amount_column], out["entity_baseline_median"], out["entity_baseline_mad"]
    )
    out["peer_baseline_z"] = _robust_z(
        out[amount_column], out["peer_baseline_median"], out["peer_baseline_mad"]
    )

    # If entity history is shallow, rely more heavily on the peer baseline.
    enough_history = out["entity_baseline_count"] >= min_history
    entity_score = _score_from_z(out["entity_baseline_z"])
    peer_score = _score_from_z(out["peer_baseline_z"])
    out["baseline_score"] = np.where(
        enough_history,
        np.maximum(entity_score, peer_score * 0.85),
        peer_score,
    ).round(2)

    return out
