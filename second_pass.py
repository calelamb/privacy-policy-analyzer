"""
Second pass script — re-runs the analyzer on apps that were skipped in the
first pass due to missing/short policy text in Master Data.csv, using the
richer policy text from 'privacy policy dataset finished.csv'.

Usage (run from the privacy_policy_analyzer directory):
    python second_pass.py

Outputs:
    data/output/second_pass_results.csv   — results for previously skipped apps
    data/output/full_results_v2_merged.csv — first pass + second pass combined
"""

import os
import sys
import pandas as pd

# ── CONFIG ────────────────────────────────────────────────────────────────────
FIRST_PASS_OUTPUT   = "data/output/full_results_v2.csv"
FINISHED_DATASET    = "privacy policy dataset finished.csv"
SECOND_PASS_OUTPUT  = "data/output/second_pass_results.csv"
MERGED_OUTPUT       = "data/output/full_results_v2_merged.csv"
MODEL               = "gpt-5.4"
MAX_CONCURRENT      = 20
POLICY_COLUMN       = "ppCompany"
# ─────────────────────────────────────────────────────────────────────────────


def main():
    """Recover skipped apps using the richer follow-up dataset.

    The script isolates rows marked ``empty_or_short_policy`` in the first-pass
    output, looks them up in the alternate dataset, and merges any recovered
    analyses back into a final combined CSV.
    """
    # 1. Load first pass results
    if not os.path.exists(FIRST_PASS_OUTPUT):
        print(f"ERROR: First pass output not found at {FIRST_PASS_OUTPUT}")
        print("Make sure the first run has completed before running this script.")
        sys.exit(1)

    first = pd.read_csv(FIRST_PASS_OUTPUT, low_memory=False)
    print(f"First pass results loaded: {len(first)} rows")

    # 2. Identify skipped apps (column is 'error', not 'error_type')
    error_col = 'error' if 'error' in first.columns else 'error_type'
    if error_col not in first.columns:
        print("ERROR: No error column found in first pass output.")
        sys.exit(1)

    skipped = first[first[error_col] == 'empty_or_short_policy']['app_id'].astype(str).tolist()
    print(f"Apps skipped in first pass: {len(skipped)}")

    # 3. Load finished dataset and find skipped apps with policy text
    if not os.path.exists(FINISHED_DATASET):
        print(f"ERROR: Finished dataset not found at {FINISHED_DATASET}")
        sys.exit(1)

    finished = pd.read_csv(FINISHED_DATASET, low_memory=False)
    finished['app_id'] = finished['app_id'].astype(str)

    skipped_with_text = finished[finished['app_id'].isin(skipped)].copy()

    def combined_len(row):
        """Return the longest available privacy-text field for a row."""
        c = str(row.get('ppCompany', '') or '').strip()
        p = str(row.get('ppPlatform', '') or '').strip()
        return max(len(c), len(p))

    skipped_with_text['_len'] = skipped_with_text.apply(combined_len, axis=1)
    skipped_with_text = skipped_with_text[skipped_with_text['_len'] >= 100]
    print(f"Skipped apps with usable text in finished dataset: {len(skipped_with_text)}")

    if len(skipped_with_text) == 0:
        print("No apps to reprocess. Exiting.")
        sys.exit(0)

    # 4. Save the subset to a temp CSV and run the analyzer on it
    temp_input = "data/output/_second_pass_input.csv"
    skipped_with_text.drop(columns=['_len']).to_csv(temp_input, index=False)
    print(f"\nTemp input saved: {temp_input}")
    print(f"Starting second pass on {len(skipped_with_text)} apps...\n")

    cmd = (
        f'python -m src.main "{temp_input}" "{SECOND_PASS_OUTPUT}" '
        f'--policy-column-primary {POLICY_COLUMN} '
        f'--model {MODEL} '
        f'--concurrent --max-concurrent {MAX_CONCURRENT}'
    )
    print(f"Running: {cmd}\n")
    exit_code = os.system(cmd)

    if exit_code != 0:
        print(f"\nERROR: Second pass failed with exit code {exit_code}")
        sys.exit(1)

    # 5. Merge first and second pass results
    if not os.path.exists(SECOND_PASS_OUTPUT):
        print(f"ERROR: Second pass output not found at {SECOND_PASS_OUTPUT}")
        sys.exit(1)

    second = pd.read_csv(SECOND_PASS_OUTPUT, low_memory=False)
    print(f"\nSecond pass complete: {len(second)} rows")

    # Remove the skipped placeholders from first pass and replace with second pass results
    first_cleaned = first[first[error_col] != 'empty_or_short_policy'].copy()
    merged = pd.concat([first_cleaned, second], ignore_index=True)
    merged['app_id'] = merged['app_id'].astype(str)
    merged = merged.sort_values('app_id').reset_index(drop=True)
    merged.to_csv(MERGED_OUTPUT, index=False)

    # Clean up temp file
    if os.path.exists(temp_input):
        os.remove(temp_input)

    print(f"\n{'='*60}")
    print(f"MERGE COMPLETE")
    print(f"  First pass (analyzed):    {len(first_cleaned)}")
    print(f"  Second pass (recovered):  {len(second)}")
    print(f"  Total in merged output:   {len(merged)}")
    print(f"  Saved to: {MERGED_OUTPUT}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
