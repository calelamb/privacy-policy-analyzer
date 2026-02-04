"""
Main analyzer module for processing privacy policies.
"""

import os
import json
import time
from typing import Optional, Dict, Any
import logging

import openai
import pandas as pd
from tqdm import tqdm

from .models import PolicyAnalysisResult
from .prompts import SYSTEM_PROMPT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _extract_coppa_fields(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Extract COPPA analysis fields for CSV output."""
    coppa = analysis.get("coppa_analysis", {})
    return {
        "coppa_mentions": coppa.get("mentions_coppa", False),
        "coppa_claims_compliance": coppa.get("claims_compliance", False),
        "coppa_consent_methods": "; ".join(coppa.get("consent_methods", [])),
        "coppa_consent_details": coppa.get("consent_method_details", ""),
        "coppa_exceptions": "; ".join(coppa.get("exceptions_claimed", [])),
        "coppa_exception_details": coppa.get("exception_details", ""),
        "coppa_age_threshold": coppa.get("age_threshold_stated", ""),
    }


def _extract_gdpr_fields(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Extract GDPR analysis fields for CSV output."""
    gdpr = analysis.get("gdpr_analysis", {})
    return {
        "gdpr_mentions": gdpr.get("mentions_gdpr", False),
        "gdpr_claims_compliance": gdpr.get("claims_compliance", False),
        "gdpr_consent_methods": "; ".join(gdpr.get("consent_methods", [])),
        "gdpr_consent_details": gdpr.get("consent_method_details", ""),
        "gdpr_lawful_bases": "; ".join(gdpr.get("lawful_bases", [])),
        "gdpr_lawful_basis_details": gdpr.get("lawful_basis_details", ""),
        "gdpr_age_threshold": gdpr.get("age_threshold_stated", ""),
    }


def _get_empty_coppa_fields() -> Dict[str, Any]:
    """Return empty COPPA fields for error cases."""
    return {
        "coppa_mentions": False,
        "coppa_claims_compliance": False,
        "coppa_consent_methods": "",
        "coppa_consent_details": "",
        "coppa_exceptions": "",
        "coppa_exception_details": "",
        "coppa_age_threshold": "",
    }


def _get_empty_gdpr_fields() -> Dict[str, Any]:
    """Return empty GDPR fields for error cases."""
    return {
        "gdpr_mentions": False,
        "gdpr_claims_compliance": False,
        "gdpr_consent_methods": "",
        "gdpr_consent_details": "",
        "gdpr_lawful_bases": "",
        "gdpr_lawful_basis_details": "",
        "gdpr_age_threshold": "",
    }


class PolicyAnalyzer:
    """
    Analyzes privacy policies using OpenAI's API to extract boolean indicators
    based on K-12 Educational App Privacy Policy Research Framework.
    """

    def __init__(self, api_key: str, model: str = "gpt-5-nano"):
        """
        Initialize the PolicyAnalyzer.

        Args:
            api_key: OpenAI API key
            model: OpenAI model to use (default: gpt-5-nano)
        """
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        logger.info(f"Initialized PolicyAnalyzer with model: {model}")

    def analyze_policy(self, policy_text: str, app_id: str = None) -> Optional[Dict[str, Any]]:
        """
        Analyze a single privacy policy and return structured results.

        Args:
            policy_text: The privacy policy text to analyze
            app_id: Optional app identifier for logging

        Returns:
            Dictionary with analysis results or None if error
        """
        # Truncate if too long (GPT-4o-mini context is 128k but we want to stay safe)
        max_chars = 100000
        if len(policy_text) > max_chars:
            policy_text = policy_text[:max_chars] + "\n\n[TRUNCATED]"
            logger.warning(f"Policy for app {app_id} truncated to {max_chars} chars")

        try:
            # Build request parameters
            request_params = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Analyze this privacy policy:\n\n{policy_text}"}
                ],
                "response_format": {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "policy_analysis",
                        "schema": PolicyAnalysisResult.model_json_schema(),
                        "strict": True
                    }
                }
            }

            # Only add temperature for models that support it (gpt-5-nano doesn't)
            if "nano" not in self.model.lower():
                request_params["temperature"] = 0.1

            response = self.client.chat.completions.create(**request_params)

            result = json.loads(response.choices[0].message.content)
            logger.info(f"Successfully analyzed policy for app {app_id}")
            return result

        except openai.RateLimitError as e:
            logger.error(f"Rate limit error for app {app_id}: {e}")
            time.sleep(60)  # Wait a minute before continuing
            return self.analyze_policy(policy_text, app_id)  # Retry

        except Exception as e:
            logger.error(f"Error analyzing policy for app {app_id}: {e}")
            return None

    def process_batch(
        self,
        input_file: str,
        output_file: str,
        policy_column: str = "policy_text",
        id_column: str = "app_id",
        name_column: str = "app_name",
        delay: float = 0.5,
        resume_from: int = 0
    ) -> pd.DataFrame:
        """
        Process a batch of policies from CSV.

        Args:
            input_file: Path to input CSV file
            output_file: Path to output CSV file
            policy_column: Column name containing policy text
            id_column: Column name containing app identifier
            name_column: Column name containing app name (optional)
            delay: Delay between API calls in seconds
            resume_from: Index to resume processing from (for crash recovery)

        Returns:
            DataFrame with analysis results
        """
        logger.info(f"Loading policies from {input_file}")

        # Load input data
        df = pd.read_csv(input_file)
        total_policies = len(df)
        logger.info(f"Found {total_policies} policies to analyze")

        # Check if output file exists for resume functionality
        results = []
        if os.path.exists(output_file) and resume_from > 0:
            existing_results = pd.read_csv(output_file)
            results = existing_results.to_dict('records')
            logger.info(f"Resuming from index {resume_from} with {len(results)} existing results")

        # Process each policy
        for idx, row in tqdm(df.iterrows(), total=total_policies, initial=resume_from):
            if idx < resume_from:
                continue

            app_id = row.get(id_column, f"app_{idx}")
            app_name = row.get(name_column, "") if name_column in row else ""
            policy_text = row.get(policy_column, "")

            # Skip empty policies
            if pd.isna(policy_text) or len(str(policy_text).strip()) < 100:
                result = {
                    "app_id": app_id,
                    "app_name": app_name,
                    "error": "empty_or_short_policy",
                    "data_collection_disclosure": False,
                    "data_use_purpose_specification": False,
                    "third_party_sharing_disclosure": False,
                    "third_party_list": "",
                    "third_party_data_shared": "",
                    "parental_consent_mechanism": False,
                    "coppa_ferpa_compliance_mention": False,
                    "data_retention_policy": False,
                    "user_data_rights": False,
                    "data_security_encryption": False,
                    "tracking_technologies_disclosure": False,
                    **_get_empty_coppa_fields(),
                    **_get_empty_gdpr_fields(),
                }
                logger.warning(f"Skipping app {app_id}: empty or short policy")
            else:
                analysis = self.analyze_policy(str(policy_text), app_id)
                if analysis:
                    # Format third party information for CSV output
                    third_party_list = analysis.get("third_party_list", [])
                    third_party_details = analysis.get("third_party_details", [])

                    # Create formatted string for third party data shared
                    third_party_data_shared = []
                    for detail in third_party_details:
                        name = detail.get("name", "Unknown")
                        purpose = detail.get("purpose", "Not specified")
                        data_types = detail.get("data_shared", [])
                        data_str = ", ".join(data_types) if data_types else "Not specified"
                        third_party_data_shared.append(f"{name} ({purpose}): {data_str}")

                    result = {
                        "app_id": app_id,
                        "app_name": app_name,
                        "data_collection_disclosure": analysis.get("data_collection_disclosure", False),
                        "data_use_purpose_specification": analysis.get("data_use_purpose_specification", False),
                        "third_party_sharing_disclosure": analysis.get("third_party_sharing_disclosure", False),
                        "third_party_list": "; ".join(third_party_list) if third_party_list else "",
                        "third_party_data_shared": " | ".join(third_party_data_shared) if third_party_data_shared else "",
                        "parental_consent_mechanism": analysis.get("parental_consent_mechanism", False),
                        "coppa_ferpa_compliance_mention": analysis.get("coppa_ferpa_compliance_mention", False),
                        "data_retention_policy": analysis.get("data_retention_policy", False),
                        "user_data_rights": analysis.get("user_data_rights", False),
                        "data_security_encryption": analysis.get("data_security_encryption", False),
                        "tracking_technologies_disclosure": analysis.get("tracking_technologies_disclosure", False),
                        **_extract_coppa_fields(analysis),
                        **_extract_gdpr_fields(analysis),
                    }
                else:
                    result = {
                        "app_id": app_id,
                        "app_name": app_name,
                        "error": "analysis_failed",
                        "data_collection_disclosure": False,
                        "data_use_purpose_specification": False,
                        "third_party_sharing_disclosure": False,
                        "third_party_list": "",
                        "third_party_data_shared": "",
                        "parental_consent_mechanism": False,
                        "coppa_ferpa_compliance_mention": False,
                        "data_retention_policy": False,
                        "user_data_rights": False,
                        "data_security_encryption": False,
                        "tracking_technologies_disclosure": False,
                        **_get_empty_coppa_fields(),
                        **_get_empty_gdpr_fields(),
                    }

            results.append(result)

            # Save progress incrementally
            if idx % 50 == 0 or idx == total_policies - 1:
                pd.DataFrame(results).to_csv(output_file, index=False)
                logger.info(f"Progress saved: {len(results)}/{total_policies} policies analyzed")

            # Rate limiting
            if idx < total_policies - 1:
                time.sleep(delay)

        # Final save and summary
        output_df = pd.DataFrame(results)
        output_df.to_csv(output_file, index=False)

        # Print summary statistics
        logger.info("\n" + "="*50)
        logger.info("ANALYSIS COMPLETE")
        logger.info("="*50)
        logger.info(f"Total policies processed: {len(output_df)}")

        if 'error' in output_df.columns:
            error_count = output_df['error'].notna().sum()
            logger.info(f"Errors encountered: {error_count}")

        return output_df

    def analyze_single_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a single privacy policy from a text file.

        Args:
            file_path: Path to text file containing privacy policy

        Returns:
            Dictionary with analysis results
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            policy_text = f.read()

        app_id = os.path.basename(file_path).replace('.txt', '')
        analysis = self.analyze_policy(policy_text, app_id)

        if analysis:
            # Format third party information for output
            third_party_list = analysis.get("third_party_list", [])
            third_party_details = analysis.get("third_party_details", [])

            # Create formatted string for third party data shared
            third_party_data_shared = []
            for detail in third_party_details:
                name = detail.get("name", "Unknown")
                purpose = detail.get("purpose", "Not specified")
                data_types = detail.get("data_shared", [])
                data_str = ", ".join(data_types) if data_types else "Not specified"
                third_party_data_shared.append(f"{name} ({purpose}): {data_str}")

            return {
                "app_id": app_id,
                "data_collection_disclosure": analysis.get("data_collection_disclosure", False),
                "data_use_purpose_specification": analysis.get("data_use_purpose_specification", False),
                "third_party_sharing_disclosure": analysis.get("third_party_sharing_disclosure", False),
                "third_party_list": "; ".join(third_party_list) if third_party_list else "",
                "third_party_data_shared": " | ".join(third_party_data_shared) if third_party_data_shared else "",
                "parental_consent_mechanism": analysis.get("parental_consent_mechanism", False),
                "coppa_ferpa_compliance_mention": analysis.get("coppa_ferpa_compliance_mention", False),
                "data_retention_policy": analysis.get("data_retention_policy", False),
                "user_data_rights": analysis.get("user_data_rights", False),
                "data_security_encryption": analysis.get("data_security_encryption", False),
                "tracking_technologies_disclosure": analysis.get("tracking_technologies_disclosure", False),
                # Include full COPPA and GDPR analysis objects for JSON output
                "coppa_analysis": analysis.get("coppa_analysis", {}),
                "gdpr_analysis": analysis.get("gdpr_analysis", {}),
            }
        else:
            return {"app_id": app_id, "error": "analysis_failed"}
