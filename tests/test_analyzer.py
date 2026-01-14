"""
Test suite for the Privacy Policy Analyzer.
"""

import os
import sys
import pytest
import json
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models import PolicyAnalysisResult
from analyzer import PolicyAnalyzer


class TestPolicyAnalysisResult:
    """Test the Pydantic model for policy analysis results."""

    def test_all_true_gives_low_risk(self):
        """Test that all TRUE values result in LOW risk."""
        result = PolicyAnalysisResult(
            data_collection_disclosure=True,
            data_use_purpose_specification=True,
            third_party_sharing_disclosure=True,
            parental_consent_mechanism=True,
            coppa_ferpa_compliance_mention=True,
            data_retention_policy=True,
            user_data_rights=True,
            data_security_encryption=True,
            tracking_technologies_disclosure=True
        )
        assert result.privacy_compliance_score == 9
        assert result.privacy_risk_level == "LOW"

    def test_all_false_gives_high_risk(self):
        """Test that all FALSE values result in HIGH risk."""
        result = PolicyAnalysisResult(
            data_collection_disclosure=False,
            data_use_purpose_specification=False,
            third_party_sharing_disclosure=False,
            parental_consent_mechanism=False,
            coppa_ferpa_compliance_mention=False,
            data_retention_policy=False,
            user_data_rights=False,
            data_security_encryption=False,
            tracking_technologies_disclosure=False
        )
        assert result.privacy_compliance_score == 0
        assert result.privacy_risk_level == "HIGH"

    def test_medium_risk_scoring(self):
        """Test that medium scores give MEDIUM risk."""
        result = PolicyAnalysisResult(
            data_collection_disclosure=True,
            data_use_purpose_specification=True,
            third_party_sharing_disclosure=True,
            parental_consent_mechanism=True,
            coppa_ferpa_compliance_mention=True,
            data_retention_policy=False,
            user_data_rights=False,
            data_security_encryption=False,
            tracking_technologies_disclosure=False
        )
        assert result.privacy_compliance_score == 5
        assert result.privacy_risk_level == "MEDIUM"


class TestPolicyAnalyzer:
    """Test the PolicyAnalyzer class."""

    @patch('analyzer.openai.OpenAI')
    def test_analyze_policy_success(self, mock_openai):
        """Test successful policy analysis."""
        # Mock the OpenAI response
        mock_client = Mock()
        mock_openai.return_value = mock_client

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({
            "data_collection_disclosure": True,
            "data_use_purpose_specification": True,
            "third_party_sharing_disclosure": True,
            "parental_consent_mechanism": True,
            "coppa_ferpa_compliance_mention": True,
            "data_retention_policy": True,
            "user_data_rights": True,
            "data_security_encryption": True,
            "tracking_technologies_disclosure": True,
            "privacy_compliance_score": 9,
            "privacy_risk_level": "LOW"
        })

        mock_client.chat.completions.create.return_value = mock_response

        # Create analyzer and test
        analyzer = PolicyAnalyzer(api_key="test_key")
        result = analyzer.analyze_policy("Sample privacy policy text", "test_app")

        assert result is not None
        assert result["data_collection_disclosure"] == True
        assert result["privacy_compliance_score"] == 9
        assert result["privacy_risk_level"] == "LOW"

    @patch('analyzer.openai.OpenAI')
    def test_analyze_policy_truncation(self, mock_openai):
        """Test that long policies are truncated."""
        mock_client = Mock()
        mock_openai.return_value = mock_client

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({
            "data_collection_disclosure": False,
            "data_use_purpose_specification": False,
            "third_party_sharing_disclosure": False,
            "parental_consent_mechanism": False,
            "coppa_ferpa_compliance_mention": False,
            "data_retention_policy": False,
            "user_data_rights": False,
            "data_security_encryption": False,
            "tracking_technologies_disclosure": False,
            "privacy_compliance_score": 0,
            "privacy_risk_level": "HIGH"
        })

        mock_client.chat.completions.create.return_value = mock_response

        # Create a very long policy text
        long_policy = "x" * 150000

        analyzer = PolicyAnalyzer(api_key="test_key")
        result = analyzer.analyze_policy(long_policy, "test_app")

        # Check that the API was called with truncated text
        call_args = mock_client.chat.completions.create.call_args
        messages = call_args[1]['messages']
        user_message = messages[1]['content']

        assert "[TRUNCATED]" in user_message
        assert len(user_message) < 110000  # Should be truncated


if __name__ == "__main__":
    pytest.main([__file__, "-v"])