# Assumptions and Decision Boundaries

This repository is a synthetic M&A infrastructure due-diligence case study. The purpose of this document is to prevent scenario assumptions from being mistaken for measured facts.

## Evidence hierarchy

### 1. Source evidence

These values come directly from the committed synthetic source files:

- annual cloud cost by provider, service, environment, and category;
- row-level waste amount;
- optimization issue classifications;
- savings-potential fields;
- implementation timing and cost fields.

### 2. Derived evidence

These values are deterministic arithmetic over source evidence:

- total annual spend;
- gross waste exposure;
- waste percentage;
- residual run rate after gross waste removal;
- provider and environment concentration;
- total actionable savings backlog;
- quick-win savings total.

### 3. Financial scenario assumptions

The NPV model introduces assumptions that are not observed facts:

- implementation costs are treated as modeled roadmap costs;
- benefits begin when each executable initiative completes;
- Year-1 benefit is prorated for the remaining portion of the year;
- Years 2–5 receive the full reconciled annual savings opportunity;
- the discount rate is 10%.

Changing any of these assumptions changes the financial result.

### 4. Deal-team judgment

The model does **not** determine:

- purchase-price adjustment;
- valuation multiple;
- transaction structure;
- probability of successful remediation;
- tax effects;
- financing effects;
- synergy overlap;
- go / no-go outcome.

Those are human deal decisions informed by diligence evidence.

## Gross waste vs. actionable savings

The target-cost inventory identifies **$8.8356M** in gross waste exposure.

The optimization analysis identifies **$7.8058M** in modeled savings potential.

The **$1.0298M difference remains unbooked** rather than being forced into the value-creation case.

## Roadmap aggregation control

The source roadmap contains both summary initiatives and their child initiatives. Summing every row would double count savings and implementation costs.

The analytical model explicitly excludes these summary rows from executable financial calculations:

- Quick Wins Package
- Reserved Instance Strategy
- Right-Sizing Program
- Implement Auto-Scaling
- Storage Optimization
- Multi-Cloud Consolidation
- Network Architecture Redesign
- Cost Governance Implementation

Only executable leaf initiatives are used for reconciliation and financial modeling.

## Synthetic benchmark file

`industry_benchmarks.csv` is scenario material created for this case study. Its values are **not current external industry benchmarks** and should not be cited as such.
