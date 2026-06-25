from __future__ import annotations

import numpy as np
import pandas as pd

from .config import PipelineConfig


def _risk_context_score(row: pd.Series, config: PipelineConfig) -> float:
    score = 0.0
    if row.get("risk_rating") == "Critical":
        score += 55
    elif row.get("risk_rating") == "High":
        score += 40
    elif row.get("risk_rating") == "Medium":
        score += 20

    if row.get("origin_country") in config.high_risk_countries or row.get("destination_country") in config.high_risk_countries:
        score += 35
    elif row.get("origin_country") in config.elevated_risk_countries or row.get("destination_country") in config.elevated_risk_countries:
        score += 20

    if row.get("amount_usd", 0) >= config.thresholds.high_value_amount:
        score += 25

    if row.get("transaction_type") in {"Trade Finance", "Crypto Exchange", "Nested Correspondent"}:
        score += 10

    return min(score, 100.0)


def _severity(score: float, config: PipelineConfig) -> str:
    if score >= config.thresholds.critical_score:
        return "Critical"
    if score >= config.thresholds.high_score:
        return "High"
    if score >= config.thresholds.alert_score:
        return "Medium"
    return "Low"


def _recommended_action(severity: str) -> str:
    if severity == "Critical":
        return "Immediate enhanced due diligence review; consider escalation and temporary hold based on policy."
    if severity == "High":
        return "Compliance analyst review; validate source of funds, purpose, and counterparties."
    if severity == "Medium":
        return "Queue for analyst triage; compare with expected customer activity and supporting documentation."
    return "No immediate action; retain for monitoring and periodic review."


def _reason_codes(row: pd.Series, config: PipelineConfig) -> str:
    reasons: list[str] = []
    t = config.thresholds

    if row.get("entity_baseline_z", 0) >= t.robust_z_alert:
        reasons.append("Large deviation from sender/corridor historical baseline")
    if row.get("peer_baseline_z", 0) >= t.robust_z_alert:
        reasons.append("Large deviation from peer-group corridor baseline")
    if row.get("rolling_amount_ratio", 1) >= t.rolling_ratio_alert:
        reasons.append("Transaction amount sharply above recent rolling median")
    if row.get("rolling_z", 0) >= t.robust_z_alert:
        reasons.append("Rolling-window statistical outlier")
    if max(
        row.get("daily_amount_ratio", 1),
        row.get("weekly_amount_ratio", 1),
        row.get("monthly_amount_ratio", 1),
        row.get("daily_count_ratio", 1),
        row.get("weekly_count_ratio", 1),
        row.get("monthly_count_ratio", 1),
    ) >= t.period_change_alert:
        reasons.append("Sudden time-period change in transaction amount or count")
    if row.get("risk_rating") in {"High", "Critical"}:
        reasons.append(f"Customer risk rating is {row.get('risk_rating')}")
    if row.get("origin_country") in config.high_risk_countries or row.get("destination_country") in config.high_risk_countries:
        reasons.append("Transaction involves configured high-risk country")
    elif row.get("origin_country") in config.elevated_risk_countries or row.get("destination_country") in config.elevated_risk_countries:
        reasons.append("Transaction involves configured elevated-risk country")
    if row.get("amount_usd", 0) >= t.high_value_amount:
        reasons.append("High-value cross-border transfer")

    if not reasons:
        return "No major anomaly indicators triggered"
    return "; ".join(dict.fromkeys(reasons))


def add_final_scores(df: pd.DataFrame, config: PipelineConfig) -> pd.DataFrame:
    """Combine detector outputs into a final anomaly score, severity, and review guidance."""
    out = df.copy()
    out["risk_context_score"] = out.apply(lambda row: _risk_context_score(row, config), axis=1)

    w = config.weights
    weighted_score = (
        out["baseline_score"].fillna(0) * w.baseline
        + out["rolling_score"].fillna(0) * w.rolling
        + out["change_score"].fillna(0) * w.time_change
        + out["risk_context_score"].fillna(0) * w.risk_context
    )

    # Risk context should not dominate routine activity, but very high contextual risk
    # should still create a review floor even when the statistical history is shallow.
    risk_floor = np.select(
        [
            out["risk_context_score"] >= 90,
            out["risk_context_score"] >= 70,
            out["risk_context_score"] >= 50,
        ],
        [75.0, 60.0, 45.0],
        default=0.0,
    )
    out["anomaly_score"] = np.maximum(weighted_score, risk_floor).clip(0, 100).round(2)

    out["severity"] = out["anomaly_score"].apply(lambda x: _severity(float(x), config))
    out["is_alert"] = out["anomaly_score"] >= config.thresholds.alert_score
    out["reason_codes"] = out.apply(lambda row: _reason_codes(row, config), axis=1)
    out["recommended_action"] = out["severity"].apply(_recommended_action)

    sort_cols = ["is_alert", "anomaly_score", "transaction_date"]
    return out.sort_values(sort_cols, ascending=[False, False, False]).reset_index(drop=True)
