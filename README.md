# FinOps for M&A: Infrastructure Due Diligence Dashboard

**Quantifying Cloud Infrastructure Waste as Acquisition Liability**  
**Case Study: $200M SaaS Target – Identifying $8.8M Annual Optimization Opportunity**

This project demonstrates a comprehensive infrastructure due diligence framework used to evaluate cloud cost structures in M&A transactions. It translates technical waste into P&L and valuation impacts, enabling data-driven negotiation adjustments and post-close value creation plans.

**Key Outcomes Modeled**  
- Current annual cloud spend: **$17.0M** (multi-cloud: AWS dominant)  
- Identified waste: **$8.8M/year** (56% of spend)  
- Optimized steady-state run rate: **$8.2M/year**  
- Recommended valuation haircut: **$15M** (to reflect infrastructure liability)  
- Post-acquisition value creation: **$32.7M** 5-year NPV at 10% discount rate  
- Payback period: **~14 months** (phased implementation with quick wins funding most efforts)  
- First-90-days quick wins: **$3.6M annualized**

**Interactive Dashboard (Tableau Public)**  
Explore filters, drill-downs, benchmarks, and phased savings:  
[**FinOps M&A Due Diligence Dashboard – $8.8M PE Acquisition Case Study**](https://tinyurl.com/47b3z559)

> All data is **fully synthetic and anonymized** — based on realistic multi-cloud patterns (AWS, GCP, Azure). No real billing data, PII, or proprietary information is included.

## Executive Summary & Narrative Structure

Three-act Tableau dashboard built for PE diligence teams, CTOs, and FinOps leaders:

1. **Home – The $8.8M Question**  
   High-level diagnostics challenging "optimized infrastructure" claims.  
   - Spend vs. benchmarks: Cost/customer $250/mo (vs. industry $80–$120), cloud as % revenue 30% (vs. 12%).  
   - Waste identification: 56% ($8.8M) across environments and categories.  
   - Multi-cloud breakdown: AWS $10.3M | GCP $5.5M | Azure $1.2M.  
   - Post-optimization value: $8.8M/year savings potential.

2. **Post-Acquisition – Unlocking Value**  
   Red flags, quick wins, and financial modeling.  
   - **5-Year NPV**: $32.7M (conservative ramp, minimal net upfront).  
   - **Top red flags**: 24/7 dev/staging ($2.88M), 90% on-demand instances ($1.95M), oversized compute ($1.24M), cross-region egress ($816K).  
   - Reserved instance coverage: 10% vs. industry 60%.  
   - Service-level waste severity: EC2 Compute & data transfer highest (critical/high).  
   - Ongoing tech debt exposure: ~$1.2M/year (untagged resources, orphaned assets, sprawl).

3. **Roadmap – Capturing the $8.8M**  
   12-month phased implementation plan (low → high risk).  
   - Phase 1 (Months 1–3): Quick wins + governance ($3.6M, low risk).  
   - Phase 2 (Months 2–4): Reserved instances & right-sizing ($2M, medium).  
   - Phase 3–4: Consolidation, auto-scaling, architecture redesign ($3.2M cumulative).  
   - Critical success factors: Executive sponsorship, FinOps lead hire, tagging strategy, weekly governance.

## Skills & Senior-Level Demonstrations

This artifact showcases senior FinOps / cloud financial management capabilities:

- **Strategic Due Diligence** — Bridging technical infra analysis with valuation/P&L impact for M&A.  
- **Financial Modeling** — NPV, payback, discounted cash flows; conservative assumptions & sensitivity.  
- **Executive Communication** — Tableau storytelling for C-suite / PE audiences (benchmarks, severity coding, phased ROI).  
- **Optimization Expertise** — Multi-cloud waste identification (right-sizing, RI strategy, shutdown policies, egress reduction).  
- **Governance & Execution** — Cost allocation, tagging, anomaly alerting, risk-prioritized roadmaps.  
- **Reproducibility** — Python models for NPV/payback to enable scenario analysis.

Ideal for roles requiring cloud cost leadership, PE tech diligence, or post-acquisition integration.

## Reproducible Financial Models (Python)

> ### Note: Exact NPV may vary slightly due to rounding in the dashboard visuals. The model uses conservative 10% discount rate and phased ramp-up for realism. Adjust initial_investment or the savings stream for sensitivity analysis.

## Cleaned Datasets (Synthetic Data Sources)

To enable full reproducibility and deeper analysis, the repo includes **4 cleaned CSV files** containing the synthetic multi-cloud data used to build the Tableau dashboard and financial models.

All data is **fully synthetic** (generated to mimic realistic AWS/GCP/Azure billing patterns from a mid-sized SaaS company) with no real account info, costs, or identifiers.

| File Name                  | Description                                                                 | Key Columns (example)                          | Rows (approx.) | Used For |
|----------------------------|-----------------------------------------------------------------------------|------------------------------------------------|----------------|----------|
| `ma_target_cloud_costs TAGM2.csv` | Detailed monthly/annual costs by service, provider, environment, waste flags | Date, Service, Cloud_Provider, Environment, Annual_Cost, Waste_Amount, Optimization_Status,| ~40 | Home spend breakdowns, multi-cloud distribution |
| `ma_post_acquisition_roadmap TAGM.csv` | Phased optimization initiatives with timeline, savings, cost, risk |  Initiative, Phase, Start_Month, Annual_Savings, Implementation_Cost, Risk_Level | ~35  | Roadmap Gantt/timeline, phased savings stacking|
| `ma_optimization_analysis TAGM.csv`    |  Itemized red flags, issues, severity, quick wins, and savings potential |Issue_Category, Issue_Description, Annual_Cost_Impact, Severity, Quick_Win | ~15 | Post-Acquisition red flags bars, service-level waste severity |
| `ma_industry_benchmarks TAGM.csv` | Benchmark metrics comparing target to industry/best-in-class  | Metric, Target_Company, Industry_Average, Best_In_Class, Gap_From_Average, Status | ~15 | Home benchmark (e.g., waste %, RI coverage) |


### NPV & Payback Functions
```python
def calculate_npv(initial_investment, annual_savings, discount_rate=0.10):
    """Net Present Value for post-acquisition cloud savings."""
    npv = -initial_investment
    for year, savings in enumerate(annual_savings, start=1):
        npv += savings / (1 + discount_rate) ** year
    return npv


def calculate_payback(initial_investment, annual_savings):
    """Payback period in years (fractional)."""
    cumulative = -initial_investment
    for year, savings in enumerate(annual_savings, start=1):
        cumulative += savings
        if cumulative >= 0:
            previous = cumulative - savings
            fraction = -previous / savings
            return year - 1 + fraction
    return float('inf')




# Assumptions matching dashboard narrative:
# - Net upfront investment: ~$1M (quick wins in Phase 1 offset most costs)
# - Year 1 savings: $4.5M (accelerated from $3.6M quick wins + early ramp)
# - Years 2–5: full $8.8M annual run-rate savings
savings_stream = [4500000, 8800000, 8800000, 8800000, 8800000]  # Y1–Y5

npv = calculate_npv(1000000, savings_stream)
print(f"5-Year NPV: ${npv:,.0f}")                # ≈ $32.7M (minor rounding variance possible)

payback = calculate_payback(1000000, savings_stream)
print(f"Payback period: {payback:.2f} years (~{int(payback * 12)} months)")  # ≈ 1.17 years / 14 months


###Sample Output when run:
5-Year NPV: $31,631,651
Payback period: 1.17 years (~14 months)

# How to Use These Datasets:In Tableau: Connect → Text/CSV → drag fields to build/recreate views (e.g., Annual_Cost by Cloud_Provider for multi-cloud bars).

import pandas as pd

# Example: Total waste from cost details
df_costs = pd.read_csv('ma_target_cloud_costs TAGM2.csv')
total_waste = df_costs['Waste_Amount'].sum()
print(f"Total identified waste: ${total_waste:,.0f}")  # Should ≈ $8.8M

# Example: Quick wins savings from roadmap
df_roadmap = pd.read_csv('ma_post_acquisition_roadmap TAGM.csv')
quick_wins = df_roadmap[df_roadmap['Phase'] == 'Phase 1']['Annual_Savings'].sum()
print(f"Phase 1 quick wins annualized: ${quick_wins:,.0f}")  # ≈ $3.6M

# Example: Top issues by impact
df_issues = pd.read_csv('ma_optimization_analysis TAGM.csv')
print(df_issues.sort_values('Annual_Cost_Impact', ascending=False).head(3)[['Issue_Description', 'Annual_Cost_Impact']])









