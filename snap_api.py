import requests
from typing import Optional, Dict, Any
from config import SNAP_PUBLIC_BASE, REQUEST_TIMEOUT

class SnapPublicAPI:
    """
    Minimal wrapper for Snapchat Public Profile API endpoints used by SnapMapr.
    Uses only public endpoints (no creator authentication) where possible.
    Docs: Public Profile API - Snap for Developers.
    """
    def __init__(self, base: str = SNAP_PUBLIC_BASE, timeout: int = REQUEST_TIMEOUT):
        self.base = base.rstrip("/")
        self.timeout = timeout

    def get_profile(self, profile_id: str) -> Dict[str, Any]:
        """
        GET /public_profiles/{profile_id}
        profile_id can be the numeric id or the @username form depending on endpoint.
        """
        url = f"{self.base}/{profile_id}"
        resp = requests.get(url, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def get_profile_stats(self, profile_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        GET /public_profiles/{profile_id}/stats
        Returns dict of metrics (views, engagement, etc) if available.
        """
        url = f"{self.base}/{profile_id}/stats"
        resp = requests.get(url, params=params or {}, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def search_profile_by_username(self, username: str) -> Dict[str, Any]:
        """
        Uses the public search endpoint if supported. (Docs mention search exists)
        If not available for your account, this will return 404.
        """
        url = f"{self.base}/search"
        params = {"q": username}
        resp = requests.get(url, params=params, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()
