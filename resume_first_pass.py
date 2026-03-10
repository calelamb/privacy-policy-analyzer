"""
Resume script — continues the first pass from where it left off.

Reads the existing output file to find successfully analyzed app_ids,
then re-runs the analyzer on any apps that failed (analysis_failed error)
plus any not yet in the output at all.

Usage (run from the privacy_policy_analyzer directory):
    python resume_first_pass.py
"""

import os
import sys
import pandas as pd

# ── CONFIG ────────────────────────────────────────────────────────────────────
MASTER_DATA         = "Master Data.csv"
EXISTING_OUTPUT     = "data/output/full_results_v2.csv"
RESUME_OUTPUT       = "data/output/full_results_v2_resume.csv"
FINAL_OUTPUT        = "data/output/full_results_v2.csv"   # overwrites with merged
MODEL               = "gpt-5.4"
MAX_CONCURRENT      = 20          # increased from 10 to reduce total API calls
POLICY_COLUMN       = "ppCompany"
# ─────────────────────────────────────────────────────────────────────────────


def main():
    """Resume a partially completed first-pass dataset run.

    The script keeps successful rows and intentional short-policy skips, then
    reprocesses only failed or previously unprocessed apps.
    """
    # 1. Load existing results — only treat successful rows as "done"
    #    Rows with error == 'analysis_failed' need to be retried
    #    Rows with error == 'empty_or_short_policy' are intentionally skipped (keep them)
    if not os.path.exists(EXISTING_OUTPUT):
        print(f"ERROR: Existing output not found at {EXISTING_OUTPUT}")
        sys.exit(1)

    existing = pd.read_csv(EXISTING_OUTPUT, low_memory=False)
    existing['app_id'] = existing['app_id'].astype(str)

    # Split into keepers (success + intentional skips) and failures to retry
    keepers  = existing[existing['error'] != 'analysis_failed'].copy()
    failures = existing[existing['error'] == 'analysis_failed'].copy()
    failed_ids     = set(failures['app_id'])
    successful_ids = set(keepers['app_id'])

    print(f"Successfully analyzed:     {keepers[keepers['error'].isna()].shape[0]}")
    print(f"Intentionally skipped:     {keepers[keepers['error'] == 'empty_or_short_policy'].shape[0]}")
    print(f"Failed (will retry):       {len(failed_ids)}")

    # 2. Load master data — include failed apps AND any not yet processed
    if not os.path.exists(MASTER_DATA):
        print(f"ERROR: Master data not found at {MASTER_DATA}")
        sys.exit(1)

    master = pd.read_csv(MASTER_DATA, low_memory=False)
    master['app_id'] = master['app_id'].astype(str)
    remaining = master[~master['app_id'].isin(successful_ids)].copy()

    print(f"\nTotal apps in Master Data: {len(master)}")
    print(f"Remaining to process:      {len(remaining)} ({len(failed_ids)} retries + {len(remaining) - len(failed_ids)} new)")

    if len(remaining) == 0:
        print("All apps already processed. Nothing to resume.")
        sys.exit(0)

    # 3. Save remaining apps to temp input file
    temp_input = "data/output/_resume_input.csv"
    remaining.to_csv(temp_input, index=False)
    print(f"\nStarting resume on {len(remaining)} apps...\n")

    cmd = (
        f'python -m src.main "{temp_input}" "{RESUME_OUTPUT}" '
        f'--policy-column-primary {POLICY_COLUMN} '
        f'--model {MODEL} '
        f'--concurrent --max-concurrent {MAX_CONCURRENT}'
    )
    print(f"Running: {cmd}\n")
    exit_code = os.system(cmd)

    if exit_code != 0:
        print(f"\nERROR: Resume run failed with exit code {exit_code}")
        print(f"Partial results (if any) saved to {RESUME_OUTPUT}")
        print("Re-run this script to continue from where it left off.")
        sys.exit(1)

    # 4. Merge keepers + newly resumed results (failures are replaced, not duplicated)
    if not os.path.exists(RESUME_OUTPUT):
        print(f"ERROR: Resume output not found at {RESUME_OUTPUT}")
        sys.exit(1)

    resumed = pd.read_csv(RESUME_OUTPUT, low_memory=False)
    merged = pd.concat([keepers, resumed], ignore_index=True)
    merged['app_id'] = merged['app_id'].astype(str)  # ensure consistent type before sort
    merged = merged.sort_values('app_id').reset_index(drop=True)
    merged.to_csv(FINAL_OUTPUT, index=False)

    # Clean up temp files
    for f in [temp_input, RESUME_OUTPUT]:
        if os.path.exists(f):
            os.remove(f)

    success_count = merged[merged['error'].isna()].shape[0]
    print(f"\n{'='*60}")
    print(f"RESUME COMPLETE")
    print(f"  Successfully analyzed: {success_count}")
    print(f"  Retried this run:      {len(resumed)}")
    print(f"  Total in output:       {len(merged)}")
    print(f"  Saved to: {FINAL_OUTPUT}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
