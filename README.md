# FinOps for M&A: Infrastructure Due Diligence Dashboard

**Quantifying Cloud Waste as Acquisition Liability – Turning Hidden Costs into Measurable Alpha**

**$200M SaaS Acquisition Case Study**  
- Claimed run rate: **$17.0M** annual cloud spend  
- Identified waste: **$8.8M/year** (56% of spend)  
- True optimized run rate: **$8.2M**  
- Recommended valuation adjustment: **$15M downward**  
- Post-acquisition value creation: **$32.7M 5-year NPV** | **14-month payback** | **$3.6M quick wins** in first 90 days  

**Explore the full interactive dashboard:**  
**[Live Tableau Public Viz →](https://tinyurl.com/47b3z559)**  
(Click to filter by provider, category, phase; drill into metrics, tooltips, and benchmarks.)

> All data is **fully synthetic and anonymized** — modeled on realistic multi-cloud (AWS/GCP/Azure) patterns with **no real PII**, account IDs, company names, or proprietary billing information. Safe for public sharing, adaptation, and portfolio demonstration.

## Dashboard Narrative & Structure
Three-act executive flow built in Tableau:

1. **Home – "The $8.8M Question: Is This Acquisition Worth It?"**  
   Challenges "optimized infrastructure" claims with high-level spend vs. benchmarks.  
   - **Annual Cloud Spend**: **$17.0M** total highlighted.  
   - **Target vs. Industry Benchmark**: Bar charts showing cost per customer monthly (**$250** vs. industry **$120–$80**), waste percentage (**58%** vs. **25%** best-in-class), cloud spend as % of revenue (**30%** vs. industry **12%**).  
   - **Multi-Cloud Distribution**: Stacked bars – AWS **$10.3M** (dominant), GCP **$5.5M**, Azure **$1.2M**.  
   - **Identified Waste**: **$8.8M** callout (56%).  
   - **True Run Rate & Value Add**: After optimization → **$8.2M** run rate, **$8.8M/year** savings opportunity.  
   - Visuals: Gauges, bar comparisons, rectangular treemap-style breakdowns for environments (Production suboptimal **$5.7M**, Development high waste **$4.1M**, Staging **$1.2M**).  
   - **Waste by Category**: Large rectangular treemap – Compute **$4.5M** (purple dominant), Storage **$1.4M**, Analytics **$0.02M**, Network **$1.4M**, Cache **$0.1M**.

2. **Post-Acquisition – "The $8.8M Answer: Unlocking Value"**  
   Deep dive on red flags, quick wins, tech debt, and NPV modeling.  
   - **5-Year NPV Impact**: **$32.7M** headline.  
   - **Payback Period**: **14 months**.  
   - **Quick Wins**: **$3.6M/year** (e.g., shutdown dev/staging 24/7 → **$2.88M**, RI quick package → **$2.8M**).  
   - **Red Flags Bar Chart**: Top issues like 24/7 dev/staging (**$2.88M**), 90% on-demand (**$1.95M**), oversized compute (**$1.24M**), cross-region transfer (**$816K**).  
   - **Reserved vs. On-Demand Analysis**: Gap bars – Target **90% on-demand** vs. industry **40%** average; reserved coverage **10%** vs. **60%**.  
   - **Service Level Waste**: Horizontal bars with severity (High/Critical purple) – EC2 Compute **$1.33M high waste**, Data Transfer **$1.26M**, etc.  
   - **Tech Debt**: **$1.2M/year** ongoing (e.g., untagged resources, multi-cloud sprawl, old snapshots).

3. **Roadmap – "How We Capture $8.8M: Implementation Timeline"**  
   Phased 12-month plan with risk/effort scoring and cumulative savings.  
   - **Optimization Roadmap Timeline**: Gantt-like horizontal bars showing initiatives across months 1–9 (e.g., Cost Governance blue ongoing, Reserved Instances red Phase 2, Auto-Scaling green Phase 3–4).  
   - Savings stacked by phase: Phase 1 quick wins **$3.6M** (low risk), Phase 2 **$2M** (medium), Phase 3 **$2.2M** (medium-high), Phase 4 **$0.8M** (high).  
   - **Implementation Guide Sidebar**: Findings recap, execution strategy (hire FinOps lead, executive sponsorship), critical success factors, risks (**$1.2M/year tech debt**), recommendation (**$15M valuation adjustment**).  
   - Color coding: Blue (ongoing), Orange/Red (Phase 1–2), Green (Phase 3–4).

## Key Business & Technical Takeaways
- Bridges financial + technical due diligence: Translates infra waste into **P&L/valuation impact**.  
- Multi-cloud benchmarking exposes hidden liabilities (e.g., **2.5×** industry spend %).  
- Phased roadmap prioritizes low-risk quick wins to fund transformation.  
- Demonstrates senior FinOps skills: Cost modeling, NPV/ROI/payback, governance recommendations, executive storytelling via Tableau.

## Tech Stack & Repo Contents
- **Visualization**: Tableau Desktop/Public (.twbx workbooks)  
- **Data**: Synthetic CSVs (raw spend, waste categories, benchmarks, roadmap)  
- **Files**:  
  - `ma_target_cloud_costs_TAGM2.csv`  
  - `ma_optimization_analysis_TAGM.csv`  
  - `ma_industry_benchmarks_TAGM.csv`  
  - `ma_post_acquisition_roadmap_TAGM.csv`  
  - Tableau workbooks (upload your .twbx if sharing source)

## Setup & Exploration
1. Clone: `git clone https://github.com/TAM-DS/FinOps-M-A-focused-Infrastructure-Due-Diligence-dashboard.git`  
2. Open .twbx in Tableau Desktop or view live on Tableau Public.  
3. Interact: Filter providers/categories, hover for details.

## Reproducible Financial Modeling in Python

The dashboard's NPV, payback, and savings projections are based on standard discounted cash flow models. Below are clean Python snippets to reproduce them exactly (or adapt for other scenarios).

### 1. NPV Calculation (Core Function)
Uses basic Python (no external libraries needed) to compute NPV from a list of cash flows.

```python
def calculate_npv(initial_investment, annual_savings, discount_rate=0.10):
    """
    Calculate Net Present Value (NPV) for post-acquisition savings.
    
    Args:
        initial_investment (float): Upfront cost (e.g., optimization capex)
        annual_savings (list[float]): List of annual cash inflows (savings)
        discount_rate (float): Discount rate (default 10%)
    
    Returns:
        float: NPV in dollars
    """
    npv = -initial_investment
    for year, savings in enumerate(annual_savings, start=1):
        npv += savings / (1 + discount_rate) ** year
    return npv


# Example: Reproduce ~$32.7M NPV
# - Assume quick wins ($3.6M) fund most initial costs → low effective upfront
# - Full $8.8M savings years 2–5
savings_stream = [3600000, 8800000, 8800000, 8800000, 8800000]  # Year 1 to 5
print(f"NPV: ${calculate_npv(0, savings_stream):,.0f}")         # ~$32.7M if minimal initial

# With assumed $4.2M initial investment (e.g., FinOps team, tooling)
print(f"NPV with $4.2M upfront: ${calculate_npv(4200000, savings_stream):,.0f}")'''



