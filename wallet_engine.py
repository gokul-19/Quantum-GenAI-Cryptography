# wallet_engine.py
import os, json
from datetime import datetime

WALLET_DIR = "wallet_data"
os.makedirs(WALLET_DIR, exist_ok=True)

def _path(name):
    return os.path.join(WALLET_DIR, f"{name.replace(' ','_')}.json")

def create_identity(name, key_hex, meta=None):
    meta = meta or {}
    entry = {"name": name, "key_hex": key_hex, "meta": meta, "created_at": datetime.utcnow().isoformat()+'Z'}
    with open(_path(name), "w") as f:
        json.dump(entry, f, indent=2)
    return entry

def load_identity(name):
    p = _path(name)
    if not os.path.exists(p):
        raise FileNotFoundError("identity not found")
    with open(p, "r") as f:
        return json.load(f)

def list_identities():
    out=[]
    for f in os.listdir(WALLET_DIR):
        if f.endswith(".json"):
            with open(os.path.join(WALLET_DIR,f)) as fh:
                out.append(json.load(fh))
    return out

def delete_identity(name):
    p = _path(name)
    if os.path.exists(p):
        os.remove(p)
        return True
    return False
