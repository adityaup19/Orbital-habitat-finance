# model/assumptions.py

# 1. Timeline: Year 0 setup + 3 years of operations
YEARS = [0, 1, 2, 3]

# 2. CapEx (build costs)
CAPEX = {
    0: 200e6,  # $200 million in Year 0
    1: 50e6    # leftover in Year 1
}

# 3. OpEx (annual O&M)
OPEX_PER_YEAR = 10e6  # $10 million/year

# 4. Revenue drivers
REVENUE = {
    'microgravity_fee_per_month': 2e6,  # per module-month
    'microgravity_utilization': 0.5,    # 50% utilization
    'tourist_ticket_price': 5e6,        # per tourist
    'tourist_volume': 4                 # tourists per year
}

# 5. Financing terms (70% debt / 30% equity)
FINANCE = {
    'debt_ratio': 0.7,
    'equity_ratio': 0.3,
    'debt_rate': 0.08,       # 8% annual
    'debt_tenor': 3,         # years
    'debt_amort': 'bullet'   # interest-only, principal at maturity
}

# 6. Discount rate & tax
DISCOUNT_RATE = 0.10  # 10%
TAX_RATE = 0.21       # 21%

# 7. Terminal growth (for terminal value)
TERMINAL_GROWTH = 0.02

# model/assumptions.py
# … your existing constants …

# 5. Financing terms: Senior debt, mezzanine, equity
FINANCE = {
    'senior_ratio': 0.70,
    'mezz_ratio':   0.15,
    'equity_ratio': 0.15,
    'senior_rate':  0.08,
    'mezz_rate':    0.12,
    'tenor': 5,  # I am extending debt to 5-year
    'amort':        'bullet'
}
