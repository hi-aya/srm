from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

# Racine projet: .../srm-api
BASE_DIR = Path(__file__).resolve().parents[2]

# Charger .env UNE SEULE FOIS
load_dotenv(BASE_DIR / ".env")

# Paths
MODEL_PATH = BASE_DIR / "models" / "risk_classifier.joblib"
KB_DIR = BASE_DIR / "knowledge_base"

# Features attendues par le modèle (ordre strict)
FEATURES = [
    "Financial_Stability_Score",
    "Delivery_Performance_Score",
    "Quality_Compliance_Score",
    "Regulatory_Adherence_Score",
    "Sustainability_Score",
    "Past_Risk_Level",
    "ERP_Transactions",
    "Incidents_Count",
    "MCDM_Score",
]

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")