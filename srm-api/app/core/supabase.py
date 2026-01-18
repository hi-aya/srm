from __future__ import annotations

from functools import lru_cache
from supabase import create_client, Client

from app.core.config import SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY


@lru_cache(maxsize=1)
def get_supabase() -> Client | None:
    """
    Retourne un client Supabase singleton (ou None si non configuré).
    """
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        return None
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
