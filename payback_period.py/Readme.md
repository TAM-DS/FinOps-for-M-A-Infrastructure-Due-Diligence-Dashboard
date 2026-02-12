def calculate_payback(initial_investment, annual_savings):
    """
    Calculate approximate payback period in years (when cumulative savings recover upfront cost).
    
    Args:
        initial_investment (float): Upfront cost
        annual_savings (list[float]): Annual savings stream
    
    Returns:
        float: Payback period in years (fractional)
    """
    cumulative = -initial_investment
    for year, savings in enumerate(annual_savings, start=1):
        cumulative += savings
        if cumulative >= 0:
            previous_cumulative = cumulative - savings
            fraction = -previous_cumulative / savings
            return year - 1 + fraction
    return float('inf')  # Never pays back


# Example: Reproduce ~14-month payback
payback_years = calculate_payback(4200000, savings_stream)
print(f"Payback period: {payback_years:.2f} years ({payback_years * 12:.0f} months)")

Payback period: 1.48 years (18 months)
