import argparse
import pandas as pd
from snap_api import SnapPublicAPI
from fetcher import SnapFetcher
from image_classifier import ImageThemeClassifier
from geo_processor import extract_latlon, infer_region_from_profile
from dashboard_app import run_dashboard

def annotate(df: pd.DataFrame):
    clf = ImageThemeClassifier()
    themes = []
    lats = []
    lons = []
    for _, row in df.iterrows():
        url = row.get("media_url")
        theme = clf.infer_theme(url)
        themes.append(theme)
        lat, lon = extract_latlon(row.get("location"))
        lats.append(lat)
        lons.append(lon)
    df["theme"] = themes
    df["lat"] = lats
    df["lon"] = lons
    return df

def run(profile_id: str):
    api = SnapPublicAPI()
    fetcher = SnapFetcher(api)
    df = fetcher.fetch_profile_items(profile_id)
    df = annotate(df)
    run_dashboard(df)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", help="Profile id or username to fetch (public)")
    args = parser.parse_args()
    run(args.profile)
