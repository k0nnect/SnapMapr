from snap_api import SnapPublicAPI
from typing import List, Dict, Any
import pandas as pd
from config import MAX_ITEMS
from tqdm import tqdm

class SnapFetcher:
    def __init__(self, api: SnapPublicAPI):
        self.api = api

    def fetch_profile_items(self, profile_id: str, max_items: int = MAX_ITEMS) -> pd.DataFrame:
        """
        Fetch profile metadata and attempt to extract recent public assets (stories/spotlight).
        Returns a DataFrame with columns: id, media_url, caption, created_time, location(if any), raw
        """
        profile = self.api.get_profile(profile_id)
        items = []

        content_candidates = []
        if isinstance(profile, dict):
            for key in ("saved_stories", "savedStories", "spotlights", "spotlight", "assets", "content"):
                if key in profile:
                    content_candidates.append(profile[key])

        if not content_candidates and profile.get("data"):
            for key in ("saved_stories", "spotlights", "assets", "content"):
                if key in profile["data"]:
                    content_candidates.append(profile["data"][key])

        for candidate in content_candidates:
            if isinstance(candidate, list):
                for asset in candidate[:max_items]:
                    items.append(self._asset_to_row(asset, profile_id))
            elif isinstance(candidate, dict):
                if "items" in candidate and isinstance(candidate["items"], list):
                    for asset in candidate["items"][:max_items]:
                        items.append(self._asset_to_row(asset, profile_id))
                else:
                    items.append(self._asset_to_row(candidate, profile_id))

        if not items:
            items.append(self._profile_to_row(profile, profile_id))

        df = pd.DataFrame(items)
        return df

    def _asset_to_row(self, asset: Dict[str, Any], profile_id: str) -> Dict[str, Any]:
        media_url = asset.get("media_url") or asset.get("mediaUrl") or asset.get("video_url") or asset.get("url")
        caption = asset.get("caption") or asset.get("title") or asset.get("description")
        created = asset.get("created_time") or asset.get("createdAt") or asset.get("timestamp")
        location = asset.get("location") or asset.get("geo") or {}
        return {
            "profile_id": profile_id,
            "asset_id": asset.get("id") or asset.get("asset_id"),
            "media_url": media_url,
            "caption": caption,
            "created_time": created,
            "location": location,
            "raw": asset
        }

    def _profile_to_row(self, profile: Dict[str, Any], profile_id: str) -> Dict[str, Any]:
        return {
            "profile_id": profile_id,
            "asset_id": f"profile-{profile_id}",
            "media_url": profile.get("avatar_url") or profile.get("profile_picture"),
            "caption": profile.get("bio") or profile.get("display_name") or "",
            "created_time": profile.get("created_time"),
            "location": profile.get("location") or {},
            "raw": profile
        }
