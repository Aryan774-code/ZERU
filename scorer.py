import math
from collections import defaultdict

def parse_usd_amount(tx):
    try:
        data = tx.get('actionData', {})
        raw_amount = float(data.get('amount', 0))
        price_usd = float(data.get('assetPriceUSD', 1.0))
        token_amount = raw_amount / 1e6
        amount_usd = token_amount * price_usd
        return amount_usd
    except Exception as e:
        return 0.0

def aggregate_features(records):
    per_wallet = defaultdict(list)
    for tx in records:
        wallet = tx.get('userWallet')
        if wallet:
            per_wallet[wallet].append(tx)

    features = {}
    for wallet, txs in per_wallet.items():
        n_deposit = n_borrow = n_repay = n_redeem = n_liquid = 0
        amt_deposit = amt_borrow = amt_repay = 0
        timestamps = []

        for tx in txs:
            usd_amount = parse_usd_amount(tx)
            timestamps.append(tx.get('timestamp', 0))
            action = tx.get('action', '').lower()

            if action == 'deposit':
                n_deposit += 1
                amt_deposit += usd_amount
            elif action == 'borrow':
                n_borrow += 1
                amt_borrow += usd_amount
            elif action == 'repay':
                n_repay += 1
                amt_repay += usd_amount
            elif action == 'redeemunderlying':
                n_redeem += 1
            elif action == 'liquidationcall':
                n_liquid += 1

        if timestamps:
            active_days = max(1, (max(timestamps) - min(timestamps)) // (24 * 3600))
        else:
            active_days = 1

        borrow_to_deposit_ratio = amt_borrow / (amt_deposit + 1)
        repayment_ratio = amt_repay / (amt_borrow + 1)
        liquidation_rate = n_liquid / (n_borrow + 1)

        features[wallet] = {
            'n_deposit': n_deposit,
            'n_borrow': n_borrow,
            'n_repay': n_repay,
            'n_liquid': n_liquid,
            'amt_deposit': amt_deposit,
            'amt_borrow': amt_borrow,
            'amt_repay': amt_repay,
            'active_days': active_days,
            'borrow_to_deposit_ratio': borrow_to_deposit_ratio,
            'repayment_ratio': repayment_ratio,
            'liquidation_rate': liquidation_rate
        }

    return features

def score_wallet(feat):
    score = 1000
    score -= 300 * feat['liquidation_rate']
    score -= 200 * max(0, feat['borrow_to_deposit_ratio'] - 1)
    score -= 200 * (1 - min(1, feat['repayment_ratio']))
    if feat['active_days'] < 2:
        score -= 100
    score += 50 * math.log(1 + feat['amt_deposit'])
    return max(0, min(1000, round(score)))
