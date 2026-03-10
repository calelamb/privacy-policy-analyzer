"""
Cluster analysis and compliance scoring for analyzed privacy policies.

Clusters policies using KMeans on 14 disclosure columns, computes a compliance
score from 35 boolean columns, and outputs an augmented CSV. This file is a
post-processing utility for downstream research analysis rather than part of
the extraction pipeline itself.
"""

import argparse
import os
import sys

import pandas as pd
from sklearn.cluster import KMeans

from src.analyzer import TABLE1_BOOLEAN_FIELDS

CLUSTERING_COLUMNS = [
    # Use the 14 most interpretable indicators for clustering
    "ci_controller_identity",
    "td_categories_disclosed",
    "pu_purposes_stated",
    "ts_recipients_disclosed",
    "re_retention_period",
    "ur_right_erasure",
    "ur_parent_delete_right",
    "sec_coppa_safeguards",
    "sec_gdpr_measures",
    "cm_parental_consent_procedures",
    "up_material_changes_notice",
    "td_children_data_types",
    "pu_children_data_use",
    "it_eu_transfers",
]

SCORING_COLUMNS = TABLE1_BOOLEAN_FIELDS


def _coerce_to_bool(series: pd.Series) -> pd.Series:
    """Convert a mixed-type pandas series into strict booleans.

    Args:
        series: Input column that may contain strings, numbers, booleans, or NaN.

    Returns:
        A boolean series suitable for scoring and clustering.
    """
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
    """Load an analyzed CSV and coerce required scoring columns to booleans.

    Args:
        input_path: Path to the analyzer output CSV.

    Returns:
        A validated dataframe ready for clustering.
    """
    df = pd.read_csv(input_path)

    missing = [c for c in SCORING_COLUMNS if c not in df.columns]
    if missing:
        print(f"Error: missing columns in input CSV: {missing}", file=sys.stderr)
        sys.exit(1)

    for col in SCORING_COLUMNS:
        df[col] = _coerce_to_bool(df[col])

    return df


def run_clustering(df: pd.DataFrame) -> pd.DataFrame:
    """Assign each policy to one of three compliance clusters.

    Args:
        df: Validated analyzer output dataframe.

    Returns:
        The same dataframe with a ``compliance_cluster`` column appended.
    """
    X = df[CLUSTERING_COLUMNS].fillna(0).astype(int)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["compliance_cluster"] = kmeans.fit_predict(X)
    return df


def compute_compliance_score(df: pd.DataFrame) -> pd.DataFrame:
    """Populate the generic ``compliance_score`` column used in summaries.

    Args:
        df: Analyzer output dataframe, with or without precomputed composite
            percentages.

    Returns:
        The dataframe with a ``compliance_score`` column.
    """
    # If composite scores are already in the dataframe, use them directly
    if "overall_composite_pct" in df.columns:
        df["compliance_score"] = df["overall_composite_pct"]
    else:
        # Fallback: compute from boolean columns
        df["compliance_score"] = (
            df[SCORING_COLUMNS].fillna(False).astype(int).sum(axis=1) / len(SCORING_COLUMNS) * 100
        ).round(2)
    return df


def print_summary(df: pd.DataFrame) -> None:
    """Print a console summary of the clustering results.

    Args:
        df: Clustered analyzer dataframe with score columns present.
    """
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
    """Merge clustering columns onto the original CSV shape and save the result.

    Args:
        original_df: Unmodified dataframe loaded directly from disk.
        clustered_df: Processed dataframe containing new cluster and score columns.
        output_path: Destination path for the augmented CSV.
    """
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
    """Parse CLI arguments and run the clustering utility end to end."""
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
