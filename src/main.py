#!/usr/bin/env python3
"""
CLI entry point for the Privacy Policy Analyzer.
"""

import argparse
import os
import sys
import json
from dotenv import load_dotenv

from .analyzer import PolicyAnalyzer


def main():
    """Main entry point for the CLI."""
    # Load environment variables
    load_dotenv()

    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Analyze privacy policies for K-12 educational apps",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze batch of policies from CSV
  python -m src.main data/input/policies.csv data/output/results.csv

  # Analyze with custom column names
  python -m src.main data/input/policies.csv data/output/results.csv \\
    --policy-column "privacy_policy" \\
    --id-column "application_id"

  # Analyze a single policy file
  python -m src.main --single data/input/example_policy.txt

  # Use a different model
  python -m src.main data/input/policies.csv data/output/results.csv \\
    --model gpt-4o

  # Resume from a specific index (for crash recovery)
  python -m src.main data/input/policies.csv data/output/results.csv \\
    --resume-from 500
        """
    )

    # File arguments
    parser.add_argument(
        "input",
        nargs='?',
        help="Input CSV file with policy texts (or single text file with --single flag)"
    )
    parser.add_argument(
        "output",
        nargs='?',
        help="Output CSV file for results"
    )

    # Single file mode
    parser.add_argument(
        "--single",
        action="store_true",
        help="Analyze a single policy text file instead of batch CSV"
    )

    # Column name arguments
    parser.add_argument(
        "--policy-column",
        default="policy_text",
        help="Column name containing policy text (default: policy_text)"
    )
    parser.add_argument(
        "--id-column",
        default="app_id",
        help="Column name containing app identifier (default: app_id)"
    )
    parser.add_argument(
        "--name-column",
        default="app_name",
        help="Column name containing app name (default: app_name)"
    )

    # Processing options
    parser.add_argument(
        "--model",
        default="gpt-5-nano",
        choices=["gpt-5-nano", "gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
        help="OpenAI model to use (default: gpt-5-nano, cheapest option)"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Delay between API calls in seconds (default: 0.5)"
    )
    parser.add_argument(
        "--resume-from",
        type=int,
        default=0,
        help="Resume processing from a specific index (for crash recovery)"
    )

    # API key option
    parser.add_argument(
        "--api-key",
        help="OpenAI API key (or set OPENAI_API_KEY environment variable)"
    )

    # Output format options
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON instead of CSV"
    )

    # Verbose mode
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.single and (not args.input or not args.output):
        parser.error("Input and output files are required for batch processing")
    elif args.single and not args.input:
        parser.error("Input file is required")

    # Get API key
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found.")
        print("Please set it as an environment variable or pass it with --api-key")
        sys.exit(1)

    # Initialize analyzer
    print(f"Initializing Privacy Policy Analyzer with model: {args.model}")
    analyzer = PolicyAnalyzer(api_key=api_key, model=args.model)

    try:
        if args.single:
            # Single file mode
            print(f"Analyzing single policy from {args.input}")
            result = analyzer.analyze_single_file(args.input)

            # Output result
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print("\nAnalysis Results:")
                print("-" * 50)
                for key, value in result.items():
                    if key != "app_id":
                        print(f"{key}: {value}")
        else:
            # Batch processing mode
            print(f"Processing policies from {args.input}")
            print(f"Results will be saved to {args.output}")

            results = analyzer.process_batch(
                input_file=args.input,
                output_file=args.output,
                policy_column=args.policy_column,
                id_column=args.id_column,
                name_column=args.name_column,
                delay=args.delay,
                resume_from=args.resume_from
            )

            print(f"\nResults saved to {args.output}")
            print(f"Processed {len(results)} policies")

            if 'error' in results.columns:
                error_count = results['error'].notna().sum()
                if error_count > 0:
                    print(f"Warning: {error_count} policies had errors")

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error during analysis: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()