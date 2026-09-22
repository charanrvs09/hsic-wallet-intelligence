# HSIC Wallet Intelligence

A customer wallet analytics and decision-intelligence platform for detecting silent attrition, understanding payment migration, identifying high-value recovery opportunities, and simulating potential Share-of-Wallet uplift.

Live Website Link: https://hsic-wallet-intelligence.streamlit.app/

## Overview

HSIC Wallet Intelligence transforms transaction-level customer behavior into actionable portfolio insights.

The platform helps answer four core questions:

- Is customer spending declining, or is payment preference shifting?
- Which customers are silently moving spend away from HSIC?
- Which customer groups offer the highest wallet-recovery opportunity?
- What could partial recovery of non-HSIC spend mean for Share of Wallet?

The solution combines descriptive analytics, customer-level behavioral engineering, business-rule detection, opportunity prioritization, unsupervised machine learning, campaign segmentation, and scenario simulation.

## Key Insights

- FY2025 HSIC Share of Wallet: **28.91%**
- FY2026 HSIC Share of Wallet: **19.48%**
- Share-of-Wallet decline: **9.43 percentage points**
- MetroMart net sales growth: **+19.39%**
- HSIC net spend growth: **-19.55%**
- Non-HSIC spend growth: **+35.22%**
- Valid behavioral population: **14,503 customers**
- Silent attriters identified: **3,973 customers**
- Silent-attrition addressable wallet: **₹2.99 Cr**
- Wallet Migrator addressable wallet: **₹6.43 Cr**

## Machine Learning

The platform uses **K-Means clustering** to discover behavioral customer groups.

### Final Clustering Setup

- Algorithm: K-Means
- Selected clusters: `K = 3`
- Silhouette Score: `0.4282`
- Preprocessing: StandardScaler
- Cluster selection evaluated using:
  - Silhouette Score
  - Calinski-Harabasz Score
  - Davies-Bouldin Score
  - Elbow / Inertia analysis

### Behavioral Segments

1. **HSIC-First Adopters**
   - 722 customers
   - Very high recent HSIC Share of Wallet
   - Strategic objective: Protect

2. **Active HSIC Growers**
   - 4,294 customers
   - Increasing HSIC usage
   - Strategic objective: Grow

3. **Wallet Migrators**
   - 9,487 customers
   - Customers remain commercially active but route most spend through alternative payment methods
   - Strategic objective: Win Back

## Silent Attrition Logic

A customer is classified as a silent attriter when:

- Baseline HSIC Share of Wallet is at least 20%
- HSIC Share of Wallet declines by at least 10 percentage points
- Recent MetroMart spend remains positive
- Recent non-HSIC spend remains positive

The behavioral comparison uses equal six-month baseline and recent periods.

## Opportunity Score

Customers are prioritized using a business-oriented Opportunity Score based on:

- Recoverable non-HSIC wallet
- Share-of-Wallet decline
- Recent MetroMart spend
- HSIC recency

The score is used for **action prioritization**, not as a probability of attrition.

## Platform Features

### Dashboard

Portfolio-level KPIs, monthly Share-of-Wallet trends, wallet composition, behavioral segments, and commercial opportunity.

### Portfolio & Migration

Fiscal-year spend comparison, payment-method migration, and Share-of-Wallet movement.

### Customer Segmentation

K-Means behavioral clusters, campaign micro-segments, and addressable wallet analysis.

### Opportunity Explorer

Interactive customer-level exploration using anonymized identifiers, including:

- Baseline vs recent Share of Wallet
- Addressable wallet
- Opportunity score
- Payment leakage method
- Behavioral flags
- Recommended recovery strategy

### Recovery Simulator

Interactive wallet-recovery scenarios showing potential:

- Incremental HSIC spend
- Projected Share of Wallet
- Share-of-Wallet uplift

Scenario outputs are illustrative and are not causal forecasts.

## Recovery Scenarios

| Recovery Scenario | Incremental HSIC Spend | Projected HSIC SoW | SoW Uplift |
|---|---:|---:|---:|
| 5% | ₹14.95 Lakh | 12.31% | +4.62 pp |
| 10% | ₹29.91 Lakh | 16.92% | +9.23 pp |
| 20% | ₹59.82 Lakh | 26.15% | +18.46 pp |

## Technology

- Python
- Pandas
- NumPy
- Scikit-learn
- K-Means Clustering
- Plotly
- Streamlit

## Project Structure

```text
hsic-wallet-intelligence/
│
├── .streamlit/
│   └── config.toml
│
├── data/
│   └── processed/
│       ├── dashboard_customers.csv
│       ├── business_segment_summary.csv
│       ├── campaign_segment_summary.csv
│       ├── campaign_segment_value.csv
│       ├── final_executive_kpis.csv
│       ├── final_impact_display.csv
│       ├── fiscal_year_sow.csv
│       ├── leakage_strategy.csv
│       ├── monthly_sow.csv
│       └── payment_analysis.csv
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
