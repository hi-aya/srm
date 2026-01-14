from fastapi import APIRouter, HTTPException, Query
import traceback

from app.schemas.risk import RiskRequest
from app.services.risk_model import risk_model_service

router = APIRouter(prefix="/risk", tags=["risk"])


@router.post("/analyze")
def analyze(
    payload: RiskRequest,
    with_llm: bool = Query(False),
):
    """
    Analyse le risque fournisseur à partir des métriques fournies.
    Le supplier_uuid est attendu DANS le payload (pas en query).
    """
    try:
        # Convertit le payload Pydantic en dict
        data = payload.model_dump()

        # Appel du service ML + SHAP + RAG
        return risk_model_service.predict_and_store(
            payload=data,
            with_llm=with_llm,
        )

    except Exception as e:
        print("❌ ERROR /risk/analyze:", repr(e))
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
