from pathlib import Path
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def generate_sample_flows(output_path: Path, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    start = pd.Timestamp("2025-01-01")
    days = pd.date_range(start, periods=180, freq="D")

    senders = [
        ("CUST_A101", "Corporate", "Medium"),
        ("CUST_A102", "SME", "Low"),
        ("CUST_A103", "NBFI", "High"),
        ("CUST_A104", "Retail", "Low"),
        ("CUST_A105", "Corporate", "Medium"),
        ("CUST_A106", "SME", "Medium"),
    ]
    receivers = ["RCV_B201", "RCV_B202", "RCV_B203", "RCV_B204", "RCV_B205", "RCV_B206"]
    corridors = [("USA", "GBR"), ("USA", "DEU"), ("USA", "ZAF"), ("GBR", "USA"), ("USA", "ARE"), ("USA", "RUS")]
    banks = ["Atlantic Bank", "Mercury Trust", "Continental Finance", "Harbor Bank"]
    tx_types = ["Wire", "ACH", "Remittance", "Trade Finance"]
    purposes = ["Invoice Payment", "Services", "Capital Goods", "Family Support", "Intercompany Transfer"]

    rows = []
    transaction_no = 1
    for day in days:
        daily_count = rng.poisson(8)
        for _ in range(daily_count):
            sender_id, segment, risk = senders[rng.integers(0, len(senders))]
            receiver_id = receivers[rng.integers(0, len(receivers))]
            origin, dest = corridors[rng.integers(0, len(corridors))]
            base = {
                "Retail": 2_000,
                "SME": 15_000,
                "Corporate": 80_000,
                "NBFI": 120_000,
            }[segment]
            amount = float(rng.lognormal(mean=np.log(base), sigma=0.55))
            rows.append(
                {
                    "transaction_id": f"TXN{transaction_no:06d}",
                    "transaction_date": day.strftime("%Y-%m-%d"),
                    "sender_id": sender_id,
                    "receiver_id": receiver_id,
                    "origin_country": origin,
                    "destination_country": dest,
                    "sender_bank": banks[rng.integers(0, len(banks))],
                    "receiver_bank": banks[rng.integers(0, len(banks))],
                    "currency": "USD",
                    "amount_usd": round(amount, 2),
                    "transaction_type": tx_types[rng.integers(0, len(tx_types))],
                    "customer_segment": segment,
                    "purpose_code": purposes[rng.integers(0, len(purposes))],
                    "risk_rating": risk,
                }
            )
            transaction_no += 1

    # Inject designed anomalies: value spike, burst pattern, new high-risk corridor, and monthly step change.
    injected = [
        ("2025-03-18", "CUST_A102", "RCV_B204", "USA", "DEU", 425_000, "Wire", "SME", "Medium", "Unusual Invoice Payment"),
        ("2025-04-03", "CUST_A103", "RCV_B205", "USA", "RUS", 780_000, "Trade Finance", "NBFI", "High", "Large Trade Settlement"),
        ("2025-05-20", "CUST_A106", "RCV_B206", "USA", "ARE", 510_000, "Wire", "SME", "Medium", "Intercompany Transfer"),
        ("2025-06-10", "CUST_A101", "RCV_B203", "USA", "SYR", 350_000, "Nested Correspondent", "Corporate", "Critical", "Third-Party Payment"),
    ]
    for date, sender, receiver, origin, dest, amount, tx_type, segment, risk, purpose in injected:
        rows.append(
            {
                "transaction_id": f"TXN{transaction_no:06d}",
                "transaction_date": date,
                "sender_id": sender,
                "receiver_id": receiver,
                "origin_country": origin,
                "destination_country": dest,
                "sender_bank": "Atlantic Bank",
                "receiver_bank": "Harbor Bank",
                "currency": "USD",
                "amount_usd": amount,
                "transaction_type": tx_type,
                "customer_segment": segment,
                "purpose_code": purpose,
                "risk_rating": risk,
            }
        )
        transaction_no += 1

    # Inject short burst of transactions for time-change detection.
    for i in range(12):
        rows.append(
            {
                "transaction_id": f"TXN{transaction_no:06d}",
                "transaction_date": "2025-05-21",
                "sender_id": "CUST_A104",
                "receiver_id": f"RCV_B20{(i % 6) + 1}",
                "origin_country": "USA",
                "destination_country": "ZAF",
                "sender_bank": "Mercury Trust",
                "receiver_bank": "Continental Finance",
                "currency": "USD",
                "amount_usd": round(float(rng.lognormal(mean=np.log(6_000), sigma=0.35)), 2),
                "transaction_type": "Remittance",
                "customer_segment": "Retail",
                "purpose_code": "Family Support",
                "risk_rating": "Low",
            }
        )
        transaction_no += 1

    df = pd.DataFrame(rows).sort_values(["transaction_date", "transaction_id"]).reset_index(drop=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


if __name__ == "__main__":
    out = PROJECT_ROOT / "data" / "sample_flows.csv"
    df = generate_sample_flows(out)
    print(f"Wrote {len(df):,} synthetic transactions to {out}")
