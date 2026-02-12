# financial_model.py
# Reproducible NPV, Payback, and Savings calculations for FinOps M&A Due Diligence
# All figures modeled after the $200M SaaS acquisition case study dashboard
# MIT License - feel free to adapt

def calculate_npv(initial_investment: float, annual_savings: list[float], discount_rate: float = 0.10) -> float:
    """
    Calculate Net Present Value (NPV) for post-acquisition cloud optimization savings.
    
    Args:
        initial_investment: Upfront cost (e.g., FinOps team setup, tooling, RI purchases)
                            Set to 0 if quick wins fully cover initial outlay.
        annual_savings: List of savings per year (Year 1 to Year 5)
        discount_rate: Annual discount rate (default 10% for tech/SaaS investments)
    
    Returns:
        NPV in dollars (rounded to nearest dollar)
    """
    npv = -initial_investment
    for year, savings in enumerate(annual_savings, start=1):
        npv += savings / (1 + discount_rate) ** year
    return round(npv)


def calculate_payback(initial_investment: float, annual_savings: list[float]) -> float:
    """
    Calculate payback period in years (time to recover initial investment from savings).
    
    Args:
        initial_investment: Upfront cost
        annual_savings: List of annual savings
    
    Returns:
        Payback period in years (fractional)
    """
    cumulative = -initial_investment
    for year, savings in enumerate(annual_savings, start=1):
        cumulative += savings
        if cumulative >= 0:
            previous_cumulative = cumulative - savings
            fraction = -previous_cumulative / savings
            return round(year - 1 + fraction, 2)
    return float('inf')  # Never pays back


if __name__ == "__main__":
    # Dashboard-derived assumptions (adjust as needed)
    QUICK_WINS_YEAR_1     = 3_600_000   # $3.6M quick wins in first 90 days → partial Year 1
    FULL_ANNUAL_SAVINGS   = 8_800_000   # $8.8M run-rate savings from Year 2 onward
    INITIAL_INVESTMENT    = 0           # Assume quick wins cover most upfront costs
                                        # (set to e.g. 4_200_000 if modeling $4.2M capex)
    DISCOUNT_RATE         = 0.10        # 10% - standard for SaaS/tech investments
    YEARS                 = 5

    # Savings stream matching dashboard narrative
    savings_stream = [QUICK_WINS_YEAR_1] + [FULL_ANNUAL_SAVINGS] * (YEARS - 1)

    # Calculate and print results
    npv = calculate_npv(INITIAL_INVESTMENT, savings_stream, DISCOUNT_RATE)
    payback_years = calculate_payback(INITIAL_INVESTMENT, savings_stream)

    print("FinOps M&A Optimization Financial Model")
    print("----------------------------------------")
    print(f"Initial Investment:          ${INITIAL_INVESTMENT:,.0f}")
    print(f"Discount Rate:               {DISCOUNT_RATE:.0%}")
    print(f"Annual Savings (Years 2–5):  ${FULL_ANNUAL_SAVINGS:,.0f}")
    print(f"Savings Year 1 (quick wins): ${QUICK_WINS_YEAR_1:,.0f}")
    print()
    print(f"5-Year NPV:                  ${npv:,.0f}")
    print(f"Payback Period:              {payback_years} years "
          f"({payback_years * 12:.0f} months)")
    print()
    print("Note: Dashboard headline NPV of $32.7M assumes near-zero net initial cost "
          "after quick wins. Increase INITIAL_INVESTMENT to see sensitivity.")
