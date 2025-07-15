import json
import sys
import pandas as pd
from creditscore import aggregate_features, score_wallet

def main():
    if len(sys.argv) != 3:
        print("Usage: python cli.py input.json output.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, "r") as f:
        records = json.load(f)

    features = aggregate_features(records)

    rows = []
    for wallet, feat in features.items():
        wallet_score = score_wallet(feat)
        row = {"wallet": wallet, "score": wallet_score}
        row.update(feat)
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(output_file, index=False)
    print(f"✅ Scoring complete. Results saved to {output_file}")

if __name__ == "__main__":
    main()
