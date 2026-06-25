from __future__ import annotations

from pathlib import Path
import pandas as pd

from .config import PipelineConfig


def build_markdown_report(scored: pd.DataFrame, config: PipelineConfig) -> str:
    alerts = scored[scored["is_alert"]].copy()
    severity_counts = scored["severity"].value_counts().reindex(["Critical", "High", "Medium", "Low"]).fillna(0).astype(int)
    corridor_counts = alerts["corridor"].value_counts().head(10)

    lines = [
        "# KYC Cross-Border Financial-Flow Anomaly Report",
        "",
        "## Executive Summary",
        "",
        f"- Transactions reviewed: **{len(scored):,}**",
        f"- Alerts generated: **{len(alerts):,}**",
        f"- Alert threshold: **{config.thresholds.alert_score:.0f}**",
        "",
        "## Severity Distribution",
        "",
    ]

    for severity, count in severity_counts.items():
        lines.append(f"- {severity}: **{count:,}**")

    lines.extend(["", "## Top Alert Corridors", ""])
    if corridor_counts.empty:
        lines.append("No corridors exceeded the alert threshold.")
    else:
        for corridor, count in corridor_counts.items():
            lines.append(f"- {corridor}: **{count:,}** alert(s)")

    lines.extend([
        "",
        "## Highest-Risk Transactions",
        "",
    ])

    display_cols = [
        "transaction_id",
        "transaction_date",
        "sender_id",
        "receiver_id",
        "corridor",
        "amount_usd",
        "risk_rating",
        "anomaly_score",
        "severity",
        "reason_codes",
    ]
    top = alerts.sort_values("anomaly_score", ascending=False).head(15)
    if top.empty:
        lines.append("No transaction-level alerts were generated.")
    else:
        lines.append(top[display_cols].to_markdown(index=False))

    lines.extend([
        "",
        "## Method Notes",
        "",
        "The score combines robust historical baseline analysis, rolling-window outlier detection, time-based change detection, and configured risk-context indicators.",
        "Reason codes are designed to explain why a transaction was prioritized for review.",
        "This report is a monitoring aid and should be used with institutional AML/KYC policy, documentation review, sanctions screening, and analyst judgment.",
        "",
    ])
    return "\n".join(lines)


def write_report(scored: pd.DataFrame, config: PipelineConfig, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(build_markdown_report(scored, config), encoding="utf-8")
