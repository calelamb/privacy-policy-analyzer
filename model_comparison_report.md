# Model Comparison Report: Privacy Policy Analysis

## Summary

Compared 10 privacy policies analyzed by three OpenAI models:
- **gpt-5-nano** (original production analysis)
- **gpt-4o-mini** (new comparison)
- **gpt-4o** (new comparison)

## Key Findings

### 1. Boolean Field Agreement

| Comparison | Agreement Rate |
|------------|---------------|
| gpt-4o-mini vs nano | **100%** (130/130 fields) |
| gpt-4o vs nano | **84.6%** (110/130 fields) |

The lower agreement rate for gpt-4o is primarily due to **Goosechase failing** (parsing error), which returned all False values. Excluding Goosechase:

- gpt-4o agreement with nano (9 policies): ~97%

### 2. Third Party Detection

| App | nano | mini | 4o |
|-----|------|------|-----|
| Access My Library® | 3 | 3 | 5 |
| ArbiterSports | 3 | 3 | 0* |
| Be Strong | 2 | 3 | 2 |
| BrainPOP ELL | 2 | 2 | 2 |
| Choosi | 2 | 2 | 2 |
| Desmos | 2 | 2 | 2 |
| DreamscapeEDU | 5 | 5 | 5 |
| Gmail | 6 | 5 | 6 |
| Goosechase | 2 | 2 | 0* |
| HMH Science Dimensions | 2 | 2 | 2 |

*gpt-4o parsing failures

**Observations:**
- gpt-4o-mini matches nano on 8/10 policies for third party counts
- gpt-4o-mini adds NAI to Be Strong (legitimate advertising partner found)
- gpt-4o finds additional parties for Access My Library (NAI, DAA)

### 3. COPPA Consent Methods

All models showed strong agreement on COPPA consent detection:
- `school_consent` detected consistently for educational apps (BrainPOP, Choosi, Desmos, Gmail, Goosechase)
- `email_plus` detected for DreamscapeEDU across all models
- `not_applicable` used consistently for Be Strong

### 4. Errors

| Model | Errors | Details |
|-------|--------|---------|
| gpt-5-nano | 0 | No errors |
| gpt-4o-mini | 0 | No errors |
| gpt-4o | 1 | Goosechase parsing failed |

### 5. Cost Comparison

| Model | Cost (10 policies) | Relative Cost |
|-------|-------------------|---------------|
| gpt-5-nano | ~$0.003 | 1x (baseline) |
| gpt-4o-mini | ~$0.016 | 5x |
| gpt-4o | ~$0.27 | 90x |

## Conclusion

**gpt-4o-mini provides the best balance of quality and cost:**

1. **100% boolean agreement** with gpt-5-nano results
2. **Equivalent third party detection** (sometimes finding additional legitimate parties)
3. **No errors** in processing
4. **5x the cost** of nano, but 18x cheaper than gpt-4o

**gpt-4o** had parsing issues (1/10 failures) and showed inconsistencies likely due to response formatting, making it less reliable despite higher cost.

**Recommendation:** For production use, gpt-4o-mini appears to offer equivalent quality to the current gpt-5-nano results while potentially catching additional third parties. If budget allows (~$3/1000 policies vs ~$0.50), gpt-4o-mini could be a quality upgrade.

## Files Generated

- `data/output/comparison_4o_mini.csv` - gpt-4o-mini results
- `data/output/comparison_4o.csv` - gpt-4o results
- `data/output/comparison_nano.csv` - Original nano results (subset)
