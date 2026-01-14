#!/usr/bin/env python3
"""
Analyzer for pre-extracted privacy policy summaries.
Works with structured Q&A format rather than full policy text.
"""

import pandas as pd
import sys
from typing import Dict

def analyze_summary_fields(row: pd.Series) -> Dict[str, bool]:
    """
    Analyze pre-extracted privacy fields to determine the 9 boolean indicators.
    """

    results = {}

    # 1. Data Collection Disclosure
    data_collected = str(row.get('What data is collected?', '')).lower()
    results['data_collection_disclosure'] = (
        len(data_collected) > 20 and
        data_collected not in ['', 'nan', 'none', 'not specified', 'unknown']
    )

    # 2. Data Use Purpose Specification
    why_needed = str(row.get('Why is it needed?', '')).lower()
    results['data_use_purpose_specification'] = (
        len(why_needed) > 20 and
        why_needed not in ['', 'nan', 'none', 'not specified', 'unknown'] and
        ('education' in why_needed or 'learning' in why_needed or 'service' in why_needed)
    )

    # 3. Third-Party Sharing Disclosure
    who_shared = str(row.get('Who is it shared with?', '')).lower()
    results['third_party_sharing_disclosure'] = (
        len(who_shared) > 10 and
        who_shared not in ['', 'nan', 'none', 'not specified', 'unknown'] and
        (who_shared != 'no one' and who_shared != 'not shared')
    )

    # 4. Parental Consent Mechanism
    family_policy = str(row.get('FamilyPolicy', '')).lower()
    under_13 = str(row.get('policyUnder13_Yes', 0))
    results['parental_consent_mechanism'] = (
        under_13 == '1' or
        'parent' in family_policy or
        'consent' in family_policy
    )

    # 5. COPPA/FERPA Compliance Mention
    coppa_compliant = row.get('Vendor asserted COPPA Compliance Only', 0)
    coppa_safe = row.get('COPPA Safe Harbor', 0)
    results['coppa_ferpa_compliance_mention'] = (
        coppa_compliant == 1 or
        coppa_safe == 1 or
        'coppa' in family_policy or
        'ferpa' in family_policy
    )

    # 6. Data Retention Policy
    retention = str(row.get('How long is data retained?', '')).lower()
    results['data_retention_policy'] = (
        len(retention) > 10 and
        retention not in ['', 'nan', 'none', 'not specified', 'unknown', 'indefinitely']
    )

    # 7. User Data Rights
    rights = str(row.get('What are a user\'s rights?', '')).lower()
    results['user_data_rights'] = (
        len(rights) > 10 and
        rights not in ['', 'nan', 'none', 'not specified', 'unknown'] and
        any(term in rights for term in ['access', 'delete', 'correct', 'review', 'control'])
    )

    # 8. Data Security & Encryption
    security = str(row.get('What security measures are taken?', '')).lower()
    results['data_security_encryption'] = (
        len(security) > 10 and
        security not in ['', 'nan', 'none', 'not specified', 'unknown'] and
        any(term in security for term in ['encrypt', 'secure', 'protect', 'ssl', 'tls', 'firewall'])
    )

    # 9. Tracking Technologies Disclosure
    has_ads = row.get('misc_hasAds', 0)
    behavioral_ads = row.get('misc_hasBehavioralAds', 0)
    retargeting = row.get('misc_retargetingPresentField_Yes', 0)
    results['tracking_technologies_disclosure'] = (
        has_ads == 1 or
        behavioral_ads == 1 or
        retargeting == 1
    )

    # Calculate score and risk level
    score = sum(results.values())
    results['privacy_compliance_score'] = score

    if score >= 7:
        results['privacy_risk_level'] = 'LOW'
    elif score >= 4:
        results['privacy_risk_level'] = 'MEDIUM'
    else:
        results['privacy_risk_level'] = 'HIGH'

    return results

def process_dataset(input_file: str, output_file: str):
    """Process the entire dataset."""

    print(f"Loading data from {input_file}...")

    # Read the file
    if input_file.endswith('.xlsx'):
        df = pd.read_excel(input_file)
    else:
        df = pd.read_csv(input_file)

    print(f"Found {len(df)} apps to analyze")

    # Analyze each row
    results = []
    for idx, row in df.iterrows():
        if idx % 100 == 0:
            print(f"Processing app {idx+1}/{len(df)}...")

        analysis = analyze_summary_fields(row)

        # Add app identifiers
        result = {
            'app_id': row.get('app_id', row.get('App ID', f'app_{idx}')),
            'app_name': row.get('app_name', row.get('App Name', '')),
            **analysis
        }
        results.append(result)

    # Create results dataframe
    results_df = pd.DataFrame(results)

    # Save results
    results_df.to_csv(output_file, index=False)
    print(f"\nResults saved to {output_file}")

    # Print summary statistics
    print("\n" + "="*50)
    print("ANALYSIS SUMMARY")
    print("="*50)
    print(f"Total apps analyzed: {len(results_df)}")

    risk_counts = results_df['privacy_risk_level'].value_counts()
    for level in ['LOW', 'MEDIUM', 'HIGH']:
        if level in risk_counts.index:
            count = risk_counts[level]
            print(f"{level} risk: {count} apps ({count/len(results_df)*100:.1f}%)")

    avg_score = results_df['privacy_compliance_score'].mean()
    print(f"\nAverage compliance score: {avg_score:.2f}/9")

    # Show which indicators are most commonly missing
    print("\nCompliance rates by indicator:")
    for col in results_df.columns:
        if col.endswith('disclosure') or col.endswith('mechanism') or col.endswith('mention') or \
           col.endswith('policy') or col.endswith('rights') or col.endswith('encryption') or \
           col.endswith('specification'):
            true_count = results_df[col].sum()
            rate = true_count / len(results_df) * 100
            print(f"  {col}: {rate:.1f}% compliant")

    return results_df

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python summary_analyzer.py <input_file> <output_file>")
        print("\nExample:")
        print("  python summary_analyzer.py data.xlsx privacy_analysis.csv")
    else:
        process_dataset(sys.argv[1], sys.argv[2])