# A hands-on project that merges my passion for space exploration with in-depth financial analysis.

orbital-habitat-finance
# Capital Stacks and IRR Analysis: Financing a 10-Person Orbital Habitat

# **Thesis Question:**  
How do different financing structures (100% equity, 70/30 senior–equity, and a 70/15/15 senior–mezzanine–equity stack) affect project returns (IRR), debt‐service coverage (DSCR), and sponsor risk in a 3-year model?

---

## 📂 Repository Structure

orbital-habitat-finance/
├── model/
│ ├── init.py
│ ├── assumptions.py # all inputs & ratios (CapEx, rates, tenor, etc.)
│ └── dcf_model.py # builds DCF, waterfalls, DSCR, IRR, sensitivity
├── Google Docs PDF/
└── README.md # this file

# Quickstart & Usage
1) Clone the repo:
bash
git clone https://github.com/<adityaup19>/orbital-habitat-finance.git
cd orbital-habitat-finance

2) Install dependencies:
bash
pip install -r requirements.txt

3) Run the Base model
bash

py -m model.dcf_model
This will print:

Unlevered DCF (100% equity baseline)

Debt‐Service Coverage Ratio (DSCR) for your capital stack

Levered Equity IRR for the 70/15/15 stack

Sensitivity table of unlevered NPV across utilization & ticket pricing

# Switch scenarios

Open model/assumptions.py, change:

FINANCE['tenor'] = 3  # or 5
Rerun py -m model.dcf_model to compare 3-year vs 5-year debt bullets.

 # Key Findings (Examples)
Unlevered IRR: 3.5%

- 70/30 Senior–Equity IRR (3-yr): –27.9%, Year 3 DSCR ≈ 0.08×

- 70/15/15 Senior–Mezz–Equity IRR (3-yr): –65.6%, Year 3 DSCR ≈ 0.08×

- 70/15/15 Senior–Mezz–Equity IRR (5-yr): +44.2%, Year 3 DSCR ≈ 0.94×

Break-even Sensitivity: NPV ≥ 0 only at ≥ 70 % utilization & ≥ $7 M ticket price

# See the project report up in the attached Google Doc PDF

# Next Steps
- Experiment with different senior/mezz ratios (e.g., 60/20/20)

- Add DSCR covenants or stress-test with Monte Carlo on revenue

- Build a small investor pitch deck with these charts

**This work is released under the MIT License. Feel free to reuse or adapt for your portfolio.**

# Created by Aditya Upadhyay 



