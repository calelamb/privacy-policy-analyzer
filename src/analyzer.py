"""
Core analysis pipeline for the v2 privacy policy research workflow.

This module is the authoritative implementation of the current analyzer. It is
responsible for:

- converting the Pydantic schema into an OpenAI-compatible JSON schema
- selecting the best policy text from research datasets
- calling the OpenAI API in sync or async mode
- flattening structured output into CSV-friendly rows
- computing GDPR, COPPA, and overall composite scores
"""

import os
import json
import time
import copy
import asyncio
from typing import Optional, Dict, Any, List, Union
import logging

import openai
import pandas as pd
from tqdm import tqdm
from tqdm.asyncio import tqdm as async_tqdm

from .models import PolicyAnalysisResult
from .prompts import SYSTEM_PROMPT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _make_openai_compatible_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a Pydantic JSON schema to OpenAI structured output compatible format.

    OpenAI's structured output doesn't support:
    - $ref references (must be inlined)
    - anyOf with null (for Optional types)
    - allOf constructs
    - title fields

    Args:
        schema: Raw JSON schema produced by ``PolicyAnalysisResult``.

    Returns:
        A deep-copied schema dictionary with unsupported constructs removed or
        inlined so it can be used as an OpenAI ``json_schema`` response format.
    """
    schema = copy.deepcopy(schema)
    defs = schema.pop("$defs", {})

    def resolve_refs(obj: Any) -> Any:
        """Recursively inline schema fragments and remove unsupported keys.

        Args:
            obj: A schema fragment represented as a dictionary, list, or scalar.

        Returns:
            The transformed schema fragment with references resolved.
        """
        if isinstance(obj, dict):
            # Handle $ref
            if "$ref" in obj:
                ref_path = obj["$ref"]
                # Extract definition name from "#/$defs/Name"
                def_name = ref_path.split("/")[-1]
                if def_name in defs:
                    resolved = resolve_refs(copy.deepcopy(defs[def_name]))
                    return resolved
                return obj

            # Handle anyOf with null (Optional types) - convert to base type
            if "anyOf" in obj:
                non_null = [t for t in obj["anyOf"] if t.get("type") != "null"]
                if len(non_null) == 1:
                    result = resolve_refs(non_null[0])
                    if "description" in obj:
                        result["description"] = obj["description"]
                    return result

            # Handle allOf - merge all schemas
            if "allOf" in obj:
                merged = {}
                for item in obj["allOf"]:
                    resolved_item = resolve_refs(item)
                    merged.update(resolved_item)
                return merged

            # Recursively process all keys
            result = {}
            for key, value in obj.items():
                # Remove title fields (not needed for OpenAI)
                if key == "title":
                    continue
                result[key] = resolve_refs(value)
            return result

        elif isinstance(obj, list):
            return [resolve_refs(item) for item in obj]

        return obj

    return resolve_refs(schema)


def build_policy_text(row: Any) -> str:
    """
    Construct the best available policy text from ppCompany and ppPlatform columns.

    Priority:
    1. ppCompany alone if >= 200 chars (vendor's full policy — preferred)
    2. ppPlatform alone if ppCompany is short/absent and ppPlatform >= 200 chars
    3. Concatenation of both if both are >= 100 chars
    4. Whatever is available if both are short (will likely be caught by the < 100 char filter)

    Args:
        row: DataFrame row or dict with ppCompany and ppPlatform keys

    Returns:
        Combined policy text string
    """
    pp_company = str(row.get('ppCompany', '') or '').strip()
    pp_platform = str(row.get('ppPlatform', '') or '').strip()

    company_len = len(pp_company)
    platform_len = len(pp_platform)

    if company_len >= 200 and platform_len >= 100:
        # Both substantive — include both, company policy first
        return f"{pp_company}\n\n[APP STORE PRIVACY LABEL]\n{pp_platform}"
    elif company_len >= 200:
        return pp_company
    elif platform_len >= 200:
        return pp_platform
    else:
        # Neither is long — concatenate whatever exists
        combined = f"{pp_company} {pp_platform}".strip()
        return combined


def _extract_coppa_fields(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Flatten the nested COPPA block into top-level CSV columns.

    Args:
        analysis: Structured model output for a single policy.

    Returns:
        A dictionary containing the ``coppa_*`` columns expected in the output
        dataset.
    """
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
    """Flatten the nested GDPR block into top-level CSV columns.

    Args:
        analysis: Structured model output for a single policy.

    Returns:
        A dictionary containing the ``gdpr_*`` columns expected in the output
        dataset.
    """
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
    """Return blank COPPA values for skipped or failed analyses.

    Returns:
        A dictionary shaped like the flattened COPPA output fields with safe
        defaults for error rows.
    """
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
    """Return blank GDPR values for skipped or failed analyses.

    Returns:
        A dictionary shaped like the flattened GDPR output fields with safe
        defaults for error rows.
    """
    return {
        "gdpr_mentions": False,
        "gdpr_claims_compliance": False,
        "gdpr_consent_methods": "",
        "gdpr_consent_details": "",
        "gdpr_lawful_bases": "",
        "gdpr_lawful_basis_details": "",
        "gdpr_age_threshold": "",
    }


# Define which indicators belong to each regulatory framework
GDPR_INDICATOR_FIELDS = [
    "ci_controller_identity", "ci_dpo_contact",
    "td_categories_disclosed", "pu_purposes_stated", "pu_legal_basis",
    "ts_recipients_disclosed", "it_eu_transfers",
    "re_retention_period",
    "ur_right_access", "ur_right_rectification", "ur_right_erasure",
    "ur_right_restrict", "ur_right_portability", "ur_right_object",
    "ur_right_withdraw_consent", "ur_right_supervisory_complaint",
    "adm_profiling_disclosure", "dp_mandatory_disclosure",
    "sec_gdpr_measures", "pa_concise_transparent", "ds_indirect_data_source",
]

COPPA_INDICATOR_FIELDS = [
    "ci_controller_identity", "ci_operator_list",
    "td_children_data_types", "td_persistent_identifiers",
    "pu_children_data_use",
    "ts_children_data_recipients", "ts_third_party_purpose",
    "re_children_retention",
    "ur_parent_review_right", "ur_parent_delete_right", "ur_parent_refuse_right",
    "sec_coppa_safeguards", "pa_prominent_link",
    "up_material_changes_notice", "cm_parental_consent_procedures",
]

ALL_INDICATOR_FIELDS = list(dict.fromkeys(GDPR_INDICATOR_FIELDS + COPPA_INDICATOR_FIELDS + [
    "ci_controller_identity", "td_categories_disclosed", "td_persistent_identifiers",
    "pu_purposes_stated", "ts_recipients_disclosed", "re_retention_period",
    "sec_coppa_safeguards", "sec_gdpr_measures", "pa_prominent_link",
    "pa_concise_transparent", "up_material_changes_notice",
    "cm_parental_consent_procedures", "ds_indirect_data_source",
]))


def _compute_composite_scores(result: Dict[str, Any]) -> Dict[str, Any]:
    """Compute GDPR, COPPA, and overall percentages from boolean indicators.

    Args:
        result: A partially flattened analysis dictionary containing the Table 1
            boolean indicators.

    Returns:
        A dictionary with score counts and percentage values for GDPR, COPPA,
        and the combined indicator set.
    """

    def count_true(fields):
        return sum(1 for f in fields if result.get(f, False) is True)

    gdpr_score = count_true(GDPR_INDICATOR_FIELDS)
    coppa_score = count_true(COPPA_INDICATOR_FIELDS)
    overall_score = count_true(ALL_INDICATOR_FIELDS)

    return {
        "gdpr_composite_score": gdpr_score,
        "gdpr_composite_pct": round(gdpr_score / len(GDPR_INDICATOR_FIELDS) * 100, 2),
        "coppa_composite_score": coppa_score,
        "coppa_composite_pct": round(coppa_score / len(COPPA_INDICATOR_FIELDS) * 100, 2),
        "overall_composite_score": overall_score,
        "overall_composite_pct": round(overall_score / len(ALL_INDICATOR_FIELDS) * 100, 2),
    }


# Complete list of the 35 Table 1 boolean indicator field names
TABLE1_BOOLEAN_FIELDS = [
    "ci_controller_identity", "ci_dpo_contact", "ci_operator_list",
    "td_categories_disclosed", "td_children_data_types", "td_persistent_identifiers",
    "pu_purposes_stated", "pu_legal_basis", "pu_children_data_use",
    "ts_recipients_disclosed", "ts_children_data_recipients", "ts_third_party_purpose",
    "it_eu_transfers",
    "re_retention_period", "re_children_retention",
    "ur_right_access", "ur_right_rectification", "ur_right_erasure", "ur_right_restrict",
    "ur_right_portability", "ur_right_object", "ur_right_withdraw_consent",
    "ur_right_supervisory_complaint",
    "ur_parent_review_right", "ur_parent_delete_right", "ur_parent_refuse_right",
    "adm_profiling_disclosure", "dp_mandatory_disclosure",
    "sec_coppa_safeguards", "sec_gdpr_measures",
    "pa_concise_transparent", "pa_prominent_link",
    "up_material_changes_notice", "cm_parental_consent_procedures",
    "ds_indirect_data_source",
]

TABLE1_EVIDENCE_FIELDS = [f + "_evidence" for f in TABLE1_BOOLEAN_FIELDS]

TABLE1_ENUM_FIELDS = [
    "ts_sharing_direction", "ts_children_sharing_direction",
    "re_retention_specificity", "re_retention_stated_period",
    "sec_specificity", "sec_measures_listed",
    "cm_consent_specificity",
]


def _extract_table1_fields(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Flatten the core Table 1 indicators, evidence, and enum fields.

    Args:
        analysis: Structured model output for a single policy.

    Returns:
        A dictionary containing the canonical flat columns used in batch CSV
        outputs.
    """
    result = {}
    # Boolean indicators
    for field in TABLE1_BOOLEAN_FIELDS:
        result[field] = analysis.get(field, False)
    # Evidence strings
    for field in TABLE1_EVIDENCE_FIELDS:
        result[field] = analysis.get(field, "")
    # Enum and free-text fields
    for field in TABLE1_ENUM_FIELDS:
        result[field] = analysis.get(field, "")
    return result


def _get_empty_table1_fields() -> Dict[str, Any]:
    """Return blank Table 1 indicator values for error rows.

    Returns:
        A dictionary with every Table 1 boolean, evidence, and enum field
        populated with an empty-safe default.
    """
    result = {}
    for field in TABLE1_BOOLEAN_FIELDS:
        result[field] = False
    for field in TABLE1_EVIDENCE_FIELDS:
        result[field] = ""
    for field in TABLE1_ENUM_FIELDS:
        result[field] = ""
    return result


def _build_success_result(app_id, app_name, analysis):
    """Build the final output row for a successful policy analysis.

    Args:
        app_id: Application identifier from the input dataset.
        app_name: Human-readable application name if available.
        analysis: Structured model output returned by the analyzer.

    Returns:
        A flattened row ready to append to the output CSV.
    """
    third_party_list = analysis.get("third_party_list", [])
    third_party_details = analysis.get("third_party_details", [])
    third_party_data_shared = []
    for detail in third_party_details:
        name = detail.get("name", "Unknown")
        purpose = detail.get("purpose", "Not specified")
        data_types = detail.get("data_shared", [])
        data_str = ", ".join(data_types) if data_types else "Not specified"
        third_party_data_shared.append(f"{name} ({purpose}): {data_str}")

    composite_scores = _compute_composite_scores(analysis)

    return {
        "app_id": app_id,
        "app_name": app_name,
        **_extract_table1_fields(analysis),
        **_extract_coppa_fields(analysis),
        **_extract_gdpr_fields(analysis),
        "third_party_list": "; ".join(third_party_list) if third_party_list else "",
        "third_party_data_shared": " | ".join(third_party_data_shared) if third_party_data_shared else "",
        **composite_scores,
    }


def _build_error_result(app_id, app_name, error_type):
    """Build the final output row for a skipped or failed policy analysis.

    Args:
        app_id: Application identifier from the input dataset.
        app_name: Human-readable application name if available.
        error_type: Stable error label such as ``empty_or_short_policy``.

    Returns:
        A flattened row with blank analysis fields and zeroed score columns.
    """
    return {
        "app_id": app_id,
        "app_name": app_name,
        "error": error_type,
        **_get_empty_table1_fields(),
        **_get_empty_coppa_fields(),
        **_get_empty_gdpr_fields(),
        "third_party_list": "",
        "third_party_data_shared": "",
        "gdpr_composite_score": 0,
        "gdpr_composite_pct": 0.0,
        "coppa_composite_score": 0,
        "coppa_composite_pct": 0.0,
        "overall_composite_score": 0,
        "overall_composite_pct": 0.0,
    }


def _resolve_policy_text(row, policy_column):
    """Resolve the best available policy text for a dataset row.

    The analyzer first respects the explicitly requested policy column. If that
    column is missing or too short, it falls back to the ``ppCompany`` /
    ``ppPlatform`` selection logic used by the main research dataset.

    Args:
        row: A pandas row or row-like mapping.
        policy_column: The preferred policy text column requested by the caller.

    Returns:
        The chosen policy text, or an empty string when no usable text exists.
    """
    policy_text = row.get(policy_column, "")
    if pd.isna(policy_text) or len(str(policy_text).strip()) < 100:
        # Try building from ppCompany/ppPlatform if available
        row_index = row.index if hasattr(row, 'index') else row.keys()
        if 'ppCompany' in row_index or 'ppPlatform' in row_index:
            policy_text = build_policy_text(row)
        else:
            policy_text = ""
    return policy_text


class PolicyAnalyzer:
    """
    Analyze privacy policies using OpenAI structured outputs.

    This class wraps both synchronous and asynchronous OpenAI clients and keeps
    the research-specific concerns in one place: request construction, usage
    tracking, retry behavior, batch orchestration, and CSV-safe flattening.
    """

    # Pricing per 1M tokens - update as needed
    MODEL_PRICING = {
        "gpt-5.4":      {"input": 2.00,  "output": 8.00},  # placeholder — update when OpenAI publishes pricing
        "gpt-5.1":      {"input": 2.00,  "output": 8.00},
        "gpt-4.1":      {"input": 2.00,  "output": 8.00},
        "gpt-4.1-mini": {"input": 0.40,  "output": 1.60},
        "gpt-4o":       {"input": 2.50,  "output": 10.00},
        "gpt-4o-mini":  {"input": 0.15,  "output": 0.60},
        "gpt-5-nano":   {"input": 0.10,  "output": 0.40},
        "gpt-3.5-turbo":{"input": 0.50,  "output": 1.50},
    }

    def __init__(self, api_key: str, model: str = "gpt-5.4"):
        """
        Initialize analyzer clients and usage tracking.

        Args:
            api_key: OpenAI API key used for both sync and async clients.
            model: OpenAI model name used for structured extraction requests.
        """
        self.client = openai.OpenAI(api_key=api_key)
        self.async_client = openai.AsyncOpenAI(api_key=api_key)
        self.model = model
        self._reset_usage()
        self._usage_lock = asyncio.Lock()
        logger.info(f"Initialized PolicyAnalyzer with model: {model}")

    def _reset_usage(self):
        """Reset in-memory token and request counters for the current session."""
        self._usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
        }

    def _record_usage(self, response):
        """Record token usage from a successful API response.

        Args:
            response: OpenAI response object with optional ``usage`` metadata.
        """
        if hasattr(response, 'usage') and response.usage:
            self._usage["prompt_tokens"] += response.usage.prompt_tokens
            self._usage["completion_tokens"] += response.usage.completion_tokens
            self._usage["total_tokens"] += response.usage.total_tokens
        self._usage["requests"] += 1
        self._usage["successful_requests"] += 1

    def _record_failure(self):
        """Record a failed request for reporting and cost summaries."""
        self._usage["requests"] += 1
        self._usage["failed_requests"] += 1

    def get_usage(self) -> Dict[str, Any]:
        """
        Return current usage statistics for the active analyzer instance.

        Returns:
            Dictionary with tokens, request counts, selected model, and an
            estimated dollar cost based on ``MODEL_PRICING``.
        """
        usage = self._usage.copy()

        # Calculate estimated cost
        pricing = self.MODEL_PRICING.get(self.model, {"input": 0, "output": 0})
        input_cost = (usage["prompt_tokens"] / 1_000_000) * pricing["input"]
        output_cost = (usage["completion_tokens"] / 1_000_000) * pricing["output"]
        usage["estimated_cost_usd"] = round(input_cost + output_cost, 4)
        usage["model"] = self.model

        return usage

    def print_usage(self):
        """Print a human-readable summary of the current usage counters."""
        usage = self.get_usage()
        print("\n" + "=" * 50)
        print("OPENAI API USAGE SUMMARY")
        print("=" * 50)
        print(f"Model: {usage['model']}")
        print(f"Requests: {usage['requests']} ({usage['successful_requests']} successful, {usage['failed_requests']} failed)")
        print(f"Prompt tokens: {usage['prompt_tokens']:,}")
        print(f"Completion tokens: {usage['completion_tokens']:,}")
        print(f"Total tokens: {usage['total_tokens']:,}")
        print(f"Estimated cost: ${usage['estimated_cost_usd']:.4f}")
        print("=" * 50)

    def reset_usage(self):
        """Reset usage counters so a new run starts from a clean slate."""
        self._reset_usage()
        logger.info("Usage counters reset")

    def analyze_policy(self, policy_text: str, app_id: str = None) -> Optional[Dict[str, Any]]:
        """
        Analyze one privacy policy synchronously.

        Args:
            policy_text: Raw privacy policy text to send to the model.
            app_id: Optional application identifier used in logs.

        Returns:
            Parsed structured output for the policy, or ``None`` when the
            request fails after retry handling.
        """
        # Truncate if too long (GPT-4o-mini context is 128k but we want to stay safe)
        max_chars = 100000
        if len(policy_text) > max_chars:
            policy_text = policy_text[:max_chars] + "\n\n[TRUNCATED]"
            logger.warning(f"Policy for app {app_id} truncated to {max_chars} chars")

        try:
            # Build request parameters with OpenAI-compatible schema
            compatible_schema = _make_openai_compatible_schema(
                PolicyAnalysisResult.model_json_schema()
            )
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
                        "schema": compatible_schema,
                        "strict": True
                    }
                },
                "temperature": 0,
            }

            response = self.client.chat.completions.create(**request_params)
            self._record_usage(response)

            result = json.loads(response.choices[0].message.content)
            logger.info(f"Successfully analyzed policy for app {app_id}")
            return result

        except openai.RateLimitError as e:
            logger.error(f"Rate limit error for app {app_id}: {e}")
            time.sleep(60)  # Wait a minute before continuing
            return self.analyze_policy(policy_text, app_id)  # Retry

        except Exception as e:
            self._record_failure()
            logger.error(f"Error analyzing policy for app {app_id}: {e}")
            return None

    async def analyze_policy_async(self, policy_text: str, app_id: str = None) -> Optional[Dict[str, Any]]:
        """
        Analyze one privacy policy asynchronously.

        Args:
            policy_text: Raw privacy policy text to send to the model.
            app_id: Optional application identifier used in logs.

        Returns:
            Parsed structured output for the policy, or ``None`` when the
            request fails after retry handling.
        """
        max_chars = 100000
        if len(policy_text) > max_chars:
            policy_text = policy_text[:max_chars] + "\n\n[TRUNCATED]"
            logger.warning(f"Policy for app {app_id} truncated to {max_chars} chars")

        try:
            compatible_schema = _make_openai_compatible_schema(
                PolicyAnalysisResult.model_json_schema()
            )
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
                        "schema": compatible_schema,
                        "strict": True
                    }
                },
                "temperature": 0,
            }

            response = await self.async_client.chat.completions.create(**request_params)

            async with self._usage_lock:
                self._record_usage(response)

            result = json.loads(response.choices[0].message.content)
            logger.info(f"Successfully analyzed policy for app {app_id}")
            return result

        except openai.RateLimitError as e:
            logger.warning(f"Rate limit hit for app {app_id}, waiting 60s: {e}")
            await asyncio.sleep(60)
            return await self.analyze_policy_async(policy_text, app_id)

        except Exception as e:
            async with self._usage_lock:
                self._record_failure()
            logger.error(f"Error analyzing policy for app {app_id}: {e}")
            return None

    async def _process_single_policy(
        self,
        row: pd.Series,
        semaphore: asyncio.Semaphore,
        id_column: str,
        name_column: str,
        policy_column: str
    ) -> Dict[str, Any]:
        """Process one dataset row inside the concurrent batch workflow.

        Args:
            row: Dataset row containing identifiers and policy text columns.
            semaphore: Async semaphore limiting concurrent OpenAI requests.
            id_column: Column name containing the application identifier.
            name_column: Column name containing the human-readable app name.
            policy_column: Preferred policy text column.

        Returns:
            A flattened output row representing either a successful analysis or
            an error placeholder.
        """
        async with semaphore:
            app_id = row.get(id_column, "unknown")
            app_name = row.get(name_column, "") if name_column in row.index else ""
            policy_text = _resolve_policy_text(row, policy_column)

            if pd.isna(policy_text) or len(str(policy_text).strip()) < 100:
                logger.warning(f"Skipping app {app_id}: empty or short policy")
                return _build_error_result(app_id, app_name, "empty_or_short_policy")

            analysis = await self.analyze_policy_async(str(policy_text), app_id)

            if analysis:
                return _build_success_result(app_id, app_name, analysis)
            else:
                return _build_error_result(app_id, app_name, "analysis_failed")

    async def process_batch_concurrent(
        self,
        input_file: str,
        output_file: str,
        policy_column: str = "policy_text",
        id_column: str = "app_id",
        name_column: str = "app_name",
        max_concurrent: int = 10,
        resume_from: int = 0
    ) -> pd.DataFrame:
        """
        Process a CSV batch concurrently using asyncio.

        Args:
            input_file: Path to the source CSV file.
            output_file: Path where partial and final CSV results are written.
            policy_column: Column name containing policy text.
            id_column: Column name containing the application identifier.
            name_column: Column name containing the application name.
            max_concurrent: Maximum number of simultaneous OpenAI requests.
            resume_from: Row index to start from when resuming a run.

        Returns:
            DataFrame containing one flattened output row per processed policy.
        """
        logger.info(f"Loading policies from {input_file}")
        df = pd.read_csv(input_file)

        if resume_from > 0:
            df = df.iloc[resume_from:]
            logger.info(f"Resuming from index {resume_from}")

        total_policies = len(df)
        logger.info(f"Found {total_policies} policies to analyze (max {max_concurrent} concurrent)")

        semaphore = asyncio.Semaphore(max_concurrent)

        # Create tasks for all policies
        tasks = [
            self._process_single_policy(row, semaphore, id_column, name_column, policy_column)
            for _, row in df.iterrows()
        ]

        # Process with progress bar
        results = []
        for coro in async_tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Analyzing"):
            result = await coro
            results.append(result)

            # Save progress periodically
            if len(results) % 50 == 0:
                pd.DataFrame(results).to_csv(output_file, index=False)
                logger.info(f"Progress saved: {len(results)}/{total_policies} policies analyzed")

        # Sort results by app_id to maintain order
        results.sort(key=lambda x: float(x.get('app_id', 0)) if x.get('app_id') else 0)

        # Final save
        output_df = pd.DataFrame(results)
        output_df.to_csv(output_file, index=False)

        logger.info("\n" + "="*50)
        logger.info("ANALYSIS COMPLETE")
        logger.info("="*50)
        logger.info(f"Total policies processed: {len(output_df)}")

        if 'error' in output_df.columns:
            error_count = output_df['error'].notna().sum()
            logger.info(f"Errors encountered: {error_count}")

        self.print_usage()
        return output_df

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
        Process a CSV batch sequentially.

        Args:
            input_file: Path to the source CSV file.
            output_file: Path where partial and final CSV results are written.
            policy_column: Column name containing policy text.
            id_column: Column name containing the application identifier.
            name_column: Column name containing the application name.
            delay: Delay between requests, mainly for lower-rate or debugging runs.
            resume_from: Row index to start from when resuming a run.

        Returns:
            DataFrame containing one flattened output row per processed policy.
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
            policy_text = _resolve_policy_text(row, policy_column)

            # Skip empty policies
            if pd.isna(policy_text) or len(str(policy_text).strip()) < 100:
                result = _build_error_result(app_id, app_name, "empty_or_short_policy")
                logger.warning(f"Skipping app {app_id}: empty or short policy")
            else:
                analysis = self.analyze_policy(str(policy_text), app_id)
                if analysis:
                    result = _build_success_result(app_id, app_name, analysis)
                else:
                    result = _build_error_result(app_id, app_name, "analysis_failed")

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

        # Print usage summary
        self.print_usage()

        return output_df

    def analyze_single_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a single text file outside of the batch CSV workflow.

        Args:
            file_path: Path to a text file containing privacy policy content.

        Returns:
            Flattened analysis output. For convenience, the nested ``coppa`` and
            ``gdpr`` objects are reattached when analysis succeeds.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            policy_text = f.read()

        app_id = os.path.basename(file_path).replace('.txt', '')
        analysis = self.analyze_policy(policy_text, app_id)

        if analysis:
            result = _build_success_result(app_id, "", analysis)
            # Include full COPPA and GDPR analysis objects for JSON output
            result["coppa_analysis"] = analysis.get("coppa_analysis", {})
            result["gdpr_analysis"] = analysis.get("gdpr_analysis", {})
            return result
        else:
            return {"app_id": app_id, "error": "analysis_failed"}
