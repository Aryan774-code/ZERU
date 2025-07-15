# Credit Score for Aave V2 Users

This package assigns credit scores (0-1000) to DeFi wallets based on Aave V2 transaction history.

## Structure

- creditscore/: Core scoring logic as a Python package
- cli.py: Command-line runner
- example_notebook.ipynb: Interactive analysis
- sample_data.json: Example input

## How to Use

### 1. Install

### 2. CLI

### 3. Notebook
Open `example_notebook.ipynb` in Jupyter.

## Scoring Formula
score = 1000

300 * liquidation_rate

200 * max(0, borrow_to_deposit_ratio - 1)

200 * (1 - repayment_ratio)

100 if active_days < 2

50 * log(1 + amt_deposit)

- Liquidations penalized
- Over-borrowing penalized
- Poor repayments penalized
- Bot-like behavior penalized
