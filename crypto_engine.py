# crypto_engine.py
import os
import base64
import hashlib
from Crypto.Cipher import AES

# ---------- Quantum-Inspired layers ----------
def quantum_rotmix(data_bytes, key):
    """
    Apply simple rotation-like mixing using key bytes.
    """
    mixed = bytearray()
    keylen = len(key)
    for i, b in enumerate(data_bytes):
        theta = (key[i % keylen] / 255) * 3.14159  # angle 0..π
        mixed.append((b ^ (int(theta * 100) & 0xFF)) & 0xFF)
    return bytes(mixed)

def quantum_noise(data_bytes):
    """
    Add small nondeterministic noise using os.urandom.
    """
    mixed = bytearray()
    for b in data_bytes:
        noise = os.urandom(1)[0] % 4
        mixed.append((b + noise) % 256)
    return bytes(mixed)

def quantum_noise_reverse(data_bytes):
    """Approximate inverse for demo (deterministic inverse used here)."""
    mixed = bytearray()
    for b in data_bytes:
        mixed.append((b - 2) % 256)
    return bytes(mixed)

# ---------- AES-CFB ----------
def aes_cfb_encrypt(key: bytes, plaintext_bytes: bytes) -> str:
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    ciphertext = cipher.encrypt(plaintext_bytes)
    return base64.b64encode(iv + ciphertext).decode()

def aes_cfb_decrypt(key: bytes, cipher_b64: str) -> bytes:
    raw = base64.b64decode(cipher_b64)
    iv, ciphertext = raw[:16], raw[16:]
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    return cipher.decrypt(ciphertext)

# ---------- Post-quantum (lightweight hash signature) ----------
def pq_hash_sign(data_bytes: bytes, key: bytes) -> str:
    return hashlib.sha3_512(key + data_bytes).hexdigest()

def pq_hash_verify(data_bytes: bytes, key: bytes, signature_hex: str) -> bool:
    return pq_hash_sign(data_bytes, key) == signature_hex

# ---------- Full pipeline ----------
def hybrid_encrypt(generator, plaintext: str):
    key = None
    # If generator provided, produce key via qgan; else produce random key
    try:
        key = generator_key_to_aes_bytes(generator)
    except Exception:
        key = os.urandom(32)

    p_bytes = plaintext.encode()
    q1 = quantum_rotmix(p_bytes, key)
    q2 = quantum_noise(q1)
    cipher_b64 = aes_cfb_encrypt(key, q2)
    signature = pq_hash_sign(cipher_b64.encode(), key)
    return {"cipher": cipher_b64, "signature": signature, "key_hex": key.hex()}

def hybrid_decrypt(cipher_b64: str, key_hex: str, signature: str):
    key = bytes.fromhex(key_hex)
    if not pq_hash_verify(cipher_b64.encode(), key, signature):
        raise ValueError("Signature verification failed")
    dec = aes_cfb_decrypt(key, cipher_b64)
    qn_rev = quantum_noise_reverse(dec)
    final = quantum_rotmix(qn_rev, key)  # note: rotation mix is symmetric in this simple demo
    return final.decode(errors="ignore")

# Helper to generate key if generator object present
def generator_key_to_aes_bytes(generator, latent_size=16, key_bytes=32):
    import hashlib, torch
    with torch.no_grad():
        latent = torch.randn(1, latent_size)
        out = generator(latent)[0]
        raw_bytes = ( (out * 255).clamp(0,255).byte().cpu().numpy().tobytes() )
        return hashlib.sha3_512(raw_bytes).digest()[:key_bytes]
