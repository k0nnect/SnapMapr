from typing import Dict, Any, Tuple, Optional
import pytz
import re

def extract_latlon(location_field) -> Tuple[Optional[float], Optional[float]]:
    """
    Attempt to extract lat/lon from a location field which could be dict or string.
    """
    if not location_field:
        return None, None
    if isinstance(location_field, dict):
        lat = location_field.get("latitude") or location_field.get("lat")
        lon = location_field.get("longitude") or location_field.get("lon") or location_field.get("lng")
        try:
            return float(lat) if lat is not None else None, float(lon) if lon is not None else None
        except Exception:
            return None, None
    if isinstance(location_field, str):
        # look for "lat, lon" pattern
        m = re.search(r"(-?\d+\.\d+)[, ]+\s*(-?\d+\.\d+)", location_field)
        if m:
            return float(m.group(1)), float(m.group(2))
    return None, None

def infer_region_from_profile(raw_profile: Dict[str, Any]) -> str:
    """
    Heuristic: use locale / country / timezone if available.
    """
    country = raw_profile.get("country") or raw_profile.get("locale") or raw_profile.get("region")
    if country:
        return str(country)
    return "unknown"
