import os
import json
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
BASE = "https://apitransporte.buenosaires.gob.ar/ecobici/gbfs"

# Carpeta donde van a caer los snapshots crudos
RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

resp = requests.get(
    f"{BASE}/stationStatus",
    params={"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET},
    timeout=30,
)
resp.raise_for_status()
data = resp.json()

# Momento exacto de la captura (en UTC), apto para nombre de archivo
captured_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
out_path = RAW_DIR / f"stationStatus_{captured_at}.json"

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

estaciones = data["data"]["stations"]
print(f"Guardado {out_path} — {len(estaciones)} estaciones")