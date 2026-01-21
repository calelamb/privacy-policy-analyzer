"""
Pydantic models for structured output schema.
Based on K-12 Educational App Privacy Policy Research Framework.
"""

from pydantic import BaseModel, Field


class PolicyAnalysisResult(BaseModel):
    """
    Structured output schema for K-12 Educational App Privacy Policy Analysis.
    Based on research framework for evaluating privacy risk in educational applications.

    Scoring: More FALSE values = Higher privacy risk
    """

    model_config = {"extra": "forbid"}

    data_collection_disclosure: bool = Field(
        description="TRUE if policy clearly discloses types of personal data collected (PII, device details, usage data)"
    )

    data_use_purpose_specification: bool = Field(
        description="TRUE if policy specifies purposes for data use AND limits use to those purposes"
    )

    third_party_sharing_disclosure: bool = Field(
        description="TRUE if policy details if/how student data is shared with third parties by name or category"
    )

    parental_consent_mechanism: bool = Field(
        description="TRUE if policy addresses obtaining verifiable parental consent for children's data (COPPA requirement)"
    )

    coppa_ferpa_compliance_mention: bool = Field(
        description="TRUE if policy explicitly mentions COPPA and/or FERPA compliance"
    )

    data_retention_policy: bool = Field(
        description="TRUE if policy provides data retention schedule or deletion timeframes"
    )

    user_data_rights: bool = Field(
        description="TRUE if policy grants users/parents rights to access, correct, or delete their data"
    )

    data_security_encryption: bool = Field(
        description="TRUE if policy mentions security measures like encryption, secure servers, or access controls"
    )

    tracking_technologies_disclosure: bool = Field(
        description="TRUE if policy discloses use of cookies, web beacons, analytics, or other tracking technologies"
    )