# bloch_plotly.py
import plotly.graph_objects as go
import numpy as np

def bloch_sphere(state_vector=None):
    u = np.linspace(0, 2*np.pi, 60)
    v = np.linspace(0, np.pi, 30)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    fig = go.Figure(data=[go.Surface(x=x,y=y,z=z,opacity=0.15,showscale=False)])
    # axes
    axes = [
        go.Scatter3d(x=[1.2,-1.2], y=[0,0], z=[0,0], mode='lines', line=dict(color='black', width=2)),
        go.Scatter3d(x=[0,0], y=[1.2,-1.2], z=[0,0], mode='lines', line=dict(color='black', width=2)),
        go.Scatter3d(x=[0,0], y=[0,0], z=[1.2,-1.2], mode='lines', line=dict(color='black', width=2))
    ]
    for a in axes:
        fig.add_trace(a)
    if state_vector is not None:
        alpha, beta = state_vector  # complex numbers allowed
        rho00 = np.abs(alpha)**2
        rho01 = alpha * np.conj(beta)
        rx = 2*np.real(rho01)
        ry = 2*np.imag(rho01)
        rz = rho00 - np.abs(beta)**2
        fig.add_trace(go.Scatter3d(x=[0,rx], y=[0,ry], z=[0,rz],
                                   mode='lines+markers', line=dict(color='red', width=6),
                                   marker=dict(size=4,color='red')))
    fig.update_layout(scene=dict(xaxis=dict(visible=False),yaxis=dict(visible=False),zaxis=dict(visible=False)),
                      margin=dict(l=0,r=0,t=0,b=0))
    return fig
