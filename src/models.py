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


class SharingDirectionEnum(str, Enum):
    """Describes what a policy actually claims about data sharing."""
    SHARES = "shares"
    DOES_NOT_SHARE = "does_not_share"
    CONDITIONAL = "conditional"
    VAGUE_OR_SILENT = "vague_or_silent"


class RetentionSpecificityEnum(str, Enum):
    """Describes how specifically a policy addresses data retention."""
    SPECIFIC_TIMEFRAME = "specific_timeframe"
    UNTIL_DELETED = "until_deleted"
    AS_LONG_AS_NECESSARY = "as_long_as_necessary"
    INDEFINITE_OR_SILENT = "indefinite_or_silent"


class SecuritySpecificityEnum(str, Enum):
    """Describes how specifically a policy addresses security measures."""
    SPECIFIC_MEASURES = "specific_measures"
    GENERAL_LANGUAGE = "general_language"
    SILENT = "silent"


class ConsentSpecificityEnum(str, Enum):
    """Describes how specifically a policy describes parental consent procedures."""
    METHOD_DESCRIBED = "method_described"
    MENTIONED_NO_METHOD = "mentioned_no_method"
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
    Structured output schema for K-12 EdTech Privacy Policy Analysis.
    Implements the full Table 1 regulatory disclosure framework (GDPR + COPPA).
    Each boolean indicator has a companion _evidence field with supporting text.
    """

    model_config = {"extra": "forbid"}

    # ── CATEGORY 1: COMPANY IDENTITY ─────────────────────────────────────────

    ci_controller_identity: bool = Field(
        description="TRUE if the policy identifies the data controller or operator by name AND provides contact details (address, email, or contact form). Both name and contact are required. FALSE if only the company name appears in a header with no contact information."
    )
    ci_controller_identity_evidence: str = Field(
        description="Quote or paraphrase the text identifying the controller and their contact details. If FALSE, write 'Not found' or describe what is missing."
    )

    ci_dpo_contact: bool = Field(
        description="TRUE if the policy explicitly provides contact details for a Data Protection Officer (DPO). Must name the role (DPO, Data Protection Officer, or equivalent) and give contact info. FALSE if only a general privacy contact is given without the DPO title."
    )
    ci_dpo_contact_evidence: str = Field(
        description="Quote or paraphrase the DPO contact information. If FALSE, write 'Not found'."
    )

    ci_operator_list: bool = Field(
        description="TRUE if the policy lists all operators (companies) collecting or maintaining children's personal information, with their name, address, telephone number, and email address as required by COPPA §312.4(d)(1). FALSE if operators are named but contact details are incomplete."
    )
    ci_operator_list_evidence: str = Field(
        description="Quote or paraphrase the operator list with contact details. If FALSE, write 'Not found' or describe what contact information is missing."
    )

    # ── CATEGORY 2: TYPES OF DATA COLLECTED ──────────────────────────────────

    td_categories_disclosed: bool = Field(
        description="TRUE if the policy explicitly lists or describes categories of personal data collected (e.g., name, email, device ID, usage data, location). A general statement like 'we collect information you provide' without listing categories = FALSE."
    )
    td_categories_disclosed_evidence: str = Field(
        description="Quote or paraphrase the data categories listed. If FALSE, write 'Not found' or note that only vague language is used."
    )

    td_children_data_types: bool = Field(
        description="TRUE if the policy specifically identifies the types of personal information collected FROM CHILDREN (not just general users). Must be child-specific disclosure per COPPA §312.4(d)(2). A general data list that doesn't distinguish children's data = FALSE."
    )
    td_children_data_types_evidence: str = Field(
        description="Quote or paraphrase the child-specific data types disclosure. If FALSE, write 'Not found'."
    )

    td_persistent_identifiers: bool = Field(
        description="TRUE if the policy explicitly discloses the collection of persistent identifiers such as cookies, device IDs, advertising IDs, IP addresses used as identifiers, or similar tracking technologies. Vague references to 'analytics' without specifying identifier types = FALSE."
    )
    td_persistent_identifiers_evidence: str = Field(
        description="Quote or paraphrase the persistent identifier disclosure. If FALSE, write 'Not found'."
    )

    # ── CATEGORY 3: PURPOSE OF COLLECTION/USE ────────────────────────────────

    pu_purposes_stated: bool = Field(
        description="TRUE if the policy states the specific purposes for which personal data is processed (e.g., 'to provide educational services', 'for analytics', 'to send newsletters'). A generic 'to improve our services' without specifics = FALSE."
    )
    pu_purposes_stated_evidence: str = Field(
        description="Quote or paraphrase the stated purposes. If FALSE, write 'Not found' or note that only vague language is used."
    )

    pu_legal_basis: bool = Field(
        description="TRUE if the policy explicitly states the legal basis for processing personal data under GDPR (e.g., consent, contractual necessity, legitimate interests, legal obligation, vital interests, public task). Simply mentioning GDPR without stating a legal basis = FALSE."
    )
    pu_legal_basis_evidence: str = Field(
        description="Quote or paraphrase the stated legal basis/bases. If FALSE, write 'Not found'."
    )

    pu_children_data_use: bool = Field(
        description="TRUE if the policy specifically explains how children's personal information is USED — not just collected. Must address the purpose of use for children's data specifically per COPPA §312.4(d)(2). A general use statement that doesn't distinguish children = FALSE."
    )
    pu_children_data_use_evidence: str = Field(
        description="Quote or paraphrase the child-specific data use explanation. If FALSE, write 'Not found'."
    )

    # ── CATEGORY 4: THIRD-PARTY SHARING ──────────────────────────────────────

    ts_recipients_disclosed: bool = Field(
        description="TRUE if the policy identifies recipients or categories of recipients to whom personal data is disclosed — by name or by category (e.g., 'analytics providers', 'cloud storage vendors', 'advertising partners'). A vague statement like 'we may share with third parties' with no categories or names = FALSE."
    )
    ts_recipients_disclosed_evidence: str = Field(
        description="Quote or paraphrase the recipient disclosure. If FALSE, write 'Not found' or quote the vague language used."
    )

    ts_sharing_direction: SharingDirectionEnum = Field(
        description="Characterize the DIRECTION of the third-party sharing disclosure: 'shares' if the policy confirms data IS shared; 'does_not_share' if it explicitly states data is NOT sold or shared with third parties for their own use; 'conditional' if sharing only happens under specific stated conditions; 'vague_or_silent' if the language is ambiguous or the topic is not addressed."
    )

    ts_children_data_recipients: bool = Field(
        description="TRUE if the policy specifically identifies the third parties that collect or receive CHILDREN'S personal information, as required by COPPA §312.4(d)(3). A general third-party list that doesn't distinguish children's data = FALSE."
    )
    ts_children_data_recipients_evidence: str = Field(
        description="Quote or paraphrase the child-specific third-party disclosure. If FALSE, write 'Not found'."
    )

    ts_children_sharing_direction: SharingDirectionEnum = Field(
        description="Same as ts_sharing_direction but specifically for children's data. Use 'not_applicable' is not an option — default to 'vague_or_silent' if children's data sharing is not addressed."
    )

    ts_third_party_purpose: bool = Field(
        description="TRUE if the policy states the PURPOSE of each third-party disclosure for children's data per COPPA §312.4(d)(3) — why children's data is shared with each third party. Listing third parties without explaining why = FALSE."
    )
    ts_third_party_purpose_evidence: str = Field(
        description="Quote or paraphrase the third-party purpose disclosure for children's data. If FALSE, write 'Not found'."
    )

    # ── CATEGORY 5: INTERNATIONAL TRANSFERS ──────────────────────────────────

    it_eu_transfers: bool = Field(
        description="TRUE if the policy discloses that personal data may be transferred outside the European Union/EEA AND describes the safeguards used (e.g., Standard Contractual Clauses, adequacy decisions, Privacy Shield successor frameworks). Mentioning international users without addressing EU transfer safeguards = FALSE."
    )
    it_eu_transfers_evidence: str = Field(
        description="Quote or paraphrase the international transfer disclosure and safeguards. If FALSE, write 'Not found'."
    )

    # ── CATEGORY 6: RETENTION ─────────────────────────────────────────────────

    re_retention_period: bool = Field(
        description="TRUE if the policy states a data retention period OR the criteria used to determine how long data is retained (e.g., 'we retain data for 2 years', 'data is deleted 30 days after account closure', 'retained as long as your account is active'). Saying 'we may delete data' without any timeframe or criteria = FALSE."
    )
    re_retention_period_evidence: str = Field(
        description="Quote or paraphrase the retention period or criteria. If FALSE, write 'Not found'."
    )
    re_retention_specificity: RetentionSpecificityEnum = Field(
        description="Classify how specifically retention is addressed. 'specific_timeframe': explicit duration given. 'until_deleted': tied to account/data deletion request. 'as_long_as_necessary': only general necessity language. 'indefinite_or_silent': no limitation stated."
    )
    re_retention_stated_period: str = Field(
        description="Extract the LITERAL retention timeframe or criterion stated in the policy (e.g., '90 days', '2 years after account closure', 'as long as necessary to provide services', 'upon written request'). If not stated, write 'Not stated'."
    )

    re_children_retention: bool = Field(
        description="TRUE if the policy specifically states that children's personal information is retained ONLY AS LONG AS NECESSARY to fulfill the purpose for which it was collected, per COPPA §312.10. A general retention policy that doesn't address children's data specifically = FALSE."
    )
    re_children_retention_evidence: str = Field(
        description="Quote or paraphrase the child-specific retention statement. If FALSE, write 'Not found'."
    )

    # ── CATEGORY 7: USER/PARENT RIGHTS ───────────────────────────────────────

    ur_right_access: bool = Field(
        description="TRUE if the policy explicitly grants users the right to ACCESS or obtain a copy of their personal data (GDPR Art. 15). Must be explicit — a general 'contact us' link without mentioning data access = FALSE."
    )
    ur_right_access_evidence: str = Field(
        description="Quote or paraphrase the access right language. If FALSE, write 'Not found'."
    )

    ur_right_rectification: bool = Field(
        description="TRUE if the policy explicitly grants users the right to CORRECT or UPDATE inaccurate personal data (GDPR Art. 16). FALSE if only deletion is mentioned without correction."
    )
    ur_right_rectification_evidence: str = Field(
        description="Quote or paraphrase the rectification right language. If FALSE, write 'Not found'."
    )

    ur_right_erasure: bool = Field(
        description="TRUE if the policy explicitly grants users the right to DELETE or ERASE their personal data (GDPR Art. 17 / 'right to be forgotten'). Must be an explicit right — mentioning data deletion as a company practice without granting it as a user right = FALSE."
    )
    ur_right_erasure_evidence: str = Field(
        description="Quote or paraphrase the erasure right language. If FALSE, write 'Not found'."
    )

    ur_right_restrict: bool = Field(
        description="TRUE if the policy explicitly grants users the right to RESTRICT processing of their personal data (GDPR Art. 18) — i.e., the right to limit how data is used without deleting it. FALSE if only deletion or opt-out of marketing is mentioned."
    )
    ur_right_restrict_evidence: str = Field(
        description="Quote or paraphrase the restriction right language. If FALSE, write 'Not found'."
    )

    ur_right_portability: bool = Field(
        description="TRUE if the policy explicitly grants users the right to DATA PORTABILITY — receiving their data in a structured, machine-readable format (GDPR Art. 20). FALSE unless portability is explicitly mentioned."
    )
    ur_right_portability_evidence: str = Field(
        description="Quote or paraphrase the portability right language. If FALSE, write 'Not found'."
    )

    ur_right_object: bool = Field(
        description="TRUE if the policy explicitly grants users the right to OBJECT to processing of their personal data (GDPR Art. 21), including objecting to direct marketing or processing based on legitimate interests. General opt-out language = FALSE unless it specifically mentions objecting to processing."
    )
    ur_right_object_evidence: str = Field(
        description="Quote or paraphrase the right to object language. If FALSE, write 'Not found'."
    )

    ur_right_withdraw_consent: bool = Field(
        description="TRUE if the policy explicitly states that users can WITHDRAW CONSENT at any time (GDPR Art. 13(2)(c)), and that withdrawal does not affect the lawfulness of prior processing. Mentioning consent without the right to withdraw = FALSE."
    )
    ur_right_withdraw_consent_evidence: str = Field(
        description="Quote or paraphrase the consent withdrawal language. If FALSE, write 'Not found'."
    )

    ur_right_supervisory_complaint: bool = Field(
        description="TRUE if the policy explicitly informs users of their right to LODGE A COMPLAINT with a data protection supervisory authority (GDPR Art. 13(2)(d)) — e.g., their national DPA or the ICO. A general 'contact us with complaints' link = FALSE."
    )
    ur_right_supervisory_complaint_evidence: str = Field(
        description="Quote or paraphrase the supervisory authority complaint language. If FALSE, write 'Not found'."
    )

    ur_parent_review_right: bool = Field(
        description="TRUE if the policy explicitly grants PARENTS the right to REVIEW the personal information collected from their child (COPPA §312.6). Must be child/parent-specific — a general user access right is insufficient."
    )
    ur_parent_review_right_evidence: str = Field(
        description="Quote or paraphrase the parent review right language. If FALSE, write 'Not found'."
    )

    ur_parent_delete_right: bool = Field(
        description="TRUE if the policy explicitly grants parents the right to DELETE or have DELETED the personal information collected from their child (COPPA §312.6(a)(2)). Must be child/parent-specific."
    )
    ur_parent_delete_right_evidence: str = Field(
        description="Quote or paraphrase the parent deletion right language. If FALSE, write 'Not found'."
    )

    ur_parent_refuse_right: bool = Field(
        description="TRUE if the policy explicitly grants parents the right to REFUSE FURTHER COLLECTION or use of their child's personal information (COPPA §312.6(a)(1)). Mentioning parental consent without the right to refuse further collection = FALSE."
    )
    ur_parent_refuse_right_evidence: str = Field(
        description="Quote or paraphrase the parent refusal right language. If FALSE, write 'Not found'."
    )

    # ── CATEGORY 8: AUTOMATED DECISION-MAKING ────────────────────────────────

    adm_profiling_disclosure: bool = Field(
        description="TRUE if the policy discloses the use of PROFILING or AUTOMATED DECISION-MAKING that produces legal or similarly significant effects (GDPR Art. 13(2)(f), Art. 22). Must explicitly mention automated decisions, profiling, or algorithmic processing of user data. FALSE if only standard analytics is mentioned without reference to automated decisions."
    )
    adm_profiling_disclosure_evidence: str = Field(
        description="Quote or paraphrase the automated decision-making/profiling disclosure. If FALSE, write 'Not found'."
    )

    # ── CATEGORY 9: DATA PROVISION REQUIREMENTS ──────────────────────────────

    dp_mandatory_disclosure: bool = Field(
        description="TRUE if the policy explicitly states whether providing personal data is mandatory or voluntary, AND describes the consequences of refusing to provide it (GDPR Art. 13(2)(e)). FALSE unless both the mandatory/voluntary status AND consequences are addressed."
    )
    dp_mandatory_disclosure_evidence: str = Field(
        description="Quote or paraphrase the data provision requirement and consequences language. If FALSE, write 'Not found'."
    )

    # ── CATEGORY 10: SECURITY ─────────────────────────────────────────────────

    sec_coppa_safeguards: bool = Field(
        description="TRUE if the policy describes REASONABLE security procedures to protect children's personal information from unauthorized access, use, or disclosure (COPPA §312.8). Must describe actual safeguards — 'we take security seriously' without any specifics = FALSE."
    )
    sec_coppa_safeguards_evidence: str = Field(
        description="Quote or paraphrase the COPPA security safeguards description. If FALSE, write 'Not found' or quote the vague language."
    )

    sec_gdpr_measures: bool = Field(
        description="TRUE if the policy describes appropriate technical and/or organizational security measures for protecting personal data (GDPR Art. 5(1)(f), Art. 32). Must name specific measure types — encryption, pseudonymization, access controls, regular testing, etc. Generic 'industry-standard security' = FALSE."
    )
    sec_gdpr_measures_evidence: str = Field(
        description="Quote or paraphrase the GDPR security measures description. If FALSE, write 'Not found' or quote the vague language."
    )
    sec_specificity: SecuritySpecificityEnum = Field(
        description="Classify the specificity of security disclosures overall. 'specific_measures': names concrete technical measures. 'general_language': vague security claims only. 'silent': no security language at all."
    )
    sec_measures_listed: str = Field(
        description="Extract the SPECIFIC security measures named in the policy as a comma-separated list (e.g., 'TLS encryption, AES-256 at rest, role-based access controls, annual penetration testing, SOC 2 Type II'). If no specific measures are named, write 'None specified'."
    )

    # ── CATEGORY 11: POLICY ACCESSIBILITY ────────────────────────────────────

    pa_concise_transparent: bool = Field(
        description="TRUE if the policy contains a statement or commitment that it is written to be concise, transparent, intelligible, and easily accessible (GDPR Art. 12(1)). The policy must assert this about itself — do not evaluate readability yourself. FALSE if no such commitment is stated."
    )
    pa_concise_transparent_evidence: str = Field(
        description="Quote or paraphrase the transparency/accessibility commitment. If FALSE, write 'Not found'."
    )

    pa_prominent_link: bool = Field(
        description="TRUE if the policy states that it is available via a clear and prominent link on the operator's website or in the app, per COPPA §312.4(d). FALSE if the policy's online availability is not addressed."
    )
    pa_prominent_link_evidence: str = Field(
        description="Quote or paraphrase the prominent link disclosure. If FALSE, write 'Not found'."
    )

    # ── CATEGORY 12: UPDATES/CHANGES ─────────────────────────────────────────

    up_material_changes_notice: bool = Field(
        description="TRUE if the policy commits to notifying users or parents of MATERIAL CHANGES to its data practices before implementing them (COPPA §312.4(b), §312.5(c)). A statement that 'we may update this policy' without committing to notification = FALSE."
    )
    up_material_changes_notice_evidence: str = Field(
        description="Quote or paraphrase the material changes notification commitment. If FALSE, write 'Not found' or quote the weaker language used."
    )

    # ── CATEGORY 13: CONSENT MECHANISMS ──────────────────────────────────────

    cm_parental_consent_procedures: bool = Field(
        description="TRUE if the policy describes the PROCEDURES used to obtain verifiable parental consent under COPPA §312.5 — i.e., HOW parental consent is obtained. Simply stating that parental consent is required without describing the procedure = FALSE."
    )
    cm_parental_consent_procedures_evidence: str = Field(
        description="Quote or paraphrase the parental consent procedure description. If FALSE, write 'Not found' or note that consent is mentioned but not the procedure."
    )
    cm_consent_specificity: ConsentSpecificityEnum = Field(
        description="Classify the specificity of parental consent procedures. 'method_described': a specific mechanism is named (signed form, email+, phone, school consent, etc.). 'mentioned_no_method': consent is mentioned but procedure is not described. 'not_applicable': policy states service is not directed at children."
    )

    # ── CATEGORY 14: DATA SOURCE ──────────────────────────────────────────────

    ds_indirect_data_source: bool = Field(
        description="TRUE if the policy discloses the SOURCE of personal data when it is NOT collected directly from the user themselves (GDPR Art. 14(2)(f)) — e.g., data obtained from third parties, public sources, or inferred from behavior. FALSE if all data is collected directly from the user and no indirect sources exist, OR if indirect sources exist but are not disclosed."
    )
    ds_indirect_data_source_evidence: str = Field(
        description="Quote or paraphrase the indirect data source disclosure. If FALSE, write 'Not found' or 'Not applicable — all data collected directly from user'."
    )

    # ── RETAINED: THIRD-PARTY EXTRACTION ─────────────────────────────────────

    third_party_list: List[str] = Field(
        description="Exhaustive list of all third-party company or service names mentioned in the policy that receive or process user data. Include analytics services, ad networks, cloud providers, payment processors, CDNs, authentication providers, social media integrations. Empty list if none mentioned."
    )

    third_party_details: List[ThirdPartyDetail] = Field(
        description="For each third party in third_party_list, provide structured details: name, purpose of sharing, and specific data types shared."
    )

    # ── RETAINED: COPPA NESTED ANALYSIS ──────────────────────────────────────

    coppa_analysis: COPPAAnalysis = Field(
        description="Detailed COPPA compliance analysis including consent methods, exceptions claimed, and age threshold."
    )

    # ── RETAINED: GDPR NESTED ANALYSIS ───────────────────────────────────────

    gdpr_analysis: GDPRAnalysis = Field(
        description="Detailed GDPR compliance analysis including consent methods, lawful bases, and age threshold."
    )
