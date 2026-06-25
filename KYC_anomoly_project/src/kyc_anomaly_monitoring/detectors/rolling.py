from __future__ import annotations

import numpy as np
import pandas as pd


def _rolling_for_group(group: pd.DataFrame, amount_column: str, window: int, min_history: int) -> pd.DataFrame:
    g = group.sort_values(["transaction_date", "transaction_id"]).copy()
    shifted = g[amount_column].shift(1)
    g["rolling_median_amount"] = shifted.rolling(window=window, min_periods=min_history).median()
    g["rolling_mean_amount"] = shifted.rolling(window=window, min_periods=min_history).mean()
    g["rolling_std_amount"] = shifted.rolling(window=window, min_periods=min_history).std(ddof=0)
    g["rolling_txn_count"] = shifted.rolling(window=window, min_periods=min_history).count()
    g["rolling_total_amount"] = shifted.rolling(window=window, min_periods=min_history).sum()

    median = g["rolling_median_amount"].replace(0, np.nan)
    g["rolling_amount_ratio"] = (g[amount_column] / median).replace([np.inf, -np.inf], np.nan).fillna(1.0)

    std = g["rolling_std_amount"].replace(0, np.nan)
    g["rolling_z"] = ((g[amount_column] - g["rolling_mean_amount"]) / std).abs()
    g["rolling_z"] = g["rolling_z"].replace([np.inf, -np.inf], np.nan).fillna(0.0)

    ratio_component = ((g["rolling_amount_ratio"].clip(lower=1, upper=8) - 1) / 7 * 100)
    z_component = (g["rolling_z"].clip(lower=0, upper=8) / 8 * 100)
    g["rolling_score"] = np.maximum(ratio_component, z_component).fillna(0).round(2)
    return g


def add_rolling_scores(
    df: pd.DataFrame,
    entity_column: str = "sender_id",
    amount_column: str = "amount_usd",
    window: int = 30,
    min_history: int = 5,
) -> pd.DataFrame:
    """Add rolling-window outlier scores by sender and corridor."""
    group_cols = [entity_column, "corridor"]
    return (
        df.groupby(group_cols, group_keys=False)
        .apply(_rolling_for_group, amount_column=amount_column, window=window, min_history=min_history)
        .reset_index(drop=True)
    )
