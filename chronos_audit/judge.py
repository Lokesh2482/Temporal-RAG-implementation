import json
import re

def clean_json(text):
    return re.sub(r"```json|```", "", text).strip()

def run_tabula_rasa_judge(judge, claim, character, time_scope, evidence):
    prompt = f"""
    ACT AS A FORENSIC NARRATIVE AUDITOR.

    Claim: "{claim}"
    Character: {character}
    Era: {time_scope}

    Evidence:
    {evidence}

    Rules:
    - Verdict 0 ONLY if explicitly contradicted or physically impossible.
    - Silence is consistent.
    - Dead or incapacitated characters cannot act.

    Output JSON only:
    {{
        "verdict": 0 or 1,
        "rationale": "Brief explanation",
        "dossier": []
    }}
    """
    response = judge.invoke(prompt).content
    return json.loads(clean_json(response))
