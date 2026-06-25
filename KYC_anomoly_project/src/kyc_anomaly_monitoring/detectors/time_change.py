from __future__ import annotations

import numpy as np
import pandas as pd


def _add_period_ratio(
    df: pd.DataFrame,
    period_column: str,
    amount_column: str,
    entity_column: str,
    label: str,
) -> pd.DataFrame:
    group_cols = [entity_column, "corridor", period_column]
    agg = df.groupby(group_cols).agg(
        period_total_amount=(amount_column, "sum"),
        period_txn_count=(amount_column, "count"),
    ).reset_index()
    agg = agg.sort_values([entity_column, "corridor", period_column])

    def calc(g: pd.DataFrame) -> pd.DataFrame:
        g = g.copy()
        previous_amount = g["period_total_amount"].shift(1).replace(0, np.nan)
        previous_count = g["period_txn_count"].shift(1).replace(0, np.nan)
        g[f"{label}_amount_ratio"] = (g["period_total_amount"] / previous_amount).replace([np.inf, -np.inf], np.nan).fillna(1.0)
        g[f"{label}_count_ratio"] = (g["period_txn_count"] / previous_count).replace([np.inf, -np.inf], np.nan).fillna(1.0)
        amount_component = ((g[f"{label}_amount_ratio"].clip(lower=1, upper=6) - 1) / 5 * 100)
        count_component = ((g[f"{label}_count_ratio"].clip(lower=1, upper=6) - 1) / 5 * 100)
        g[f"{label}_change_score"] = np.maximum(amount_component, count_component).round(2)
        return g

    agg = agg.groupby([entity_column, "corridor"], group_keys=False).apply(calc)
    keep_cols = group_cols + [
        f"{label}_amount_ratio",
        f"{label}_count_ratio",
        f"{label}_change_score",
    ]
    return df.merge(agg[keep_cols], on=group_cols, how="left")


def add_time_change_scores(
    df: pd.DataFrame,
    entity_column: str = "sender_id",
    amount_column: str = "amount_usd",
) -> pd.DataFrame:
    """Add day/week/month period-change scores."""
    out = _add_period_ratio(df, "transaction_day", amount_column, entity_column, "daily")
    out = _add_period_ratio(out, "transaction_week", amount_column, entity_column, "weekly")
    out = _add_period_ratio(out, "transaction_month", amount_column, entity_column, "monthly")
    out["change_score"] = out[
        ["daily_change_score", "weekly_change_score", "monthly_change_score"]
    ].max(axis=1).fillna(0).round(2)
    return out
