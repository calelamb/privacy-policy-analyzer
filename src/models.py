"""
Pydantic models for structured output schema.
Based on K-12 Educational App Privacy Policy Research Framework.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class COPPAConsentMethod(str, Enum):
    """FTC-approved verifiable parental consent methods under COPPA."""
    SIGNED_CONSENT_FORM = "signed_consent_form"
    CREDIT_DEBIT_CARD = "credit_debit_card"
    TOLL_FREE_PHONE = "toll_free_phone"
    VIDEO_CONFERENCE = "video_conference"
    GOVERNMENT_ID = "government_id"
    KNOWLEDGE_BASED_AUTH = "knowledge_based_auth"
    EMAIL_PLUS = "email_plus"
    SCHOOL_CONSENT = "school_consent"
    OTHER = "other"
    NOT_SPECIFIED = "not_specified"
    NOT_APPLICABLE = "not_applicable"


class COPPAException(str, Enum):
    """COPPA exceptions for parental consent."""
    SCHOOL_AUTHORIZATION = "school_authorization"
    ONE_TIME_RESPONSE = "one_time_response"
    INTERNAL_OPERATIONS = "internal_operations"
    CHILD_SAFETY = "child_safety"
    MULTIPLE_CONTACT = "multiple_contact"
    NONE_CLAIMED = "none_claimed"
    NOT_APPLICABLE = "not_applicable"


class GDPRConsentMethod(str, Enum):
    """GDPR parental consent verification methods."""
    WRITTEN_CONSENT = "written_consent"
    EMAIL_VERIFICATION = "email_verification"
    PARENT_ACCOUNT_LINKING = "parent_account_linking"
    VIDEO_PHONE_VERIFICATION = "video_phone_verification"
    ID_DOCUMENT = "id_document"
    REASONABLE_EFFORTS = "reasonable_efforts"
    OTHER = "other"
    NOT_SPECIFIED = "not_specified"
    NOT_APPLICABLE = "not_applicable"


class GDPRLawfulBasis(str, Enum):
    """GDPR lawful bases for processing children's data."""
    CONSENT = "consent"
    CONTRACT = "contract"
    LEGAL_OBLIGATION = "legal_obligation"
    VITAL_INTERESTS = "vital_interests"
    PUBLIC_TASK = "public_task"
    LEGITIMATE_INTERESTS = "legitimate_interests"
    PREVENTIVE_COUNSELING = "preventive_counseling"
    NOT_SPECIFIED = "not_specified"
    NOT_APPLICABLE = "not_applicable"


class ThirdPartyDetail(BaseModel):
    """Details about a specific third party and data shared with them."""

    model_config = {"extra": "forbid"}

    name: str = Field(
        description="Name of the third party (e.g., 'Google Analytics', 'AWS', 'Facebook')"
    )

    purpose: str = Field(
        description="Purpose for sharing with this third party (e.g., 'analytics', 'cloud storage', 'advertising', 'not specified')"
    )

    data_shared: List[str] = Field(
        description="Specific types of data shared with this third party (e.g., ['IP address', 'device ID', 'usage data'])"
    )


class COPPAAnalysis(BaseModel):
    """Detailed COPPA compliance analysis."""

    model_config = {"extra": "forbid"}

    mentions_coppa: bool = Field(
        description="TRUE if policy explicitly mentions COPPA or Children's Online Privacy Protection Act"
    )

    claims_compliance: bool = Field(
        description="TRUE if policy claims to comply with COPPA requirements"
    )

    consent_methods: List[COPPAConsentMethod] = Field(
        description="List of parental consent methods described in the policy (from categorized list)"
    )

    consent_method_details: str = Field(
        description="Quoted or paraphrased text from policy describing consent methods"
    )

    exceptions_claimed: List[COPPAException] = Field(
        description="List of COPPA exceptions claimed in the policy (from categorized list)"
    )

    exception_details: str = Field(
        description="Quoted or paraphrased text from policy describing exceptions"
    )

    age_threshold_stated: Optional[int] = Field(
        description="Age threshold stated in policy for children's data (typically 13 for COPPA)"
    )


class GDPRAnalysis(BaseModel):
    """Detailed GDPR compliance analysis for children's data."""

    model_config = {"extra": "forbid"}

    mentions_gdpr: bool = Field(
        description="TRUE if policy explicitly mentions GDPR, EU users, or Article 8"
    )

    claims_compliance: bool = Field(
        description="TRUE if policy claims to comply with GDPR requirements"
    )

    consent_methods: List[GDPRConsentMethod] = Field(
        description="List of parental consent verification methods described (from categorized list)"
    )

    consent_method_details: str = Field(
        description="Quoted or paraphrased text from policy describing consent methods"
    )

    lawful_bases: List[GDPRLawfulBasis] = Field(
        description="List of lawful bases claimed for processing children's data (from categorized list)"
    )

    lawful_basis_details: str = Field(
        description="Quoted or paraphrased text from policy describing lawful basis"
    )

    age_threshold_stated: Optional[int] = Field(
        description="Age threshold stated in policy for children's data (13-16 range for GDPR, varies by country)"
    )


class PolicyAnalysisResult(BaseModel):
    """
    Structured output schema for K-12 Educational App Privacy Policy Analysis.
    Based on research framework for evaluating privacy in educational applications.
    """

    model_config = {"extra": "forbid"}

    # Existing 9 boolean indicators
    data_collection_disclosure: bool = Field(
        description="TRUE if policy clearly discloses types of personal data collected (PII, device details, usage data)"
    )

    data_use_purpose_specification: bool = Field(
        description="TRUE if policy specifies purposes for data use AND limits use to those purposes"
    )

    third_party_sharing_disclosure: bool = Field(
        description="TRUE if policy details if/how student data is shared with third parties by name or category"
    )

    third_party_list: List[str] = Field(
        description="List of all third parties mentioned in the policy that receive data (company/service names only)"
    )

    third_party_details: List[ThirdPartyDetail] = Field(
        description="Detailed information about what specific data is shared with each third party"
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

    # NEW: Detailed COPPA analysis
    coppa_analysis: COPPAAnalysis = Field(
        description="Detailed analysis of COPPA compliance and parental consent methods"
    )

    # NEW: Detailed GDPR analysis
    gdpr_analysis: GDPRAnalysis = Field(
        description="Detailed analysis of GDPR compliance for children's data"
    )
