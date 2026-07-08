"""Time-series preprocessing: normalisation, windowing, and splitting."""

from typing import Literal, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler


class TimeSeriesPreprocessor:
    """Prepares time-series DataFrames for ML model input."""

    def __init__(self) -> None:
        self._scaler: Optional[MinMaxScaler | StandardScaler] = None

    def handle_missing(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fill missing values: forward fill then backward fill."""
        return df.ffill().bfill()

    def normalise(
        self,
        df: pd.DataFrame,
        method: Literal["minmax", "standard"] = "minmax",
        feature_cols: Optional[list[str]] = None,
    ) -> pd.DataFrame:
        """Fit-transform numeric feature columns.

        Stores the fitted scaler so the same transform can be applied to test data.

        Args:
            df: Input DataFrame.
            method: 'minmax' scales to [0, 1]; 'standard' gives zero mean / unit variance.
            feature_cols: Columns to scale. Defaults to all numeric columns.
        """
        cols = feature_cols or df.select_dtypes(include="number").columns.tolist()
        scaler = MinMaxScaler() if method == "minmax" else StandardScaler()
        df = df.copy()
        df[cols] = scaler.fit_transform(df[cols])
        self._scaler = scaler
        return df

    def transform(self, df: pd.DataFrame, feature_cols: Optional[list[str]] = None) -> pd.DataFrame:
        """Apply the already-fitted scaler to new data (e.g. test set)."""
        if self._scaler is None:
            raise RuntimeError("Call normalise() on training data first.")
        cols = feature_cols or df.select_dtypes(include="number").columns.tolist()
        df = df.copy()
        df[cols] = self._scaler.transform(df[cols])
        return df

    def create_windows(
        self,
        df: pd.DataFrame,
        feature_cols: list[str],
        label_col: str,
        window_size: int = 30,
        step: int = 1,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Slide a fixed-length window over the time series.

        Args:
            df: Time-series DataFrame sorted by time.
            feature_cols: Input feature columns.
            label_col: Column containing the class/regression label.
            window_size: Number of timesteps per window.
            step: Stride between consecutive windows.

        Returns:
            (X, y) where X.shape == (n_windows, window_size, n_features)
            and y.shape == (n_windows,).
        """
        X_list, y_list = [], []
        values = df[feature_cols].values
        labels = df[label_col].values

        for start in range(0, len(df) - window_size + 1, step):
            end = start + window_size
            X_list.append(values[start:end])
            y_list.append(labels[end - 1])

        return np.array(X_list), np.array(y_list)

    def train_test_split(
        self,
        df: pd.DataFrame,
        test_size: float = 0.2,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Temporal split that preserves order (no shuffling).

        Args:
            df: Sorted time-series DataFrame.
            test_size: Fraction of rows reserved for the test set.
        """
        split_idx = int(len(df) * (1 - test_size))
        return df.iloc[:split_idx].copy(), df.iloc[split_idx:].copy()
