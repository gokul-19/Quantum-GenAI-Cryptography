# visualizations.py
import plotly.figure_factory as ff
import plotly.graph_objects as go
import numpy as np
import random

# --------------------------------------------------------
# 1. QKD Timeline
# --------------------------------------------------------

def qkd_timeline():
    df = [
        dict(Task="Alice chooses bits", Start='2025-01-01', Finish='2025-01-02'),
        dict(Task="Alice chooses bases", Start='2025-01-02', Finish='2025-01-03'),
        dict(Task="Quantum transmission", Start='2025-01-03', Finish='2025-01-04'),
        dict(Task="Bob measures", Start='2025-01-04', Finish='2025-01-05'),
        dict(Task="Basis reconciliation", Start='2025-01-05', Finish='2025-01-06'),
        dict(Task="Key extraction", Start='2025-01-06', Finish='2025-01-07')
    ]
    
    fig = ff.create_gantt(df, index_col='Task', title="QKD Process Timeline", show_colorbar=True)
    return fig
# --------------------------------------------------------
# 2. Rotating Qubit Animation
# --------------------------------------------------------

def rotating_qubit_animation():
    frames = []
    steps = 60

    for t in range(steps):
        theta = np.pi/2
        phi = 2*np.pi * (t/steps)

        x = np.sin(theta) * np.cos(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(theta)

        frames.append(go.Frame(data=[
            go.Scatter3d(
                x=[0, x], y=[0, y], z=[0, z],
                mode="lines+markers",
                marker=dict(size=6)
            )
        ]))

    fig = go.Figure(
        frames=frames,
        data=[go.Scatter3d(x=[0, 0], y=[0, 0], z=[0, 1])]
    )

    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-1, 1]),
            yaxis=dict(range=[-1, 1]),
            zaxis=dict(range=[-1, 1])
        ),
        updatemenus=[{
            "type": "buttons",
            "buttons": [{
                "label": "Play",
                "method": "animate",
                "args": [None]
            }]
        }]
    )
    return fig

# --------------------------------------------------------
# 2. Rotating Qubit Animation
# --------------------------------------------------------

def rotating_qubit_animation():
    frames = []
    steps = 60

    for t in range(steps):
        theta = np.pi/2
        phi = 2*np.pi * (t/steps)

        x = np.sin(theta) * np.cos(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(theta)

        frames.append(go.Frame(data=[
            go.Scatter3d(
                x=[0, x], y=[0, y], z=[0, z],
                mode="lines+markers",
                marker=dict(size=6)
            )
        ]))

    fig = go.Figure(
        frames=frames,
        data=[go.Scatter3d(x=[0, 0], y=[0, 0], z=[0, 1])]
    )

    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-1, 1]),
            yaxis=dict(range=[-1, 1]),
            zaxis=dict(range=[-1, 1])
        ),
        updatemenus=[{
            "type": "buttons",
            "buttons": [{
                "label": "Play",
                "method": "animate",
                "args": [None]
            }]
        }]
    )
    return fig

# --------------------------------------------------------
# 3. QGAN Latent Explorer
# --------------------------------------------------------

def qgan_latent_explorer(generator):
    import torch

    z = torch.randn(1, 16)
    with torch.no_grad():
        out = generator(z).cpu().numpy().flatten()

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=out, mode='lines+markers'))
    fig.update_layout(title="QGAN Latent Vector Output")
    return fig

# --------------------------------------------------------
# 4. Encryption Pipeline Diagram
# --------------------------------------------------------

def encryption_pipeline():
    fig = go.Figure()

    labels = [
        "Message →", "Quantum RotMix →", "Quantum Noise →",
        "AES-CFB Encrypt →", "Ciphertext"
    ]

    x = [0, 1, 2, 3, 4]

    fig.add_trace(go.Scatter(
        x=x, y=[0]*5, mode='markers+text',
        text=labels, textposition="top center", marker=dict(size=20)
    ))

    for i in range(4):
        fig.add_annotation(
            x=x[i] + 0.5, y=0, text="→", showarrow=False, font=dict(size=30)
        )

    fig.update_layout(title="Encryption Pipeline", xaxis=dict(visible=False), yaxis=dict(visible=False))
    return fig

# --------------------------------------------------------
# 5. Quantum State Cloud
# --------------------------------------------------------

def quantum_state_cloud(N=200):
    xs, ys, zs = [], [], []
    for _ in range(N):
        theta = np.random.uniform(0, np.pi)
        phi = np.random.uniform(0, 2*np.pi)
        xs.append(np.sin(theta)*np.cos(phi))
        ys.append(np.sin(theta)*np.sin(phi))
        zs.append(np.cos(theta))

    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=xs, y=ys, z=zs, mode='markers',
        marker=dict(size=4, opacity=0.7)
    ))
    fig.update_layout(title="Quantum State Cloud (Random Pure States)")
    return fig

# --------------------------------------------------------
# 6. Entropy Heatmap
# --------------------------------------------------------

def entropy_heatmap():
    H = np.zeros((20, 20))
    for i in range(20):
        for j in range(20):
            p = (i + 1) / 21
            q = (j + 1) / 21
            H[i][j] = -(p*np.log2(p) + q*np.log2(q))

    fig = go.Figure(data=go.Heatmap(z=H))
    fig.update_layout(title="Entropy Heatmap")
    return fig
