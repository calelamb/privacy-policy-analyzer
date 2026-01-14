#!/usr/bin/env python3
"""
Quick script to check the columns in your Excel/CSV file and prepare it for analysis.
"""

import pandas as pd
import sys

def check_and_prepare_file(input_file):
    """Check columns and prepare file for analysis."""

    # Try to read the file (works with both Excel and CSV)
    if input_file.endswith('.xlsx') or input_file.endswith('.xls'):
        df = pd.read_excel(input_file)
        output_file = input_file.replace('.xlsx', '_prepared.csv').replace('.xls', '_prepared.csv')
    else:
        df = pd.read_csv(input_file)
        output_file = input_file.replace('.csv', '_prepared.csv')

    print(f"File loaded successfully!")
    print(f"Total rows: {len(df)}")
    print(f"\nColumns found:")
    for i, col in enumerate(df.columns, 1):
        print(f"{i}. {col}")
        # Show sample of non-null values
        non_null = df[col].dropna()
        if len(non_null) > 0:
            sample = str(non_null.iloc[0])[:100] + "..." if len(str(non_null.iloc[0])) > 100 else str(non_null.iloc[0])
            print(f"   Sample: {sample}")

    print("\n" + "="*50)
    print("COLUMN MAPPING HELPER")
    print("="*50)

    # Try to auto-detect columns
    policy_col = None
    id_col = None
    name_col = None

    for col in df.columns:
        col_lower = col.lower()
        if any(term in col_lower for term in ['policy', 'privacy', 'text', 'content']):
            policy_col = col
        elif any(term in col_lower for term in ['id', 'identifier', 'app_id']):
            id_col = col
        elif any(term in col_lower for term in ['name', 'app', 'title']):
            name_col = col

    print(f"\nAuto-detected mappings:")
    print(f"Policy text column: {policy_col}")
    print(f"App ID column: {id_col}")
    print(f"App name column: {name_col}")

    # Create the command
    if policy_col and id_col:
        print(f"\n✅ Ready to analyze! Use this command:")
        print(f"\npython -m src.main '{input_file}' data/output/results.csv \\")
        print(f"  --policy-column '{policy_col}' \\")
        print(f"  --id-column '{id_col}'", end="")
        if name_col:
            print(f" \\")
            print(f"  --name-column '{name_col}'")
        else:
            print()
    else:
        print("\n⚠️  Could not auto-detect all required columns.")
        print("You'll need to specify them manually in the command.")

    # Check for empty policies
    if policy_col:
        empty_count = df[policy_col].isna().sum() + (df[policy_col].str.len() < 100).sum()
        if empty_count > 0:
            print(f"\n⚠️  Warning: {empty_count} policies are empty or very short (<100 chars)")
            print("These will be marked as errors in the output.")

    return df

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_columns.py <your_excel_or_csv_file>")
        print("\nThis script will:")
        print("1. Show you all columns in your file")
        print("2. Auto-detect which columns contain the privacy policies")
        print("3. Generate the exact command you need to run the analysis")
    else:
        check_and_prepare_file(sys.argv[1])