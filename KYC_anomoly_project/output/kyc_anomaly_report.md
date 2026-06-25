# KYC Cross-Border Financial-Flow Anomaly Report

## Executive Summary

- Transactions reviewed: **1,425**
- Alerts generated: **29**
- Alert threshold: **60**

## Severity Distribution

- Critical: **3**
- High: **4**
- Medium: **22**
- Low: **1,396**

## Top Alert Corridors

- USA->RUS: **15** alert(s)
- USA->ARE: **5** alert(s)
- USA->DEU: **3** alert(s)
- USA->ZAF: **2** alert(s)
- GBR->USA: **2** alert(s)
- USA->SYR: **1** alert(s)
- USA->GBR: **1** alert(s)

## Highest-Risk Transactions

| transaction_id   | transaction_date    | sender_id   | receiver_id   | corridor   |   amount_usd | risk_rating   |   anomaly_score | severity   | reason_codes                                                                                                                                                                                                                                                                                                                                                                             |
|:-----------------|:--------------------|:------------|:--------------|:-----------|-------------:|:--------------|----------------:|:-----------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| TXN001411        | 2025-04-03 00:00:00 | CUST_A103   | RCV_B205      | USA->RUS   |    780000    | High          |           98.57 | Critical   | Large deviation from sender/corridor historical baseline; Large deviation from peer-group corridor baseline; Transaction amount sharply above recent rolling median; Rolling-window statistical outlier; Sudden time-period change in transaction amount or count; Customer risk rating is High; Transaction involves configured elevated-risk country; High-value cross-border transfer |
| TXN001412        | 2025-05-20 00:00:00 | CUST_A106   | RCV_B206      | USA->ARE   |    510000    | Medium        |           91.75 | Critical   | Large deviation from sender/corridor historical baseline; Large deviation from peer-group corridor baseline; Transaction amount sharply above recent rolling median; Rolling-window statistical outlier; Sudden time-period change in transaction amount or count; High-value cross-border transfer                                                                                      |
| TXN001410        | 2025-03-18 00:00:00 | CUST_A102   | RCV_B204      | USA->DEU   |    425000    | Medium        |           91.75 | Critical   | Large deviation from sender/corridor historical baseline; Large deviation from peer-group corridor baseline; Transaction amount sharply above recent rolling median; Rolling-window statistical outlier; Sudden time-period change in transaction amount or count; High-value cross-border transfer                                                                                      |
| TXN000708        | 2025-03-29 00:00:00 | CUST_A103   | RCV_B206      | USA->RUS   |    454791    | High          |           77.25 | High       | Large deviation from sender/corridor historical baseline; Large deviation from peer-group corridor baseline; Transaction amount sharply above recent rolling median; Rolling-window statistical outlier; Sudden time-period change in transaction amount or count; Customer risk rating is High; Transaction involves configured elevated-risk country; High-value cross-border transfer |
| TXN001417        | 2025-05-21 00:00:00 | CUST_A104   | RCV_B204      | USA->ZAF   |     12734.8  | Low           |           75.16 | High       | Large deviation from sender/corridor historical baseline; Large deviation from peer-group corridor baseline; Transaction amount sharply above recent rolling median; Rolling-window statistical outlier; Sudden time-period change in transaction amount or count                                                                                                                        |
| TXN001399        | 2025-06-28 00:00:00 | CUST_A103   | RCV_B206      | USA->RUS   |    292234    | High          |           75    | High       | Large deviation from sender/corridor historical baseline; Large deviation from peer-group corridor baseline; Sudden time-period change in transaction amount or count; Customer risk rating is High; Transaction involves configured elevated-risk country; High-value cross-border transfer                                                                                             |
| TXN001413        | 2025-06-10 00:00:00 | CUST_A101   | RCV_B203      | USA->SYR   |    350000    | Critical      |           75    | High       | Customer risk rating is Critical; Transaction involves configured high-risk country; High-value cross-border transfer                                                                                                                                                                                                                                                                    |
| TXN000197        | 2025-01-25 00:00:00 | CUST_A103   | RCV_B204      | USA->RUS   |    264253    | High          |           69.95 | Medium     | Large deviation from sender/corridor historical baseline; Large deviation from peer-group corridor baseline; Rolling-window statistical outlier; Sudden time-period change in transaction amount or count; Customer risk rating is High; Transaction involves configured elevated-risk country; High-value cross-border transfer                                                         |
| TXN000809        | 2025-04-10 00:00:00 | CUST_A101   | RCV_B206      | USA->ARE   |    303899    | Medium        |           68.59 | Medium     | Large deviation from sender/corridor historical baseline; Large deviation from peer-group corridor baseline; Transaction amount sharply above recent rolling median; Rolling-window statistical outlier; High-value cross-border transfer                                                                                                                                                |
| TXN000695        | 2025-03-28 00:00:00 | CUST_A103   | RCV_B203      | USA->DEU   |    541433    | High          |           68.5  | Medium     | Large deviation from sender/corridor historical baseline; Large deviation from peer-group corridor baseline; Transaction amount sharply above recent rolling median; Sudden time-period change in transaction amount or count; Customer risk rating is High; High-value cross-border transfer                                                                                            |
| TXN001277        | 2025-06-14 00:00:00 | CUST_A105   | RCV_B202      | GBR->USA   |    336344    | Medium        |           67.55 | Medium     | Large deviation from sender/corridor historical baseline; Large deviation from peer-group corridor baseline; Rolling-window statistical outlier; Sudden time-period change in transaction amount or count; High-value cross-border transfer                                                                                                                                              |
| TXN000441        | 2025-02-24 00:00:00 | CUST_A104   | RCV_B202      | USA->ARE   |      8374.08 | Low           |           64.36 | Medium     | Large deviation from sender/corridor historical baseline; Large deviation from peer-group corridor baseline; Transaction amount sharply above recent rolling median; Rolling-window statistical outlier; Sudden time-period change in transaction amount or count                                                                                                                        |
| TXN000154        | 2025-01-21 00:00:00 | CUST_A103   | RCV_B204      | USA->DEU   |    689427    | High          |           62.95 | Medium     | Large deviation from sender/corridor historical baseline; Large deviation from peer-group corridor baseline; Sudden time-period change in transaction amount or count; Customer risk rating is High; High-value cross-border transfer                                                                                                                                                    |
| TXN000395        | 2025-02-19 00:00:00 | CUST_A103   | RCV_B201      | USA->RUS   |    362673    | High          |           61.75 | Medium     | Large deviation from sender/corridor historical baseline; Large deviation from peer-group corridor baseline; Sudden time-period change in transaction amount or count; Customer risk rating is High; Transaction involves configured elevated-risk country; High-value cross-border transfer                                                                                             |
| TXN000956        | 2025-04-29 00:00:00 | CUST_A101   | RCV_B201      | GBR->USA   |    237096    | Medium        |           60.08 | Medium     | Large deviation from sender/corridor historical baseline; Large deviation from peer-group corridor baseline; Rolling-window statistical outlier; Sudden time-period change in transaction amount or count                                                                                                                                                                                |

## Method Notes

The score combines robust historical baseline analysis, rolling-window outlier detection, time-based change detection, and configured risk-context indicators.
Reason codes are designed to explain why a transaction was prioritized for review.
This report is a monitoring aid and should be used with institutional AML/KYC policy, documentation review, sanctions screening, and analyst judgment.
