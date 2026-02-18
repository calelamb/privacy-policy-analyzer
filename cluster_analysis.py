"""
Cluster analysis and compliance scoring for analyzed privacy policies.

Clusters policies using KMeans on 8 disclosure columns, computes a compliance
score from 13 boolean columns, and outputs an augmented CSV.
"""

import argparse
import os
import sys

import pandas as pd
from sklearn.cluster import KMeans

CLUSTERING_COLUMNS = [
    "data_collection_disclosure",
    "data_use_purpose_specification",
    "third_party_sharing_disclosure",
    "tracking_technologies_disclosure",
    "data_retention_policy",
    "user_data_rights",
    "data_security_encryption",
    "parental_consent_mechanism",
]

SCORING_COLUMNS = CLUSTERING_COLUMNS + [
    "coppa_ferpa_compliance_mention",
    "coppa_mentions",
    "coppa_claims_compliance",
    "gdpr_mentions",
    "gdpr_claims_compliance",
]


def _coerce_to_bool(series: pd.Series) -> pd.Series:
    """Convert a column with mixed types (string, numeric, NaN) to boolean."""
    def _convert(val):
        if pd.isna(val):
            return False
        if isinstance(val, bool):
            return val
        if isinstance(val, str):
            return val.strip().lower() == "true"
        return bool(val)

    return series.map(_convert).astype(bool)


def load_and_validate(input_path: str) -> pd.DataFrame:
    """Read the CSV and validate that all required columns are present."""
    df = pd.read_csv(input_path)

    missing = [c for c in SCORING_COLUMNS if c not in df.columns]
    if missing:
        print(f"Error: missing columns in input CSV: {missing}", file=sys.stderr)
        sys.exit(1)

    for col in SCORING_COLUMNS:
        df[col] = _coerce_to_bool(df[col])

    return df


def run_clustering(df: pd.DataFrame) -> pd.DataFrame:
    """Run KMeans clustering on the 8 disclosure columns."""
    X = df[CLUSTERING_COLUMNS].fillna(0).astype(int)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["compliance_cluster"] = kmeans.fit_predict(X)
    return df


def compute_compliance_score(df: pd.DataFrame) -> pd.DataFrame:
    """Compute a per-row compliance score as a percentage of 13 booleans."""
    df["compliance_score"] = (
        df[SCORING_COLUMNS].fillna(False).astype(int).sum(axis=1) / len(SCORING_COLUMNS) * 100
    ).round(2)
    return df


def print_summary(df: pd.DataFrame) -> None:
    """Print cluster sizes, per-cluster average scores, and disclosure rates."""
    print("\n=== Cluster Analysis Summary ===\n")

    print("Cluster sizes:")
    sizes = df["compliance_cluster"].value_counts().sort_index()
    for cluster, count in sizes.items():
        print(f"  Cluster {cluster}: {count} policies")

    print(f"\n  Total: {len(df)} policies\n")

    print("Per-cluster average compliance score:")
    for cluster in sorted(df["compliance_cluster"].unique()):
        avg = df.loc[df["compliance_cluster"] == cluster, "compliance_score"].mean()
        print(f"  Cluster {cluster}: {avg:.2f}%")

    print("\nPer-cluster disclosure rates:")
    for cluster in sorted(df["compliance_cluster"].unique()):
        subset = df[df["compliance_cluster"] == cluster]
        print(f"\n  Cluster {cluster}:")
        for col in CLUSTERING_COLUMNS:
            rate = subset[col].mean() * 100
            print(f"    {col}: {rate:.1f}%")


def save_output(original_df: pd.DataFrame, clustered_df: pd.DataFrame, output_path: str) -> None:
    """Merge cluster/score columns back onto the original DataFrame and save."""
    original_df["_row_idx"] = range(len(original_df))
    clustered_df["_row_idx"] = range(len(clustered_df))

    policies_updated = original_df.merge(
        clustered_df[["_row_idx", "app_id", "app_name", "compliance_cluster", "compliance_score"]],
        on=["_row_idx", "app_id", "app_name"],
        how="left",
    )
    policies_updated.drop(columns=["_row_idx"], inplace=True)

    policies_updated.to_csv(output_path, index=False)
    print(f"\nSaved to: {output_path}")
    print(f"Shape: {policies_updated.shape[0]} rows x {policies_updated.shape[1]} columns")


def main():
    parser = argparse.ArgumentParser(
        description="Cluster analyzed privacy policies and compute compliance scores."
    )
    parser.add_argument("input", help="Path to the analyzed policies CSV")
    parser.add_argument(
        "-o", "--output",
        help="Output CSV path (default: input filename with _clustered suffix)",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Error: file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        output_path = args.output
    else:
        base, ext = os.path.splitext(args.input)
        output_path = f"{base}_clustered{ext}"

    # Keep original for clean merge
    original_df = pd.read_csv(args.input)

    # Work on a copy for clustering/scoring
    df = load_and_validate(args.input)
    df = run_clustering(df)
    df = compute_compliance_score(df)

    print_summary(df)
    save_output(original_df, df, output_path)


if __name__ == "__main__":
    main()
