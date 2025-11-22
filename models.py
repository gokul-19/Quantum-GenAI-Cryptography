# models.py
import torch
import torch.nn as nn

def rotation_matrix(theta):
    """Simple 2x2 rotation-like transform (tensor-based)."""
    return torch.tensor([[torch.cos(theta), -torch.sin(theta)],
                         [torch.sin(theta),  torch.cos(theta)]], dtype=torch.float32)

def entangle(v1, v2):
    """Simulate a simple mixing/entanglement."""
    return (v1 + v2) / 2.0

class GeneratorQuantumCircuit(nn.Module):
    def __init__(self, n_qubits=4, n_layers=2, latent_dim=16):
        super().__init__()
        self.n_qubits = n_qubits
        self.n_layers = n_layers
        self.latent_dim = latent_dim
        # Small MLP to map latent -> per-qubit rotation angles
        self.net = nn.Sequential(
            nn.Linear(latent_dim, 64),
            nn.ReLU(),
            nn.Linear(64, n_qubits)
        )

    def forward(self, latent):
        """
        latent: (batch, latent_dim)
        returns: (batch, n_qubits) float tensor values in [-1,1] representing "measurements"
        """
        batch = latent.shape[0]
        angles = self.net(latent)  # (batch, n_qubits)
        out = torch.tanh(angles)
        return out  # use this as raw quantum-like observables

class DiscriminatorQuantumCircuit(nn.Module):
    def __init__(self, n_qubits=4, n_layers=2):
        super().__init__()
        self.n_qubits = n_qubits
        self.n_layers = n_layers
        # small mixer + final logit
        self.mlp = nn.Sequential(
            nn.Linear(n_qubits, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        """
        x: (batch, n_qubits)
        returns: (batch, 1) probability-like output
        """
        return self.mlp(x)
