from __future__ import annotations

import pandas as pd


def add_core_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add reusable features for corridor, calendar, and normalized risk rating."""
    out = df.copy()
    out["corridor"] = out["origin_country"].astype(str) + "->" + out["destination_country"].astype(str)
    out["country_pair"] = out["corridor"]
    out["transaction_day"] = out["transaction_date"].dt.floor("D")
    out["transaction_week"] = out["transaction_date"].dt.to_period("W").dt.start_time
    out["transaction_month"] = out["transaction_date"].dt.to_period("M").dt.start_time
    out["log_amount_usd"] = out["amount_usd"].clip(lower=1).map(lambda x: __import__("math").log1p(x))
    risk_map = {"Low": 0, "Medium": 1, "High": 2, "Critical": 3}
    out["risk_rating_num"] = out["risk_rating"].map(risk_map).fillna(1).astype(int)
    return out
