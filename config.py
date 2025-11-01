import os

SNAP_PUBLIC_BASE = os.getenv("SNAP_PUBLIC_BASE", "https://businessapi.snapchat.com/v1/public_profiles")

SNAP_CLIENT_ID = os.getenv("SNAP_CLIENT_ID", "")
SNAP_CLIENT_SECRET = os.getenv("SNAP_CLIENT_SECRET", "")

MAX_ITEMS = int(os.getenv("MAX_ITEMS", "50"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
