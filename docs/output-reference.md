# Output Reference

The v2 analyzer writes a wide CSV intended for downstream statistical analysis, auditing, and research review. In a typical full run the file contains 102 columns.

## Column Groups

| Group | Count | Notes |
| --- | --- | --- |
| Identifier columns | 2 | `app_id`, `app_name` |
| Error column | 1 | `error`, usually blank on success |
| Boolean indicators | 35 | the main Table 1 compliance calls |
| Evidence fields | 35 | one `_evidence` column per boolean |
| Enum or extracted text fields | 7 | sharing direction, retention specificity, security specificity, consent specificity |
| Flattened COPPA summary fields | 7 | `coppa_*` columns |
| Flattened GDPR summary fields | 7 | `gdpr_*` columns |
| Third-party summary fields | 2 | `third_party_list`, `third_party_data_shared` |
| Composite score fields | 6 | GDPR, COPPA, and overall score plus percentage |

## Identifier And Error Fields

| Column | Meaning |
| --- | --- |
| `app_id` | stable application identifier from the input file |
| `app_name` | application name if present in the input |
| `error` | blank on success, otherwise an error code |

Current error codes:

- `empty_or_short_policy` - no usable policy text was available
- `analysis_failed` - the model call failed or returned unusable output

## The 35 Boolean Indicators

### Company identity

- `ci_controller_identity`
- `ci_dpo_contact`
- `ci_operator_list`

### Types of data collected

- `td_categories_disclosed`
- `td_children_data_types`
- `td_persistent_identifiers`

### Purpose of collection and use

- `pu_purposes_stated`
- `pu_legal_basis`
- `pu_children_data_use`

### Third-party sharing

- `ts_recipients_disclosed`
- `ts_children_data_recipients`
- `ts_third_party_purpose`

### International transfers

- `it_eu_transfers`

### Retention

- `re_retention_period`
- `re_children_retention`

### User and parent rights

- `ur_right_access`
- `ur_right_rectification`
- `ur_right_erasure`
- `ur_right_restrict`
- `ur_right_portability`
- `ur_right_object`
- `ur_right_withdraw_consent`
- `ur_right_supervisory_complaint`
- `ur_parent_review_right`
- `ur_parent_delete_right`
- `ur_parent_refuse_right`

### Automated decision-making

- `adm_profiling_disclosure`

### Data provision requirements

- `dp_mandatory_disclosure`

### Security

- `sec_coppa_safeguards`
- `sec_gdpr_measures`

### Policy accessibility

- `pa_concise_transparent`
- `pa_prominent_link`

### Updates and changes

- `up_material_changes_notice`

### Consent mechanisms

- `cm_parental_consent_procedures`

### Data source

- `ds_indirect_data_source`

## Evidence Fields

Every boolean field has a matching evidence column:

- Example: `ci_controller_identity` and `ci_controller_identity_evidence`
- Example: `ur_right_erasure` and `ur_right_erasure_evidence`

Interpretation guidance:

- `TRUE` means the policy explicitly disclosed the requirement.
- `FALSE` means the policy did not clearly disclose it.
- Evidence strings are short supporting excerpts or short explanations such as `Not found`.

## Enum And Extracted Text Fields

| Column | Meaning | Expected values |
| --- | --- | --- |
| `ts_sharing_direction` | overall sharing claim | `shares`, `does_not_share`, `conditional`, `vague_or_silent` |
| `ts_children_sharing_direction` | child-specific sharing claim | `shares`, `does_not_share`, `conditional`, `vague_or_silent` |
| `re_retention_specificity` | how specific retention language is | `specific_timeframe`, `until_deleted`, `as_long_as_necessary`, `indefinite_or_silent` |
| `re_retention_stated_period` | literal retention language extracted from the policy | free text |
| `sec_specificity` | how specific security language is | `specific_measures`, `general_language`, `silent` |
| `sec_measures_listed` | extracted list of concrete controls | free text |
| `cm_consent_specificity` | how specific consent language is | `method_described`, `mentioned_no_method`, `not_applicable` |

## Flattened COPPA And GDPR Summary Fields

These are supplementary columns derived from the nested structured output:

### COPPA

- `coppa_mentions`
- `coppa_claims_compliance`
- `coppa_consent_methods`
- `coppa_consent_details`
- `coppa_exceptions`
- `coppa_exception_details`
- `coppa_age_threshold`

### GDPR

- `gdpr_mentions`
- `gdpr_claims_compliance`
- `gdpr_consent_methods`
- `gdpr_consent_details`
- `gdpr_lawful_bases`
- `gdpr_lawful_basis_details`
- `gdpr_age_threshold`

## Third-Party Summary Fields

| Column | Meaning |
| --- | --- |
| `third_party_list` | semicolon-separated list of named third parties found in the policy |
| `third_party_data_shared` | formatted summary of party name, purpose, and data types shared |

## Composite Scores

| Column | Meaning |
| --- | --- |
| `gdpr_composite_score` | number of GDPR indicators satisfied |
| `gdpr_composite_pct` | GDPR compliance percentage |
| `coppa_composite_score` | number of COPPA indicators satisfied |
| `coppa_composite_pct` | COPPA compliance percentage |
| `overall_composite_score` | number of all tracked indicators satisfied |
| `overall_composite_pct` | overall compliance percentage |

## Recommended Analysis Practice

- Use the boolean columns for quantitative work.
- Use evidence columns when checking borderline or surprising cases.
- Treat blank `error` values as successful analyses.
- Prefer the merged output after the second pass when working on final research summaries.
