# FinOps M&A: Infrastructure Due Diligence Framework
### Turning Cloud Waste into Negotiation Power

---

> **"The infrastructure was described as optimized. It wasn't.**
> **56% of $17M in annual cloud spend was waste.**
> **This dashboard found it — before the deal closed."**

---

## The Problem Nobody Talks About in M&A

When PE firms and acquirers evaluate a $200M SaaS target, they scrutinize revenue, churn, and EBITDA.

They rarely scrutinize cloud infrastructure.

That's expensive.

A target claiming "optimized infrastructure" at $17M annual cloud spend was running:
- Dev and staging environments **24/7** — $2.88M in waste
- **90% on-demand instances** when 60% reserved is industry standard — $1.95M in avoidable cost
- Oversized compute nobody had reviewed in months — $1.24M
- Cross-region egress charges nobody had flagged — $816K

**Total waste identified: $8.8M per year. 56% of total spend.**

This project is the framework that found it.

---

## What This Project Actually Is

This isn't a Tableau showcase.

It's a **CFO-grade acquisition intelligence tool** that translates cloud infrastructure waste into P&L impact, valuation adjustments, and post-close value creation — built for PE diligence teams, CTOs, and FinOps leaders who need answers before the wire transfer clears.

**The output isn't pretty charts. It's negotiation leverage.**

---

## Key Outcomes

| Metric | Value |
|--------|-------|
| Annual cloud spend (pre-optimization) | $17.0M |
| Waste identified | $8.8M (56% of spend) |
| Optimized steady-state run rate | $8.2M/year |
| Recommended valuation haircut | **$15M** |
| 5-Year NPV (post-acquisition value creation) | **$32.7M** |
| Payback period | **~14 months** |
| First-90-day quick wins | $3.6M annualized |

---

## The Dashboard: Three Acts

Built as a narrative — not a report. Because PE partners and CTOs don't read reports. They follow stories.

### Act 1 — The $8.8M Question
*Home: Challenging "optimized infrastructure" claims before anyone believes them*

- Cost per customer: **$250/mo** (industry benchmark: $80–$120)
- Cloud as % of revenue: **30%** (industry benchmark: 12%)
- Reserved instance coverage: **10%** (industry standard: 60%)
- Multi-cloud breakdown: AWS $10.3M | GCP $5.5M | Azure $1.2M

### Act 2 — Post-Acquisition: Unlocking the Value
*Red flags, quick wins, and the financial model that changes the negotiation*

- 5-Year NPV: $32.7M at conservative 10% discount rate
- Top waste categories by severity — EC2 compute and data transfer flagged critical
- Ongoing tech debt exposure: ~$1.2M/year in untagged resources and sprawl

### Act 3 — The Roadmap: Capturing $8.8M
*12-month phased implementation — low risk first, quick wins funding everything else*

- **Phase 1 (Months 1–3):** Governance + quick wins → $3.6M annualized, low risk
- **Phase 2 (Months 2–4):** Reserved instances + right-sizing → $2M
- **Phases 3–4:** Consolidation, auto-scaling, architecture redesign → $3.2M cumulative

---

## Why This Approach Is Different

Most infrastructure audits answer: *"How much are we spending?"*

This framework answers: *"How much should we be spending — and what does the gap cost us in valuation?"*

That shift — from technical audit to financial instrument — is what makes infrastructure due diligence actually useful in an M&A context.

---

## Tech Stack

| Layer | Tools |
|-------|-------|
| Visualization & Storytelling | Tableau Public |
| Financial Modeling | Python (NumPy, Pandas) |
| Data | 4 synthetic CSV datasets (realistic AWS/GCP/Azure billing patterns) |
| Reproducibility | Full Python NPV/payback functions included |

---

## Reproducible Financial Models

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

# Conservative assumptions matching dashboard narrative
savings_stream = [4500000, 8800000, 8800000, 8800000, 8800000]  # Y1–Y5

npv = calculate_npv(1000000, savings_stream)
print(f"5-Year NPV: ${npv:,.0f}")         # ≈ $32.7M
payback = calculate_payback(1000000, savings_stream)
print(f"Payback period: {payback:.2f} years (~{int(payback * 12)} months)")  # ≈ 14 months
```

---

## Dataset Overview

All data is fully synthetic — generated to mimic realistic multi-cloud billing patterns from a mid-sized SaaS company. No real account info, costs, or identifiers.

| File | Description | Rows |
|------|-------------|------|
| `ma_target_cloud_costs.csv` | Monthly/annual costs by service, provider, environment, waste flags | ~40 |
| `ma_post_acquisition_roadmap.csv` | Phased initiatives with timeline, savings, cost, risk level | ~35 |
| `ma_optimization_analysis.csv` | Red flags, severity, quick wins, savings potential | ~15 |
| `ma_industry_benchmarks.csv` | Target vs. industry vs. best-in-class comparison | ~15 |

---

## Who This Is Built For

This framework is immediately applicable for:

- **PE firms** evaluating infrastructure liability in SaaS acquisitions
- **CTOs** inheriting cloud environments post-close
- **FinOps leaders** building diligence capabilities from scratch
- **CFOs** who need infrastructure risk translated into financial language

---

## The Bigger Picture

I build data infrastructure from scratch — petabyte-scale lakes, medallion architecture, autonomous AI systems running in live financial markets.

This project sits at the intersection of everything I care about:

**Customer problems → Data infrastructure → Financial outcomes.**

Cloud waste isn't a technical problem. It's a business problem wearing a technical disguise.

This framework rips off the disguise.

---

*Built by Tracy | Apex Engineering*
*[LinkedIn](https://www.linkedin.com/in/tracymanning/) | [Tableau Dashboard](https://public.tableau.com/app/profile/tagm/vizzes)*
