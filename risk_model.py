from __future__ import annotations

from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import shap

from app.services.supabase_client import get_supabase
from app.services.llm_rag import generate_actions_with_rag

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "models" / "risk_classifier.joblib"

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

class RiskModelService:
    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

        self.model = joblib.load(MODEL_PATH)
        self.explainer = shap.TreeExplainer(self.model)  # <- laisse raw
        self.sb = get_supabase()

    def _build_X(self, payload: dict) -> pd.DataFrame:
        row = {f: payload[f] for f in FEATURES}
        return pd.DataFrame([row], columns=FEATURES)

    def _top_factors_shap(self, X: pd.DataFrame, class_label=1, top_k: int = 5):
        shap_values = self.explainer.shap_values(X)

        classes = list(getattr(self.model, "classes_", []))
        class_idx = classes.index(class_label) if (classes and class_label in classes) else 0

        if isinstance(shap_values, list):
            sv = shap_values[class_idx][0]
        else:
            sv = np.array(shap_values)
            if sv.ndim == 3:
                sv = sv[0, :, class_idx]
            elif sv.ndim == 2:
                sv = sv[0]
            else:
                raise ValueError(f"Unexpected SHAP shape: {sv.shape}")

        vals = X.iloc[0].to_dict()
        total = float(np.sum(np.abs(sv)) + 1e-9)

        factors = []
        for feat, shap_val in zip(FEATURES, sv):
            shap_val = float(shap_val)
            value = float(vals[feat])
            factors.append({
                "feature": feat,
                "value": value,
                "shap_value": shap_val,
                "impact_direction": "increase_risk" if shap_val > 0 else "decrease_risk",
                "contribution_percent": round(abs(shap_val) / total * 100, 2),
            })

        factors.sort(key=lambda x: x["contribution_percent"], reverse=True)
        return factors[:top_k]

    def predict_and_store(self, payload: dict, supplier_id: int | None = None, year: int | None = None, with_llm: bool = False) -> dict:
        X = self._build_X(payload)

        probas = self.model.predict_proba(X)[0]
        classes = list(self.model.classes_)

        if 1 in classes:
            idx = classes.index(1)
            proba_high = float(probas[idx])
            pred = int(self.model.predict(X)[0])
            risk_class = "High" if pred == 1 else "Non-High"
            risk_probability = round(proba_high, 3)
            top_factors = self._top_factors_shap(X, class_label=1, top_k=5)
        else:
            best = int(np.argmax(probas))
            risk_class = str(classes[best])
            risk_probability = round(float(probas[best]), 3)
            top_factors = self._top_factors_shap(X, class_label=classes[best], top_k=5)

        result = {
            "supplier_id": supplier_id,
            "year": year,
            "risk_class": risk_class,
            "risk_probability": risk_probability,
            "top_factors": top_factors,
        }

        llm_result = None
        if with_llm:
            llm_result = generate_actions_with_rag(result)
            result["llm"] = llm_result

        # Insert Supabase
        if self.sb is not None:
            record = {
                "supplier_id": supplier_id,
                "year": year,
                "payload": payload,
                "prediction": {
                    "risk_class": risk_class,
                    "risk_probability": risk_probability,
                    "top_factors": top_factors,
                },
                "llm_result": llm_result,
            }

            try:
                self.sb.table("risk_explanations").insert(record).execute()
                print("Supabase insert OK")
            except Exception as e:
                print("Supabase insert FAILED:", e)

        return result

risk_model_service = RiskModelService()
