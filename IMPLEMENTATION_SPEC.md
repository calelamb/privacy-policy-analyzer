# Privacy Policy Analyzer — Implementation Spec v2.0
**Feed this file to Claude Code. It contains complete, unambiguous instructions for every change needed.**

---

## Context

This is a K-12 EdTech privacy policy research tool used to analyze ~1,694 app privacy policies for GDPR and COPPA regulatory compliance. The output feeds directly into an AMCIS 2026 academic paper. The current model uses 9 generic boolean indicators. We are refactoring it to use 35 specific indicators that map 1:1 to every row in the paper's regulatory compliance framework (Table 1), plus evidence strings, directionality enums, free-text extraction fields, and Python-computed composite scores.

**Model to use:** `gpt-5.1` (the latest available OpenAI model). Update all references from `gpt-5-nano` to `gpt-5.1` as the default.

**Source data:** `Master Data.csv` in the project root. Policy text is in columns `ppCompany` (vendor's full policy, preferred) and `ppPlatform` (app store label, fallback). There is no pre-built `policy_text` column — it must be constructed at runtime.

---

## Files to Modify

1. `src/models.py` — Complete rewrite of `PolicyAnalysisResult`
2. `src/prompts.py` — Complete rewrite of `SYSTEM_PROMPT`
3. `src/analyzer.py` — Update result construction, add policy text builder, update model default, add composite score computation
4. `src/main.py` — Update `--model` choices and default; add `--input-primary-col` / `--input-fallback-col` flags
5. `cluster_analysis.py` — Update column lists

---

## FILE 1: src/models.py

**Action:** Complete rewrite. Keep all existing enum classes (`COPPAConsentMethod`, `COPPAException`, `GDPRConsentMethod`, `GDPRLawfulBasis`), `ThirdPartyDetail`, `COPPAAnalysis`, and `GDPRAnalysis` exactly as they are. Replace `PolicyAnalysisResult` entirely.

### New Enums to Add

Add these four new enum classes after the existing ones:

```python
class SharingDirectionEnum(str, Enum):
    """Describes what a policy actually claims about data sharing."""
    SHARES = "shares"                      # Explicitly confirms data IS shared with named/categorized parties
    DOES_NOT_SHARE = "does_not_share"      # Explicitly states data is NOT sold or shared
    CONDITIONAL = "conditional"            # Shares only under specific stated conditions (e.g., with consent, legal requirement)
    VAGUE_OR_SILENT = "vague_or_silent"   # Generic language, no clear claim, or topic not addressed


class RetentionSpecificityEnum(str, Enum):
    """Describes how specifically a policy addresses data retention."""
    SPECIFIC_TIMEFRAME = "specific_timeframe"   # Gives explicit duration (e.g., "90 days", "2 years", "30 days after deletion")
    UNTIL_DELETED = "until_deleted"             # Retained until account/data deletion is requested
    AS_LONG_AS_NECESSARY = "as_long_as_necessary"  # General necessity language only, no specific timeframe
    INDEFINITE_OR_SILENT = "indefinite_or_silent"  # No retention limitation stated or topic not addressed


class SecuritySpecificityEnum(str, Enum):
    """Describes how specifically a policy addresses security measures."""
    SPECIFIC_MEASURES = "specific_measures"   # Names concrete measures (e.g., TLS, AES-256, access controls, SOC 2)
    GENERAL_LANGUAGE = "general_language"    # Uses vague language like "industry-standard security" or "we take security seriously"
    SILENT = "silent"                        # No security language at all


class ConsentSpecificityEnum(str, Enum):
    """Describes how specifically a policy describes parental consent procedures."""
    METHOD_DESCRIBED = "method_described"    # Names a specific mechanism (signed form, email+, school consent, etc.)
    MENTIONED_NO_METHOD = "mentioned_no_method"  # References consent requirement but gives no mechanism
    NOT_APPLICABLE = "not_applicable"        # Policy states the service is not directed at children / no children's data collected
```

### New PolicyAnalysisResult

Replace the entire `PolicyAnalysisResult` class with the following. Every boolean indicator has a matching `_evidence` field (type `str`) that holds a short quoted or paraphrased excerpt from the policy justifying the TRUE or FALSE call. If FALSE, the evidence field should contain `"Not found"` or a brief explanation of what's missing.

```python
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
    # Evaluate EACH right independently. Find the rights/data subject rights section first,
    # then assess each right against the full policy text.

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
```

---

## FILE 2: src/prompts.py

**Action:** Complete rewrite of `SYSTEM_PROMPT`. The new prompt must be organized by the 14 regulatory categories matching the model schema above. It instructs the model to work in a structured, step-by-step manner and return evidence for every indicator.

```python
SYSTEM_PROMPT = """You are a legal analyst specializing in privacy regulatory compliance for K-12 educational technology applications. You will analyze a privacy policy and extract structured compliance information across 14 regulatory categories derived from GDPR and COPPA requirements.

CORE RULES:
1. Evaluate ONLY what the policy EXPLICITLY STATES — do not infer, assume, or give credit for implied compliance.
2. CONSERVATIVE BIAS: When in doubt between TRUE and FALSE, always return FALSE. Vague, generic, or boilerplate language does not satisfy a requirement.
3. For every boolean field, return a companion _evidence field containing either: (a) a direct quote or close paraphrase from the policy supporting your TRUE call, or (b) "Not found" if FALSE, optionally noting what language would be needed to satisfy the requirement.
4. Evidence quotes should be concise — 1-3 sentences maximum. Use ellipsis (...) to condense if needed.
5. These are K-12 educational apps. Pay particular attention to children-specific requirements (COPPA). Many policies are written for general users and fail to address children's data specifically — this matters.

CATEGORY 1 — COMPANY IDENTITY
Assess whether the policy identifies who is responsible for data processing.
- ci_controller_identity: The policy must name the data controller/operator AND provide contact information (physical address, email address, or contact form URL). A company name in a header with no contact details = FALSE.
- ci_dpo_contact: The policy must name a Data Protection Officer (by title) and provide their contact details. A generic privacy@company.com without the DPO title = FALSE.
- ci_operator_list: Per COPPA §312.4(d)(1), if multiple operators collect children's data, each must be listed with name, address, telephone, and email. This is a high bar — most policies will be FALSE.

CATEGORY 2 — TYPES OF DATA COLLECTED
Assess whether the policy itemizes the personal data collected.
- td_categories_disclosed: Must list specific data categories (e.g., "name, email address, date of birth, device identifier, usage logs"). "Information you provide to us" without listing categories = FALSE.
- td_children_data_types: Must specifically address data collected FROM CHILDREN, not just general users. If the policy has a "Children's Privacy" or "Under 13" section that lists data types, that qualifies. General data lists do not.
- td_persistent_identifiers: Must explicitly disclose cookies, device IDs, advertising IDs, or similar persistent identifiers. Mentioning "analytics" without specifying the identifier type = FALSE.

CATEGORY 3 — PURPOSE OF COLLECTION/USE
Assess whether the policy explains why data is collected and used.
- pu_purposes_stated: Must list specific purposes. "To improve our services" alone is too vague. "To provide personalized learning recommendations, to communicate progress reports to teachers, and to comply with legal obligations" = TRUE.
- pu_legal_basis: Must explicitly name one or more GDPR lawful bases: consent, contractual necessity, legitimate interests, legal obligation, vital interests, or public task. Simply complying with GDPR without stating a basis = FALSE.
- pu_children_data_use: Must explain specifically how CHILDREN'S data is used. A children's privacy section that says "we use your child's data to provide the Service" with no further detail = borderline FALSE. It must give meaningful purpose language specific to children.

CATEGORY 4 — THIRD-PARTY SHARING
This is critical for K-12 apps. Evaluate carefully.
- ts_recipients_disclosed: Must name specific third parties OR describe them by meaningful category (e.g., "cloud hosting providers", "analytics vendors", "payment processors"). "We may share with service providers" with no further description = FALSE.
- ts_sharing_direction: Choose one value:
  * "shares" — policy confirms data is shared with third parties
  * "does_not_share" — policy explicitly states data is NOT sold or shared with third parties for their own purposes
  * "conditional" — sharing only occurs under stated conditions (legal requirement, consent, business transfer)
  * "vague_or_silent" — unclear or not addressed
- ts_children_data_recipients: Must specifically name or categorize who receives CHILDREN'S data per COPPA §312.4(d)(3). Same standard as above, but child-specific.
- ts_children_sharing_direction: Same vocabulary as ts_sharing_direction, applied specifically to children's data.
- ts_third_party_purpose: Per COPPA §312.4(d)(3), must explain WHY children's data is shared with each named third party. Listing third parties without stating the purpose of each disclosure = FALSE.

CATEGORY 5 — INTERNATIONAL TRANSFERS
- it_eu_transfers: Must (a) disclose that data may be transferred outside the EU/EEA AND (b) name the safeguard used (Standard Contractual Clauses, adequacy decision, Binding Corporate Rules, etc.). Mentioning "international" servers without EU-specific safeguards = FALSE. Apps not mentioning EU users at all = FALSE.

CATEGORY 6 — RETENTION
- re_retention_period: Must state a retention timeframe OR criteria for determining retention. "We retain data until you delete your account" = TRUE. "We may delete data when no longer needed" with no further specification = borderline FALSE (too vague).
- re_retention_specificity: Classify as: specific_timeframe / until_deleted / as_long_as_necessary / indefinite_or_silent.
- re_retention_stated_period: Extract the literal phrase used (e.g., "90 days", "for the duration of the school year plus one additional year", "upon written request from a parent"). Write "Not stated" if absent.
- re_children_retention: Must specifically address children's data retention and state it is kept only as long as necessary. A general retention policy that doesn't mention children = FALSE.

CATEGORY 7 — USER AND PARENT RIGHTS
This section has 11 separate fields. Locate the rights/data subject rights section of the policy first, then evaluate each right independently. Many policies list GDPR rights in bulk — read carefully to determine which specific rights are actually mentioned.

GDPR rights to evaluate (each independently):
- ur_right_access: Right to obtain a copy of personal data (GDPR Art. 15)
- ur_right_rectification: Right to correct inaccurate data (GDPR Art. 16)
- ur_right_erasure: Right to delete data / be forgotten (GDPR Art. 17)
- ur_right_restrict: Right to limit how data is used without deleting it (GDPR Art. 18)
- ur_right_portability: Right to receive data in machine-readable format (GDPR Art. 20)
- ur_right_object: Right to object to processing, especially direct marketing (GDPR Art. 21)
- ur_right_withdraw_consent: Right to withdraw consent at any time (GDPR Art. 13(2)(c))
- ur_right_supervisory_complaint: Right to complain to a data protection authority (GDPR Art. 13(2)(d))

COPPA parent rights to evaluate (each independently):
- ur_parent_review_right: Parent right to review child's personal information (COPPA §312.6)
- ur_parent_delete_right: Parent right to delete child's personal information (COPPA §312.6(a)(2))
- ur_parent_refuse_right: Parent right to refuse further collection or use (COPPA §312.6(a)(1))

Note: A policy that says "you have the right to access, correct, and delete your data" satisfies ur_right_access, ur_right_rectification, and ur_right_erasure but NOT ur_right_restrict, ur_right_portability, ur_right_object, ur_right_withdraw_consent, or ur_right_supervisory_complaint.

CATEGORY 8 — AUTOMATED DECISION-MAKING
- adm_profiling_disclosure: Must explicitly mention automated decision-making, profiling, or algorithmic processing that has legal or significant effects. Standard analytics and reporting do NOT qualify. Adaptive learning algorithms that affect student placements or grades MAY qualify — use judgment. Absence of any mention = FALSE.

CATEGORY 9 — DATA PROVISION REQUIREMENTS
- dp_mandatory_disclosure: Must address TWO things: (1) whether providing data is mandatory or voluntary, AND (2) what happens if the user refuses. Both must be present for TRUE. "You can choose not to provide information" without explaining the consequences = FALSE.

CATEGORY 10 — SECURITY
- sec_coppa_safeguards: Must describe SPECIFIC security procedures for children's data. "We use industry-standard security" = FALSE. "We use TLS encryption and restrict access to authorized personnel" = TRUE.
- sec_gdpr_measures: Same standard — must name specific technical or organizational measures. Generic security claims = FALSE.
- sec_specificity: Classify as: specific_measures / general_language / silent.
- sec_measures_listed: Extract all specific security measures named as a comma-separated list. "None specified" if none.

CATEGORY 11 — POLICY ACCESSIBILITY
- pa_concise_transparent: Must contain a statement that the policy is written to be concise, transparent, and easily understandable (the policy asserting this about itself, not your judgment of it).
- pa_prominent_link: Must state that the policy is available via a prominent link on the website or in the app.

CATEGORY 12 — UPDATES/CHANGES
- up_material_changes_notice: Must commit to NOTIFYING users/parents before implementing material changes. "We reserve the right to update this policy" without notification commitment = FALSE. "We will notify you by email before any material changes take effect" = TRUE.

CATEGORY 13 — CONSENT MECHANISMS
- cm_parental_consent_procedures: Must describe HOW parental consent is obtained — the actual mechanism or procedure. "We require parental consent for children under 13" without describing the process = FALSE.
- cm_consent_specificity: Classify as: method_described / mentioned_no_method / not_applicable.

CATEGORY 14 — DATA SOURCE
- ds_indirect_data_source: Must disclose sources of data NOT collected directly from the user (e.g., "we receive information about you from our business partners", "we infer interests from browsing behavior collected by our advertising partners"). If all data comes directly from user input, write "Not applicable — all data collected directly from user" in the evidence field.

THIRD-PARTY EXTRACTION (always perform, regardless of ts_recipients_disclosed value):
Search the ENTIRE policy exhaustively for any mention of third-party companies, services, platforms, or vendors that receive or process user data. Look in: data sharing sections, analytics sections, advertising sections, cookies/tracking sections, service provider lists, security sections, payment sections, social media integrations, international transfer sections, and acquisition/merger clauses.

For each third party found:
- name: Exact company/service name
- purpose: Why data is shared (analytics, advertising, cloud hosting, payment processing, etc.)
- data_shared: Specific data types shared (be specific — not just "personal information")

Common third parties to watch for: Google Analytics, Google Firebase, Facebook/Meta Pixel, Amazon AWS, Microsoft Azure, Stripe, Twilio, Salesforce, HubSpot, Mixpanel, Amplitude, Segment, Intercom, Zendesk, Cloudflare, SendGrid, Apple, advertising networks (DoubleClick, AdMob, etc.), data brokers.

COPPA NESTED ANALYSIS:
Complete the coppa_analysis object per COPPA-specific analysis. This supplements the boolean indicators with categorized consent method classification and exception identification.

GDPR NESTED ANALYSIS:
Complete the gdpr_analysis object per GDPR-specific analysis. This supplements the boolean indicators with categorized consent method and lawful basis classification.

Remember: you are evaluating a privacy policy for a K-12 educational app. Children's data protection is the highest priority. Be precise, be conservative, and always provide evidence."""
```

---

## FILE 3: src/analyzer.py

**Action:** Several targeted changes. Do NOT rewrite the entire file — make surgical modifications.

### Change 1: Add policy text builder function

Add this function after the existing `_make_openai_compatible_schema` function:

```python
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
```

### Change 2: Update `_extract_coppa_fields` and `_extract_gdpr_fields`

These functions are unchanged — keep them exactly as they are.

### Change 3: Add composite score computation function

Add this function after `_get_empty_gdpr_fields`:

```python
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
    """Compute GDPR, COPPA, and overall composite scores from indicator dict."""

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
```

### Change 4: Add new field extraction helpers

Add these two helpers (they work alongside the existing `_extract_coppa_fields` and `_extract_gdpr_fields`):

```python
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
    """Extract all Table 1 indicator booleans, evidence strings, and enum fields."""
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
    """Return empty Table 1 fields for error/skip cases."""
    result = {}
    for field in TABLE1_BOOLEAN_FIELDS:
        result[field] = False
    for field in TABLE1_EVIDENCE_FIELDS:
        result[field] = ""
    for field in TABLE1_ENUM_FIELDS:
        result[field] = ""
    return result
```

### Change 5: Update MODEL_PRICING and default model

In the `PolicyAnalyzer` class, update:

```python
MODEL_PRICING = {
    "gpt-5.1": {"input": 2.00, "output": 8.00},        # Update with actual pricing
    "gpt-4.1": {"input": 2.00, "output": 8.00},         # Update with actual pricing
    "gpt-4.1-mini": {"input": 0.40, "output": 1.60},    # Update with actual pricing
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    "gpt-5-nano": {"input": 0.10, "output": 0.40},
}

def __init__(self, api_key: str, model: str = "gpt-5.1"):  # Changed default from gpt-5-nano
```

Also update the temperature logic: change `temperature = 0.1` to `temperature = 0` everywhere it appears. And update the nano check to be more general:

```python
# Remove the "only add temperature for non-nano models" special case.
# Always add temperature=0 for all models including gpt-5.1
# Remove this block:
#   if "nano" not in self.model.lower():
#       request_params["temperature"] = 0.1
# Replace with:
request_params["temperature"] = 0
```

### Change 6: Update `_process_single_policy` result construction

The result dict in `_process_single_policy` (used by `process_batch_concurrent`) needs to be updated. Find the two places where result dicts are built (success case and error case) and replace them:

**Error/skip case** (when policy is too short or analysis failed):
```python
return {
    "app_id": app_id,
    "app_name": app_name,
    "error": "empty_or_short_policy",  # or "analysis_failed"
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
```

**Success case** (when analysis returns a result):
```python
# Format third party information for CSV output
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
```

Apply the **same pattern** to the synchronous `process_batch` method's result construction blocks and `analyze_single_file`.

### Change 7: Update policy text extraction in `_process_single_policy`

The current code reads `policy_text = row.get(policy_column, "")`. Add a fallback to use `build_policy_text` when processing from Master Data.csv:

```python
# Build policy text: use specified column if it exists and is substantive,
# otherwise use build_policy_text to combine ppCompany + ppPlatform
policy_text = row.get(policy_column, "")
if pd.isna(policy_text) or len(str(policy_text).strip()) < 100:
    # Try building from ppCompany/ppPlatform if available
    if 'ppCompany' in row.index or 'ppPlatform' in row.index:
        policy_text = build_policy_text(row)
    else:
        policy_text = ""
```

Apply the same logic in `process_batch`.

---

## FILE 4: src/main.py

**Action:** Minor updates only.

### Change 1: Update `--model` choices and default

```python
parser.add_argument(
    "--model",
    default="gpt-5.1",
    choices=["gpt-5.1", "gpt-4.1", "gpt-4.1-mini", "gpt-4o-mini", "gpt-4o", "gpt-5-nano", "gpt-3.5-turbo"],
    help="OpenAI model to use (default: gpt-5.1, recommended for research-quality analysis)"
)
```

### Change 2: Add primary/fallback policy column flags

```python
parser.add_argument(
    "--policy-column-primary",
    default=None,
    help="Primary column for policy text (default: uses --policy-column). "
         "When processing Master Data.csv, use 'ppCompany'."
)
parser.add_argument(
    "--policy-column-fallback",
    default=None,
    help="Fallback column for policy text when primary is empty. "
         "When processing Master Data.csv, use 'ppPlatform'."
)
```

Update the section that calls `process_batch` / `process_batch_concurrent` to pass the primary column as `policy_column`. The fallback logic is already handled inside `build_policy_text`.

---

## FILE 5: cluster_analysis.py

**Action:** Update column lists only. Logic stays identical.

```python
CLUSTERING_COLUMNS = [
    # Use the 14 most interpretable indicators for clustering
    "ci_controller_identity",
    "td_categories_disclosed",
    "pu_purposes_stated",
    "ts_recipients_disclosed",
    "re_retention_period",
    "ur_right_erasure",
    "ur_parent_delete_right",
    "sec_coppa_safeguards",
    "sec_gdpr_measures",
    "cm_parental_consent_procedures",
    "up_material_changes_notice",
    "td_children_data_types",
    "pu_children_data_use",
    "it_eu_transfers",
]

SCORING_COLUMNS = TABLE1_BOOLEAN_FIELDS  # Import this from analyzer.py or redefine it
```

For the `compute_compliance_score` function, update to use the pre-computed composite scores rather than recomputing:

```python
def compute_compliance_score(df: pd.DataFrame) -> pd.DataFrame:
    """Use pre-computed composite scores from analyzer output."""
    # If composite scores are already in the dataframe, use them directly
    if "overall_composite_pct" in df.columns:
        df["compliance_score"] = df["overall_composite_pct"]
    else:
        # Fallback: compute from boolean columns
        df["compliance_score"] = (
            df[SCORING_COLUMNS].fillna(False).astype(int).sum(axis=1) / len(SCORING_COLUMNS) * 100
        ).round(2)
    return df
```

---

## Running the Re-Analysis

Once all changes are implemented, run the full analysis with:

```bash
# From the project root
python -m src.main "Master Data.csv" "data/output/Analyzed_Policies_v2.csv" \
  --policy-column ppCompany \
  --id-column app_id \
  --name-column app_name \
  --model gpt-5.1 \
  --concurrent \
  --max-concurrent 10
```

**Validation run first (10 apps):**
```bash
python -m src.main "data/input/test_sample_5.csv" "data/output/test_v2.csv" \
  --policy-column ppCompany \
  --model gpt-5.1 \
  --concurrent \
  --max-concurrent 3
```

After validation, hand-check the evidence strings for 3-5 policies against the raw policy text to confirm the model is citing real text and not hallucinating.

---

## Expected Output Schema

The output CSV `Analyzed_Policies_v2.csv` will have the following columns in order:

```
app_id, app_name, error,
# Table 1 booleans (35)
ci_controller_identity, ci_controller_identity_evidence,
ci_dpo_contact, ci_dpo_contact_evidence,
ci_operator_list, ci_operator_list_evidence,
td_categories_disclosed, td_categories_disclosed_evidence,
td_children_data_types, td_children_data_types_evidence,
td_persistent_identifiers, td_persistent_identifiers_evidence,
pu_purposes_stated, pu_purposes_stated_evidence,
pu_legal_basis, pu_legal_basis_evidence,
pu_children_data_use, pu_children_data_use_evidence,
ts_recipients_disclosed, ts_recipients_disclosed_evidence,
ts_sharing_direction,
ts_children_data_recipients, ts_children_data_recipients_evidence,
ts_children_sharing_direction,
ts_third_party_purpose, ts_third_party_purpose_evidence,
it_eu_transfers, it_eu_transfers_evidence,
re_retention_period, re_retention_period_evidence,
re_retention_specificity, re_retention_stated_period,
re_children_retention, re_children_retention_evidence,
ur_right_access, ur_right_access_evidence,
ur_right_rectification, ur_right_rectification_evidence,
ur_right_erasure, ur_right_erasure_evidence,
ur_right_restrict, ur_right_restrict_evidence,
ur_right_portability, ur_right_portability_evidence,
ur_right_object, ur_right_object_evidence,
ur_right_withdraw_consent, ur_right_withdraw_consent_evidence,
ur_right_supervisory_complaint, ur_right_supervisory_complaint_evidence,
ur_parent_review_right, ur_parent_review_right_evidence,
ur_parent_delete_right, ur_parent_delete_right_evidence,
ur_parent_refuse_right, ur_parent_refuse_right_evidence,
adm_profiling_disclosure, adm_profiling_disclosure_evidence,
dp_mandatory_disclosure, dp_mandatory_disclosure_evidence,
sec_coppa_safeguards, sec_coppa_safeguards_evidence,
sec_gdpr_measures, sec_gdpr_measures_evidence,
sec_specificity, sec_measures_listed,
pa_concise_transparent, pa_concise_transparent_evidence,
pa_prominent_link, pa_prominent_link_evidence,
up_material_changes_notice, up_material_changes_notice_evidence,
cm_parental_consent_procedures, cm_parental_consent_procedures_evidence,
cm_consent_specificity,
ds_indirect_data_source, ds_indirect_data_source_evidence,
# Third-party extraction
third_party_list, third_party_data_shared,
# COPPA nested analysis (flattened)
coppa_mentions, coppa_claims_compliance, coppa_consent_methods,
coppa_consent_details, coppa_exceptions, coppa_exception_details, coppa_age_threshold,
# GDPR nested analysis (flattened)
gdpr_mentions, gdpr_claims_compliance, gdpr_consent_methods,
gdpr_consent_details, gdpr_lawful_bases, gdpr_lawful_basis_details, gdpr_age_threshold,
# Composite scores
gdpr_composite_score, gdpr_composite_pct,
coppa_composite_score, coppa_composite_pct,
overall_composite_score, overall_composite_pct
```

Total: ~95 columns.

---

## Key Constraints to Preserve

1. **`_make_openai_compatible_schema()`** — Keep this function exactly as-is. It is required for OpenAI structured output compatibility and must continue to be applied to the new schema.
2. **Async/concurrent processing** — Keep `process_batch_concurrent` and the semaphore pattern unchanged.
3. **Rate limit retry logic** — Keep the `RateLimitError` catch and 60-second sleep in both sync and async methods.
4. **Resume-from-index logic** — Keep `--resume-from` flag behavior unchanged.
5. **Incremental saves every 50 rows** — Keep this pattern unchanged in both batch methods.
6. **`COPPAAnalysis`, `GDPRAnalysis`, `ThirdPartyDetail` models** — Keep exactly as-is. Do not modify.
7. **`_extract_coppa_fields()` and `_extract_gdpr_fields()`** — Keep exactly as-is.
