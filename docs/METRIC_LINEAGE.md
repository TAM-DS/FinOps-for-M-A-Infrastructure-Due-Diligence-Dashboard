# Metric Lineage

All dollar values are synthetic scenario values.

## Target infrastructure evidence

### Annual cloud run rate

```text
SUM(target_cloud_costs.Annual_Cost)
= $17,040,000
```

Every row is also validated as:

```text
Annual_Cost = Monthly_Cost × 12
```

### Gross waste exposure

```text
SUM(target_cloud_costs.Waste_Amount)
= $8,835,600
```

### Waste percentage

```text
$8,835,600 / $17,040,000
= 51.9%
```

### Residual run rate if all gross waste were removed

```text
$17,040,000 - $8,835,600
= $8,204,400
```

## Actionable remediation evidence

### Modeled savings backlog

```text
SUM(optimization_analysis.Savings_Potential)
= $7,805,800
```

### Quick-win opportunity

Rows where `Quick_Win == "Yes"`:

```text
SUM(Savings_Potential)
= $3,609,600
```

### Unbooked gross-waste gap

```text
$8,835,600 - $7,805,800
= $1,029,800
```

This amount is not included in the value-creation model.

## Roadmap reconciliation

The roadmap contains summary rows and executable child rows. After excluding the documented summary initiatives:

```text
SUM(executable_roadmap.Annual_Savings)
= $7,805,800
```

That exactly reconciles to the optimization analysis.

Modeled executable implementation cost:

```text
SUM(executable_roadmap.Implementation_Cost)
= $1,066,000
```

## Staged Year-1 savings

For each executable initiative:

```text
completion_month_offset = (Start_Month - 1) + Duration_Months
active_months_in_year_1 = MAX(0, 12 - completion_month_offset)
year_1_savings = Annual_Savings × active_months_in_year_1 / 12
```

Summed across executable initiatives:

```text
Year-1 staged savings
= $5,676,190
```

This is a scenario assumption: savings begin immediately when an initiative completes and accrue linearly afterward.

## Five-year NPV scenario

Inputs:

```text
Initial implementation cost = $1,066,000
Year 1 savings             = $5,676,190
Years 2–5 savings          = $7,805,800 per year
Discount rate              = 10%
```

Formula:

```text
NPV = -initial_cost + Σ(year_savings / (1 + discount_rate)^year)
```

Result:

```text
5-year NPV = $26,588,114.27
```

The NPV is a **financial scenario**, not source evidence and not an automatic valuation adjustment.
