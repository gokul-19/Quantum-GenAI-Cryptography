# qgan_engine.py
import os
import hashlib
import torch
from models import GeneratorQuantumCircuit

DEFAULT_LATENT = 16

def make_fallback_generator():
    """Create a generator with random initialization (useful if no checkpoint available)."""
    return GeneratorQuantumCircuit(latent_dim=DEFAULT_LATENT)

def load_generator(checkpoint_path: str):
    """Try to load a saved generator state dict; fallback if missing."""
    G = make_fallback_generator()
    if checkpoint_path and os.path.exists(checkpoint_path):
        try:
            data = torch.load(checkpoint_path, map_location="cpu")
            if isinstance(data, dict) and "state_dict" in data:
                G.load_state_dict(data["state_dict"])
            else:
                G.load_state_dict(data)
            print(f"[qgan_engine] Loaded generator from {checkpoint_path}")
        except Exception as e:
            print(f"[qgan_engine] Failed to load checkpoint: {e}. Using fallback generator.")
    else:
        print("[qgan_engine] No generator checkpoint found; using random-init generator.")
    G.eval()
    return G

def qgan_key_from_generator(generator: GeneratorQuantumCircuit, latent_size=DEFAULT_LATENT, key_bytes=32):
    """
    Generate AES key bytes (length key_bytes) from the generator by sampling latent vector.
    """
    with torch.no_grad():
        latent = torch.randn(1, latent_size)
        out = generator(latent)[0]  # tensor shape (n_qubits,)
        # Convert to bytes: scale to 0..255 and hash-expand
        raw_bytes = ( (out * 255).clamp(0,255).byte().cpu().numpy().tobytes() )
        key = hashlib.sha3_512(raw_bytes).digest()[:key_bytes]
        return key
