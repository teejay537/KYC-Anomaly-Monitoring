from __future__ import annotations

from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = [
    "transaction_id",
    "transaction_date",
    "sender_id",
    "receiver_id",
    "origin_country",
    "destination_country",
    "sender_bank",
    "receiver_bank",
    "currency",
    "amount_usd",
    "transaction_type",
    "customer_segment",
    "purpose_code",
    "risk_rating",
]


def load_flows(path: str | Path) -> pd.DataFrame:
    """Load transaction-level financial-flow data from CSV and validate basic schema."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    df = pd.read_csv(path)
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.copy()
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
    if df["transaction_date"].isna().any():
        bad_count = int(df["transaction_date"].isna().sum())
        raise ValueError(f"Found {bad_count} rows with invalid transaction_date")

    df["amount_usd"] = pd.to_numeric(df["amount_usd"], errors="coerce")
    if df["amount_usd"].isna().any():
        bad_count = int(df["amount_usd"].isna().sum())
        raise ValueError(f"Found {bad_count} rows with invalid amount_usd")

    if (df["amount_usd"] < 0).any():
        raise ValueError("amount_usd must be non-negative")

    return df.sort_values(["sender_id", "transaction_date", "transaction_id"]).reset_index(drop=True)


def write_csv(df: pd.DataFrame, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
