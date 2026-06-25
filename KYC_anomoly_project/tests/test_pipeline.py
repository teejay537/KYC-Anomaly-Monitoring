from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from kyc_anomaly_monitoring.config import PipelineConfig
from kyc_anomaly_monitoring.pipeline import run_pipeline
from kyc_anomaly_monitoring.data_io import load_flows


def test_load_sample_data_has_required_columns():
    df = load_flows(PROJECT_ROOT / "data" / "sample_flows.csv")
    assert len(df) > 100
    assert {"transaction_id", "sender_id", "amount_usd", "risk_rating"}.issubset(df.columns)


def test_pipeline_generates_scores_and_alerts(tmp_path):
    config = PipelineConfig.from_json(PROJECT_ROOT / "configs" / "sample_config.json")
    config.input_csv = str(PROJECT_ROOT / "data" / "sample_flows.csv")
    config.output_dir = str(tmp_path)
    scored = run_pipeline(config)

    assert "anomaly_score" in scored.columns
    assert "reason_codes" in scored.columns
    assert scored["anomaly_score"].between(0, 100).all()
    assert scored["is_alert"].sum() >= 1
    assert (tmp_path / "anomaly_scores.csv").exists()
    assert (tmp_path / "alerts.csv").exists()
    assert (tmp_path / "kyc_anomaly_report.md").exists()


def test_critical_or_high_risk_scenarios_are_prioritized(tmp_path):
    config = PipelineConfig.from_json(PROJECT_ROOT / "configs" / "sample_config.json")
    config.input_csv = str(PROJECT_ROOT / "data" / "sample_flows.csv")
    config.output_dir = str(tmp_path)
    scored = run_pipeline(config)

    high_risk = scored[scored["transaction_id"].isin(["TXN001411", "TXN001413"])]
    assert not high_risk.empty
    assert high_risk["anomaly_score"].max() >= config.thresholds.alert_score
