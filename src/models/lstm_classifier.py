"""LSTM classifier for time-series failure detection."""

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset


class LSTMClassifier(nn.Module):
    def __init__(self, input_size: int, hidden_size: int = 64, num_layers: int = 2,
                 num_classes: int = 2, dropout: float = 0.3):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers,
                            batch_first=True, dropout=dropout if num_layers > 1 else 0.0)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        # x: (batch, seq_len, input_size)
        out, _ = self.lstm(x)
        out = self.dropout(out[:, -1, :])   # last timestep
        return self.fc(out)


class LSTMTrainer:
    """Wraps LSTMClassifier with sklearn-style fit/predict interface."""

    def __init__(self, input_size: int, hidden_size: int = 64, num_layers: int = 2,
                 num_classes: int = 2, dropout: float = 0.3,
                 lr: float = 1e-3, epochs: int = 30, batch_size: int = 256,
                 class_weights=None):
        self.device = torch.device("cpu")
        self.epochs = epochs
        self.batch_size = batch_size
        self.num_classes = num_classes
        self.model = LSTMClassifier(input_size, hidden_size, num_layers,
                                    num_classes, dropout).to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        weight = class_weights.to(self.device) if class_weights is not None else None
        self.criterion = nn.CrossEntropyLoss(weight=weight)

    def fit(self, X: np.ndarray, y: np.ndarray) -> "LSTMTrainer":
        """Train on X (n, seq, features) and y (n,)."""
        X_t = torch.tensor(X, dtype=torch.float32)
        y_t = torch.tensor(y, dtype=torch.long)
        loader = DataLoader(TensorDataset(X_t, y_t), batch_size=self.batch_size, shuffle=True)

        self.model.train()
        for epoch in range(self.epochs):
            total_loss = 0.0
            for xb, yb in loader:
                self.optimizer.zero_grad()
                loss = self.criterion(self.model(xb), yb)
                loss.backward()
                self.optimizer.step()
                total_loss += loss.item()
            if (epoch + 1) % 5 == 0:
                print(f"  Epoch {epoch+1}/{self.epochs}  loss={total_loss/len(loader):.4f}")
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        self.model.eval()
        with torch.no_grad():
            logits = self.model(torch.tensor(X, dtype=torch.float32))
            return logits.argmax(dim=1).numpy()

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        self.model.eval()
        with torch.no_grad():
            logits = self.model(torch.tensor(X, dtype=torch.float32))
            return torch.softmax(logits, dim=1).numpy()

    def predict_flat(self, X_flat: np.ndarray, window: int, n_features: int) -> np.ndarray:
        """Accept flattened input (n, window*features) for KernelSHAP compatibility."""
        X_3d = X_flat.reshape(-1, window, n_features)
        return self.predict_proba(X_3d)
