from __future__ import annotations

import json
from pathlib import Path
from openai import OpenAI

from app.core.config import KB_DIR, OPENAI_API_KEY, OPENAI_MODEL


def _select_playbook(risk_class: str) -> Path:
    if risk_class == "High":
        return KB_DIR / "1_critical_risks_playbook.md"
    if risk_class == "Medium":
        return KB_DIR / "2_medium_risks_playbook.md"
    return KB_DIR / "3_preventive_actions.md"


def _simple_retrieve(playbook_text: str, dominant_feature: str, max_lines: int = 80) -> str:
    keywords_map = {
        "MCDM_Score": ["audit", "pilotage", "plan", "revue", "indicateur"],
        "Incidents_Count": ["incident", "qualité", "capa", "non-conform", "réclamation"],
        "Financial_Stability_Score": ["financ", "solvabilité", "paiement", "trésorerie", "dépendance"],
        "Delivery_Performance_Score": ["délai", "livraison", "otd", "retard", "lead time"],
        "Quality_Compliance_Score": ["qualité", "contrôle", "ppm", "inspection", "défaut"],
        "Regulatory_Adherence_Score": ["réglement", "conformité", "certificat", "audit"],
        "Sustainability_Score": ["durable", "esg", "carbone", "scope", "émission"],
    }

    keywords = keywords_map.get(dominant_feature, [])
    lines = []
    if keywords:
        for line in playbook_text.splitlines():
            if any(k.lower() in line.lower() for k in keywords):
                lines.append(line)
            if len(lines) >= max_lines:
                break

    if not lines:
        lines = playbook_text.splitlines()[:max_lines]

    return "\n".join(lines)


def generate_actions_with_rag(shap_json: dict) -> dict:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not set in environment")

    client = OpenAI(api_key=OPENAI_API_KEY)

    risk_class = shap_json.get("risk_class") or shap_json.get("predicted_risk_class", "Non-High")
    playbook_path = _select_playbook(risk_class)
    playbook_text = playbook_path.read_text(encoding="utf-8")

    dominant_feature = shap_json["top_factors"][0]["feature"] if shap_json.get("top_factors") else "MCDM_Score"
    rag_context = _simple_retrieve(playbook_text, dominant_feature)

    # IMPORTANT: on force un JSON strict, sans markdown
    prompt = f"""
Tu es un expert en Supplier Risk Management (SRM).
Tu dois produire une sortie ACTIONNABLE et AUDITABLE.

Règles strictes:
- Réponds UNIQUEMENT en JSON valide (UTF-8), sans texte autour.
- N'invente rien: utilise uniquement les données fournies (features + valeurs + SHAP + probabilité).
- Chaque action DOIT être liée à une feature cible (target_feature) parmi:
  {FEATURES if 'FEATURES' in globals() else 'Financial_Stability_Score,Delivery_Performance_Score,Quality_Compliance_Score,Regulatory_Adherence_Score,Sustainability_Score,Past_Risk_Level,ERP_Transactions,Incidents_Count,MCDM_Score'}
- Chaque action DOIT contenir: 
  action, owner, type, why, target_feature, kpi, success_threshold, trigger_condition, deliverable, frequency, deadline_days
- "type" ∈ ["immédiate","court_terme","moyen_terme","annuel"]
- "deadline_days" doit être un entier cohérent avec type:
  immédiate <= 30 ; court_terme <= 90 ; moyen_terme <= 180 ; annuel >= 300
- Le champ "why" doit citer la valeur de la feature ET son sens SHAP (increase/decrease) + contribution_percent.
- Génère 6 à 10 actions (pas moins).

Entrée (prédiction + SHAP):
{json.dumps(shap_json, ensure_ascii=False, indent=2)}

Contexte interne (extraits playbook):
{rag_context}

Sortie attendue EXACTE (structure):
{{
  "risk_summary": {{
    "risk_class": "...",
    "risk_probability": 0.0,
    "explanation": "4-6 phrases max. Cite les 2-3 drivers principaux (feature + valeur + contribution).",
    "key_drivers": [
      {{
        "feature": "...",
        "value": 0.0,
        "impact_direction": "increase_risk|decrease_risk",
        "contribution_percent": 0.0,
        "why_it_matters": "1 phrase"
      }}
    ]
  }},
  "actions": [
    {{
      "action": "...",
      "owner": "Achats|Qualité|Finance|Supply|Juridique|RSE|ERP",
      "type": "immédiate|court_terme|moyen_terme|annuel",
      "why": "Doit citer feature+valeur+shap+contribution",
      "target_feature": "...",
      "kpi": "...",
      "success_threshold": "...",
      "trigger_condition": "...",
      "deliverable": "...",
      "frequency": "hebdo|mensuel|trimestriel|annuel",
      "deadline_days": 0
    }}
  ]
}}
"""



    resp = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    content = resp.choices[0].message.content.strip()

    # Si jamais le modèle met du texte autour, on essaie d'extraire un JSON
    start = content.find("{")
    end = content.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"LLM did not return JSON. Output was: {content[:200]}")

    content_json = content[start : end + 1]
    return json.loads(content_json)
