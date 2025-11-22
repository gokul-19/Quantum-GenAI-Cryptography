# app.py
import streamlit as st
import torch
import streamlit.components.v1 as components
from qgan_engine import load_generator, qgan_key_from_generator
from crypto_engine import hybrid_encrypt, hybrid_decrypt, generator_key_to_aes_bytes
from multiuser_exchange import simulate_bb84
from wallet_engine import create_identity, list_identities, load_identity
from bloch_plotly import bloch_sphere
import plotly.io as pio

st.set_page_config(page_title="Quantum-Inspired GenAI Cryptography", layout="wide", page_icon="🔐")
st.markdown("<style>body {background-color: #05050a; color: #ddd}</style>", unsafe_allow_html=True)

# Top banner
st.markdown("""
<h1 style='text-align:center;color:#0af;'>🔐 Quantum-Inspired GenAI Cryptography</h1>
<p style='text-align:center;color:#aaa;'>Hybrid classical–quantum demo: QGAN keygen, QKD-style exchange, AES-CFB encrypt/decrypt</p>
<hr style='border:1px solid #222;'/>
""", unsafe_allow_html=True)

# Left control panel
with st.sidebar:
    st.header("Controls")
    checkpoint = st.text_input("Generator checkpoint path (optional)", value="models/generator.pth")
    startup_load = st.radio("Load model at start?", ("Yes", "No"), index=1)
    st.markdown("---")
    st.markdown("Logs path (for debugging):")
    st.code("/mnt/data/logs-gokul-19-quantum-genai-cryptography-main-qgan-train.py-2025-11-22T13_21_28.369Z.txt")

# Load generator if requested
generator = None
if startup_load == "Yes":
    generator = load_generator(checkpoint)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "QGAN KeyGen", 
    "QKD Exchange", 
    "Encrypt / Decrypt", 
    "Wallet", 
    "Visualizations"
])


# ---------------- Tab 1: QGAN KeyGen ----------------
with tab1:
    st.subheader("QGAN-based Key Generation")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate Key (QGAN)"):
            if generator is None:
                generator = load_generator(checkpoint)
            key_bytes = qgan_key_from_generator(generator)
            st.success("Generated key (hex):")
            st.code(key_bytes.hex())
            st.session_state["last_key_hex"] = key_bytes.hex()
    with col2:
        if st.button("Generate Fallback Key (random)"):
            k = torch.rand(32).mul(255).to(torch.uint8).cpu().numpy().tobytes()
            st.code(k.hex())
            st.session_state["last_key_hex"] = k.hex()
    st.markdown("Use this key to create wallet identity or encrypt messages.")

# ---------------- Tab 2: QKD Exchange ----------------
with tab2:
    st.subheader("Simulate QKD (BB84-style)")
    length = st.slider("Number of qubits/bits", 64, 512, 128)
    noise = st.slider("Noise rate", 0.0, 0.2, 0.02, step=0.01)
    if st.button("Simulate QKD Exchange"):
        res = simulate_bb84(length=length, noise_rate=noise)
        st.success("Simulated exchange complete.")
        st.code(res["shared_key_hex"])
        st.session_state["last_key_hex"] = res["shared_key_hex"]

# ---------------- Tab 3: Encrypt / Decrypt ----------------
with tab3:
    st.subheader("Hybrid Encrypt / Decrypt")
    message = st.text_area("Message to encrypt")
    key_input = st.text_input("Key hex (leave empty to use last generated key)")
    signature_box = st.text_area("Signature (for decrypt use)")
    if st.button("Encrypt Message"):
        key_hex = key_input.strip() or st.session_state.get("last_key_hex")
        if not key_hex:
            st.error("No key present. Generate or paste a key hex.")
        else:
            # build fake generator handle to satisfy api (we'll pass None and use explicit key)
            # crypto_engine.hybrid_encrypt expects a generator or will fallback - to use explicit key, we hack by decrypt below
            from crypto_engine import aes_cfb_encrypt, pq_hash_sign
            key_bytes = bytes.fromhex(key_hex)
            # Preprocess + aes encrypt: call functions directly
            from crypto_engine import quantum_rotmix, quantum_noise
            q1 = quantum_rotmix(message.encode(), key_bytes)
            q2 = quantum_noise(q1)
            cipher = aes_cfb_encrypt(key_bytes, q2)
            signature = pq_hash_sign(cipher.encode(), key_bytes)
            st.success("Encrypted")
            st.code(cipher)
            st.write("Signature:")
            st.code(signature)
            st.session_state["last_cipher"] = cipher
            st.session_state["last_signature"] = signature
    if st.button("Decrypt Message"):
        key_hex = key_input.strip() or st.session_state.get("last_key_hex")
        cipher = st.session_state.get("last_cipher") or ""
        signature = signature_box.strip() or st.session_state.get("last_signature")
        if not (key_hex and cipher and signature):
            st.error("Need key, cipher, and signature to decrypt")
        else:
            try:
                from crypto_engine import aes_cfb_decrypt, quantum_noise_reverse, quantum_rotmix, pq_hash_verify
                key_bytes = bytes.fromhex(key_hex)
                if not pq_hash_verify(cipher.encode(), key_bytes, signature):
                    st.error("Signature verification failed")
                else:
                    raw = aes_cfb_decrypt(key_bytes, cipher)
                    rev_noise = quantum_noise_reverse(raw)
                    final = quantum_rotmix(rev_noise, key_bytes)
                    st.success("Decrypted message:")
                    st.code(final.decode(errors="ignore"))
            except Exception as e:
                st.error(f"Decryption failed: {e}")

# ---------------- Tab 4: Wallet ----------------
with tab4:
    st.subheader("Wallet")
    name = st.text_input("Identity name")
    key_hex = st.text_input("Key hex for identity")
    if st.button("Create Identity"):
        if not (name and key_hex):
            st.error("Provide both name and key_hex")
        else:
            create_identity(name, key_hex)
            st.success("Identity saved")
    if st.button("List identities"):
        ids = list_identities()
        st.json(ids)
    load_name = st.text_input("Load identity by name")
    if st.button("Load identity"):
        try:
            entry = load_identity(load_name)
            st.json(entry)
            st.session_state["last_key_hex"] = entry["key_hex"]
        except Exception as e:
            st.error(str(e))

# ---------------- Tab 5: Visualizations ----------------
with tab5:
    st.header("Quantum Visualizations")

    from visualizations import (
        rotating_qubit_animation, qgan_latent_explorer,
        encryption_pipeline, quantum_state_cloud, entropy_heatmap
    )

    if st.button("Show Rotating Qubit Animation"):
        st.plotly_chart(rotating_qubit_animation(), use_container_width=True)

    if st.button("Show QGAN Latent Explorer"):
        if generator is None:
            st.error("Load generator first!")
        else:
            st.plotly_chart(qgan_latent_explorer(generator), use_container_width=True)

    if st.button("Show Encryption Pipeline Diagram"):
        st.plotly_chart(encryption_pipeline(), use_container_width=True)

    if st.button("Show Quantum State Cloud"):
        st.plotly_chart(quantum_state_cloud(), use_container_width=True)

    if st.button("Show Entropy Heatmap"):
        st.plotly_chart(entropy_heatmap(), use_container_width=True)

    
