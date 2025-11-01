import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
from image_classifier import ImageThemeClassifier
from geo_processor import extract_latlon, infer_region_from_profile

st.set_page_config(page_title="SnapMapr", layout="wide")

def run_dashboard(df: pd.DataFrame):
    st.title("SnapMapr — Public Snapchat Profile Explorer")

    # left: controls
    with st.sidebar:
        st.header("Controls")
        profile_id = st.text_input("Profile ID or username (@name)", value="")
        max_items = st.slider("Max items to fetch", min_value=1, max_value=200, value=50)
        refresh = st.button("Refresh / Fetch")
        st.markdown("---")
        st.write("Filter by theme")
        themes = st.multiselect("Themes", options=sorted(df.get("theme", pd.Series()).unique().tolist()), default=None)

    # top metrics
    st.markdown("### Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Assets", int(len(df)))
    col2.metric("Profiles", df["profile_id"].nunique() if "profile_id" in df.columns else 1)
    if "sentiment" in df.columns:
        col3.metric("Avg sentiment", f"{df['sentiment'].mean():.2f}")

    # map
    st.markdown("### Map")
    map_df = df.dropna(subset=["lat", "lon"])
    if map_df.empty:
        st.info("No geolocated items to show on the map.")
    else:
        start_lat = float(map_df["lat"].mean())
        start_lon = float(map_df["lon"].mean())
        m = folium.Map(location=[start_lat, start_lon], zoom_start=2)
        for _, r in map_df.iterrows():
            popup = folium.Popup(f"<b>{r.get('asset_id')}</b><br/>theme: {r.get('theme')}<br/>{r.get('caption') or ''}", max_width=300)
            folium.CircleMarker(location=[r["lat"], r["lon"]], radius=6, popup=popup).add_to(m)
        st_folium(m, width=800, height=450)

    # charts
    st.markdown("### Theme distribution")
    if "theme" in df.columns:
        fig = px.histogram(df, x="theme", title="Themes")
        st.plotly_chart(fig, use_container_width=True)

    # table + export
    st.markdown("### Assets table")
    st.dataframe(df[["profile_id", "asset_id", "theme", "sentiment", "media_url", "created_time"]])

    csv = df.to_csv(index=False)
    st.download_button("Download CSV", csv, file_name="snapmapr_export.csv", mime="text/csv")
