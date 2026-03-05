"""
FastAPI backend wrapping PolicyAnalyzer for interactive privacy policy analysis.
"""

import os
import re
from typing import Optional

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.analyzer import PolicyAnalyzer

app = FastAPI(title="EdTech Privacy Policy Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Singleton analyzer instance
_analyzer: Optional[PolicyAnalyzer] = None


def get_analyzer() -> PolicyAnalyzer:
    global _analyzer
    if _analyzer is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="OPENAI_API_KEY not set")
        _analyzer = PolicyAnalyzer(api_key=api_key)
    return _analyzer


class AnalyzeRequest(BaseModel):
    policy_text: Optional[str] = None
    policy_url: Optional[str] = None


INDICATOR_KEYS = [
    "data_collection_disclosure",
    "data_use_purpose_specification",
    "third_party_sharing_disclosure",
    "parental_consent_mechanism",
    "coppa_ferpa_compliance_mention",
    "data_retention_policy",
    "user_data_rights",
    "data_security_encryption",
    "tracking_technologies_disclosure",
]


def strip_html(html: str) -> str:
    """Strip HTML tags and decode common entities for raw text extraction."""
    text = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"&#\d+;", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


@app.post("/api/analyze")
async def analyze(req: AnalyzeRequest):
    policy_text = req.policy_text

    if not policy_text and req.policy_url:
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
                resp = await client.get(req.policy_url)
                resp.raise_for_status()
                policy_text = strip_html(resp.text)
        except httpx.HTTPError as e:
            raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {e}")

    if not policy_text or len(policy_text.strip()) < 100:
        raise HTTPException(status_code=400, detail="Policy text is too short or empty. Paste the full policy text for best results.")

    analyzer = get_analyzer()
    result = analyzer.analyze_policy(policy_text, app_id="web_user")

    if result is None:
        raise HTTPException(status_code=500, detail="Analysis failed. Please try again.")

    # Compute compliance score and risk level
    compliance_score = sum(1 for k in INDICATOR_KEYS if result.get(k, False))
    if compliance_score >= 7:
        risk_level = "Low"
    elif compliance_score >= 4:
        risk_level = "Medium"
    else:
        risk_level = "High"

    return {
        **result,
        "compliance_score": compliance_score,
        "risk_level": risk_level,
    }
