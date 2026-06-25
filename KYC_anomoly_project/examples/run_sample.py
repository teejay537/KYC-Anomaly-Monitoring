from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from kyc_anomaly_monitoring.config import PipelineConfig
from kyc_anomaly_monitoring.pipeline import run_pipeline


if __name__ == "__main__":
    config = PipelineConfig.from_json(PROJECT_ROOT / "configs" / "sample_config.json")
    scored = run_pipeline(config)
    print(scored[["transaction_id", "sender_id", "corridor", "amount_usd", "anomaly_score", "severity", "reason_codes"]].head(10).to_string(index=False))
