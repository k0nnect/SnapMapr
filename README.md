# 📍 SnapMapr — Snapchat Public Profile Intelligence Dashboard

**SnapMapr** is an interactive, data-driven dashboard built in **Python + Streamlit** that connects to the **Snapchat Business API** to visualize, analyze, and monitor Snapchat Public Profiles in real time.

Unlike basic Snapchat API wrappers on GitHub, SnapMapr focuses on **interactive geospatial insights**, allowing users to map engagement, discover content trends, and visualize post locations directly on a live map — all from a beautiful web dashboard.

---

## 🚀 Features

- 🌍 **Live SnapMap Visualization** — See where posts originate geographically using Folium maps.
- 📊 **Profile Metrics Explorer** — Pull follower counts, engagement data, and story stats.
- 🧭 **Geospatial Analytics** — Identify audience hotspots and regional engagement trends.
- 🔐 **Secure OAuth2 Integration** — Works with your own Snapchat Developer App credentials.
- 🧩 **Modular Architecture** — Separated into clean modules for easy customization and extension.
- 🖥️ **Streamlit UI** — Launches as a local web app with a modern dashboard layout.

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/k0nnect/snapmapr.git
cd snapmapr
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install streamlit folium streamlit-folium requests geopy python-dotenv
```

### 3. Configure your Snapchat Developer App

1. Go to [https://developers.snap.com](https://developers.snap.com)
2. Create a **Business API** app
3. Copy your:
   - `CLIENT_ID`
   - `CLIENT_SECRET`

---

## 🔐 Authentication Setup

Create a `.env` file in your project root:

```env
SNAP_CLIENT_ID=your_client_id_here
SNAP_CLIENT_SECRET=your_client_secret_here
```

When you run the app, SnapMapr will automatically request and use an OAuth2 token.

---

## ▶️ Running the App

Launch with:

```bash
streamlit run main.py
```

Then open your browser to the local URL (usually `http://localhost:8501`).

---

## 🗺️ Example Usage

1. Enter a Snapchat **Public Profile ID** in the dashboard (e.g. a brand or creator).
2. SnapMapr fetches live data using Snapchat’s Business API.
3. Watch the dashboard populate with:
   - Profile info and metrics
   - Map of post locations
   - Analytics summaries

---

## 🧠 Libraries Used

    |-------|------|
| Frontend: Streamlit |
| Mapping: Folium + Streamlit-Folium |
| API: Snapchat Business API |
| Auth: OAuth2 via Snapchat Developer |
| Backend: Python 3.12 |
| Environment: dotenv |

---

## ⚠️ Disclaimer

SnapMapr is an independent, educational project built for API research and visualization.  
It is **not affiliated with, endorsed, or maintained by Snapchat Inc.**

Use only your own credentials and comply with Snapchat’s Developer Terms of Service.

---

## ⭐ Contribute

Want to improve SnapMapr?
1. Fork this repo
2. Create a new branch
3. Commit and push
4. Submit a pull request!

---

### 💫 Give the project a ⭐ if you like it!
