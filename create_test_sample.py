#!/usr/bin/env python3
"""
Create a small reproducible sample from the large research dataset.

This utility is mainly for quick smoke tests, prompt experiments, or debugging
without running the analyzer over the full raw dataset.
"""

import pandas as pd


def main() -> None:
    """Create ``data/input/test_sample_5.csv`` from the raw working dataset."""
    input_file = "appmicroscope_data_clean_cert - appmicroscope_data_clean_cert.csv"
    df = pd.read_csv(input_file)

    print(f"Total rows in dataset: {len(df)}")
    print(f"Columns: {', '.join(df.columns[:10])}...")

    # Check if ppCompany column exists and has data
    if 'ppCompany' in df.columns:
        # Filter for rows that have non-empty privacy policies
        df_with_policies = df[df['ppCompany'].notna() & (df['ppCompany'].str.len() > 100)]
        print(f"Rows with privacy policies: {len(df_with_policies)}")

        # Select 5 random rows
        sample_size = min(5, len(df_with_policies))
        sample_df = df_with_policies.sample(n=sample_size, random_state=42)

        # Save to test file
        output_file = "data/input/test_sample_5.csv"
        sample_df.to_csv(output_file, index=False)

        print(f"\nCreated test sample with {sample_size} policies")
        print(f"Saved to: {output_file}")

        # Show the selected apps
        print("\nSelected apps for testing:")
        for idx, row in sample_df.iterrows():
            app_name = row.get('app_name', row.get('App Name', 'Unknown'))
            app_id = row.get('app_id', row.get('App ID', idx))
            policy_length = len(str(row['ppCompany']))
            print(f"  - {app_name} (ID: {app_id}) - Policy length: {policy_length} chars")
    else:
        print("ERROR: ppCompany column not found in the dataset!")
        print("Available columns:", df.columns.tolist())


if __name__ == "__main__":
    main()
