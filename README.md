# Privacy Policy Analyzer for K-12 Educational Apps

An automated tool for analyzing privacy policies of educational applications, extracting 9 key privacy indicators based on academic research frameworks for K-12 app privacy risk assessment.

## Overview

This tool processes privacy policy texts and extracts boolean indicators for:
- Data collection disclosure
- Data use purpose specification
- Third-party sharing practices
- Parental consent mechanisms
- COPPA/FERPA compliance
- Data retention policies
- User data rights
- Security measures
- Tracking technologies

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd privacy_policy_analyzer

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your OpenAI API key
```

### Basic Usage

```bash
# Analyze a batch of policies from CSV
python -m src.main data/input/policies.csv data/output/results.csv

# Analyze a single policy file
python -m src.main --single data/input/example_policy.txt

# Use custom column names
python -m src.main data/input/policies.csv data/output/results.csv \
  --policy-column "privacy_policy" \
  --id-column "application_id"
```

## Input Format

The input CSV should have at minimum:
- `app_id`: Unique identifier for each app
- `policy_text`: Full privacy policy text
- `app_name`: (Optional) Application name

## Output Format

The tool generates a CSV with the following columns:

### Boolean Indicators (TRUE/FALSE)
- `data_collection_disclosure`
- `data_use_purpose_specification`
- `third_party_sharing_disclosure`
- `parental_consent_mechanism`
- `coppa_ferpa_compliance_mention`
- `data_retention_policy`
- `user_data_rights`
- `data_security_encryption`
- `tracking_technologies_disclosure`

## Advanced Options

```bash
# Use a different model (default: gpt-5-nano, cheapest)
python -m src.main input.csv output.csv --model gpt-4o-mini

# Adjust rate limiting delay (default: 0.5 seconds)
python -m src.main input.csv output.csv --delay 1.0

# Resume from specific index after interruption
python -m src.main input.csv output.csv --resume-from 500

# Output as JSON
python -m src.main --single policy.txt --json
```

## Cost Estimates

Using GPT-5-nano (recommended, cheapest):
- Input: $0.05 per 1M tokens
- Output: $0.40 per 1M tokens
- Per policy: ~$0.0002-0.0005
- 140,000 policies: ~$30-70 total

## Research Framework

This tool implements privacy evaluation criteria from:
- Common Sense Media State of Kids' Privacy Report
- FTC/iKeepSafe COPPA Compliance Guidelines
- Academic research on K-12 EdTech privacy policies

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure `OPENAI_API_KEY` is set in `.env` file
2. **Rate Limits**: Tool automatically handles rate limits with retry logic
3. **Large Policies**: Policies >100k chars are automatically truncated
4. **Crash Recovery**: Use `--resume-from` flag to continue from last checkpoint

### Error Handling

The tool marks policies with errors but continues processing:
- `empty_or_short_policy`: Policy text <100 characters
- `analysis_failed`: API error during analysis

## Development

```bash
# Run tests
pytest tests/

# Format code
black src/

# Lint
flake8 src/
```

## License

For academic research use. Please cite appropriately if used in publications.

## Support

For issues or questions, please open an issue on the repository.