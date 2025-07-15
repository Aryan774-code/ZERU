# Credit Score Model - Analysis and Documentation

## ✅ Purpose
This model assigns a **credit score (0–1000)** to wallets using historical Aave V2 transaction data.  
Higher scores indicate reliable, responsible users; lower scores suggest riskier, exploitative, or bot-like behavior.

---

## ✅ Features Engineered
For each wallet, we aggregate its raw transaction history into meaningful features:

| Feature                    | Description                                                      |
|----------------------------|------------------------------------------------------------------|
| n_deposit                  | Count of deposit transactions                                    |
| n_borrow                   | Count of borrow transactions                                     |
| n_repay                    | Count of repay transactions                                      |
| n_liquid                   | Count of liquidation events                                      |
| amt_deposit (USD)          | Total USD value of deposits                                      |
| amt_borrow (USD)           | Total USD value of borrows                                       |
| amt_repay (USD)            | Total USD value of repayments                                    |
| active_days                | Days active between first and last transaction                  |
| borrow_to_deposit_ratio    | amt_borrow / (amt_deposit + 1)                                   |
| repayment_ratio            | amt_repay / (amt_borrow + 1)                                     |
| liquidation_rate           | n_liquid / (n_borrow + 1)                                        |

✅ Amounts are normalized to USD using the `assetPriceUSD` in the raw data.  
✅ Transaction amounts are decoded from raw token units using 6 decimal assumption (e.g. for USDC).

---

## ✅ Scoring Formula

Each wallet gets a **score from 0 to 1000** based on:

score = 1000

300 * liquidation_rate

200 * max(0, borrow_to_deposit_ratio - 1)

200 * (1 - min(1, repayment_ratio))

100 if active_days < 2

50 * log(1 + amt_deposit)


### Explanation:

- **Liquidation penalty**: High liquidation_rate = big risk = big score reduction.
- **Over-borrowing penalty**: borrow_to_deposit_ratio > 1 signals over-leverage.
- **Repayment quality**: Low repayment_ratio suggests default or poor behavior.
- **Bot activity penalty**: Very short active_days (<2) suggests exploitative use.
- **Deposit reward**: Larger total deposits boost score via log scaling.

---

## ✅ Example Interpretation

| Wallet Address                          | Score | Notes                                      |
|-----------------------------------------|-------|--------------------------------------------|
| 0xabc...                                | 910   | Good repayment, low liquidation, high deposit. |
| 0xdef...                                | 420   | High borrow relative to deposit, some liquidation. |
| 0xghi...                                | 150   | No repayments, liquidated often, bot-like activity. |

---

## ✅ Design Goals
✅ Simple, transparent rule-based system.  
✅ Explainable: weights and penalties are visible in formula.  
✅ Extensible for ML training later.  

---

## ✅ Limitations
⚠️ Assumes 6 decimals for tokens – correct for USDC, not always true.  
⚠️ Prices from assetPriceUSD may vary in quality depending on data source.  
⚠️ No time-series or collateralization ratio modeling.  
⚠️ No risk-adjusted asset differentiation (DAI vs volatile tokens).

---

## ✅ Future Improvements
- Add token decimal mapping per asset.  
- Include time-series features (e.g. time between borrows and repayments).  
- Use ML models with labeled data for training better scoring functions.  
- Handle multi-chain, multi-protocol data sources.  
- Expose as an API or web dashboard for real-time scoring.

---

## ✅ How to Use
or use `example_notebook.ipynb` for interactive analysis.

---

## ✅ License / Ownership
This scoring logic is for educational and research use.  
Feel free to fork, modify, and extend it for your own DeFi risk analysis projects.

