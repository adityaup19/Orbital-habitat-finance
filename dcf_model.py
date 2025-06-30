
import pandas as pd
import numpy as np

import numpy_financial as nf


from model.assumptions import (
    YEARS,
    CAPEX,
    OPEX_PER_YEAR,
    REVENUE,
    FINANCE,
    DISCOUNT_RATE,
    TAX_RATE,
    TERMINAL_GROWTH
)

def project_cash_flows():
    rows = []
    for year in YEARS:
        capex = CAPEX.get(year, 0)
        opex  = OPEX_PER_YEAR if year >= 1 else 0

        if year >= 1:
            rev_micro = REVENUE['microgravity_fee_per_month'] * 12 * REVENUE['microgravity_utilization']
            rev_tour  = REVENUE['tourist_ticket_price']      * REVENUE['tourist_volume']
        else:
            rev_micro, rev_tour = 0, 0

        revenue = rev_micro + rev_tour
        ebit    = revenue - opex
        tax     = max(ebit, 0) * TAX_RATE
        nopat   = ebit - tax

        rows.append({
            'Year':    year,
            'CapEx':   -capex,
            'OpEx':    -opex,
            'Revenue':  revenue,
            'EBIT':     ebit,
            'Tax':     -tax,
            'NOPAT':    nopat
        })

    return pd.DataFrame(rows).set_index('Year')

def compute_free_cash_flow(df):
    # CapEx is negative, so adding to NOPAT yields correct FCF
    df['FCF'] = df['NOPAT'] + df['CapEx']
    return df

def add_terminal_value(df):
    last = df.index.max()
    tv = df.at[last, 'NOPAT'] * (1 + TERMINAL_GROWTH) / (DISCOUNT_RATE - TERMINAL_GROWTH)
    df.at[last, 'TerminalValue'] = tv
    return df

def build_combined_debt_schedule():
    total_capex = sum(CAPEX.get(y, 0) for y in YEARS)
    sr_amount   = total_capex * FINANCE['senior_ratio']
    mz_amount   = total_capex * FINANCE['mezz_ratio']
    sched       = []

    for year in YEARS:
        entry = {'Year': year}
        for name, amt, rate in (
            ('Snr', sr_amount, FINANCE['senior_rate']),
            ('Mz',  mz_amount,  FINANCE['mezz_rate'])
        ):
            if year == 0:
                balance = amt
                interest = principal = payment = 0.0
            elif 1 <= year <= FINANCE['tenor']:
                prev = sched[-1][f'DebtBalance_{name}']
                interest = prev * rate
                if year < FINANCE['tenor']:
                    principal, balance = 0.0, prev
                else:
                    principal, balance = prev, 0.0
                payment = interest + principal
            else:
                balance = interest = principal = payment = 0.0

            entry[f'DebtBalance_{name}'] = balance
            entry[f'Interest_{name}']    = interest
            entry[f'Principal_{name}']   = principal
            entry[f'Payment_{name}']     = payment

        entry['TotalPayment'] = entry['Payment_Snr'] + entry['Payment_Mz']
        sched.append(entry)

    return pd.DataFrame(sched).set_index('Year')

def main():
    # 1. Unlevered DCF
    df = project_cash_flows()
    df = compute_free_cash_flow(df)
    df = add_terminal_value(df)

    # 2. Combined debt schedule & merge
    debt = build_combined_debt_schedule()
    df = df.join(debt)

    # 2b. DSCR calculation
    df['DSCR'] = df['FCF'] / df['TotalPayment']

    # 3. Levered cash flows & equity IRR
    df['LeveredFCF'] = df['FCF'] - df['TotalPayment']
    total_equity = sum(CAPEX.get(y, 0) for y in YEARS) * FINANCE['equity_ratio']

    eq_cf = [-total_equity]
    for year in YEARS[1:]:
        levered = df.at[year, 'LeveredFCF']
        if year == YEARS[-1]:
            levered += df.at[year, 'TerminalValue']
        eq_cf.append(levered)

    # 4. Metrics using numpy_financial
    cf_unlev = df['FCF'].tolist()
    cf_unlev[-1] += df.at[YEARS[-1], 'TerminalValue']

    unlev_npv   = nf.npv(DISCOUNT_RATE, cf_unlev)
    unlev_irr   = nf.irr(cf_unlev)
    levered_irr = nf.irr(eq_cf)

    # 5. Print results
    print("\n=== Unlevered DCF ===")
    print(df[['CapEx','OpEx','Revenue','NOPAT','FCF','TerminalValue']])
    print(f"NPV (unlevered): ${unlev_npv/1e6:.1f}M   IRR: {unlev_irr*100:.1f}%")

    print("\n=== Debt Service Coverage Ratio (DSCR) ===")
    print(df[['FCF','TotalPayment','DSCR']])

    print("\n=== Levered Equity IRR ===")
    print(df[['LeveredFCF']])
    print(f"Equity IRR (70/15/15 stack): {levered_irr*100:.1f}% on equity outlay ${total_equity/1e6:.1f}M")

if __name__ == "__main__":
    main()

