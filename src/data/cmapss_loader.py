"""Loads the NASA CMAPSS turbofan engine degradation dataset."""

from pathlib import Path

import pandas as pd

CMAPSS_COLUMNS = [
    "unit_id", "cycle",
    "op_setting_1", "op_setting_2", "op_setting_3",
    "sensor_1", "sensor_2", "sensor_3", "sensor_4", "sensor_5",
    "sensor_6", "sensor_7", "sensor_8", "sensor_9", "sensor_10",
    "sensor_11", "sensor_12", "sensor_13", "sensor_14", "sensor_15",
    "sensor_16", "sensor_17", "sensor_18", "sensor_19", "sensor_20",
    "sensor_21",
]

# Sensors with near-zero variance across all operating conditions (commonly dropped)
CONSTANT_SENSORS = ["sensor_1", "sensor_5", "sensor_10", "sensor_16", "sensor_18", "sensor_19"]


class CMAPSSLoader:
    """Loads and prepares the NASA CMAPSS FD00{1-4} datasets."""

    def __init__(self, data_dir: str = "data/raw/cmapss") -> None:
        self.data_dir = Path(data_dir)

    def load(self, subset: str = "FD001") -> tuple[pd.DataFrame, pd.DataFrame]:
        """Load train and test splits for a CMAPSS subset.

        Args:
            subset: One of 'FD001', 'FD002', 'FD003', 'FD004'.

        Returns:
            (train_df, test_df) with RUL column attached to both.
        """
        train_path = self.data_dir / f"train_{subset}.txt"
        test_path  = self.data_dir / f"test_{subset}.txt"
        rul_path   = self.data_dir / f"RUL_{subset}.txt"

        for p in [train_path, test_path, rul_path]:
            if not p.exists():
                raise FileNotFoundError(
                    f"{p} not found. Download CMAPSS from "
                    "https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health"
                    "/pcoe/pcoe-data-set-repository/"
                )

        train_df = pd.read_csv(train_path, sep=r"\s+", header=None, names=CMAPSS_COLUMNS)
        test_df  = pd.read_csv(test_path,  sep=r"\s+", header=None, names=CMAPSS_COLUMNS)

        # Compute RUL for training data (failure = last cycle per unit)
        max_cycle    = train_df.groupby("unit_id")["cycle"].max().rename("max_cycle")
        train_df     = train_df.join(max_cycle, on="unit_id")
        train_df["RUL"] = train_df["max_cycle"] - train_df["cycle"]
        train_df.drop(columns=["max_cycle"], inplace=True)

        # Attach ground-truth RUL to test data
        rul_df          = pd.read_csv(rul_path, sep=r"\s+", header=None, names=["RUL_at_end"])
        rul_df["unit_id"] = range(1, len(rul_df) + 1)
        last_cycles     = test_df.groupby("unit_id")["cycle"].max().rename("max_cycle")
        test_df         = test_df.join(last_cycles, on="unit_id")
        test_df         = test_df.join(rul_df.set_index("unit_id")["RUL_at_end"], on="unit_id")
        test_df["RUL"]  = test_df["RUL_at_end"] + (test_df["max_cycle"] - test_df["cycle"])
        test_df.drop(columns=["max_cycle", "RUL_at_end"], inplace=True)

        return train_df, test_df

    def add_failure_label(self, df: pd.DataFrame, rul_threshold: int = 30) -> pd.DataFrame:
        """Add a binary failure label: 1 if RUL <= threshold, else 0.

        Args:
            df: DataFrame with a 'RUL' column.
            rul_threshold: Cycles-to-failure below which a unit is considered
                in the failure zone. Default of 30 is standard in the literature.
        """
        df = df.copy()
        df["failure_imminent"] = (df["RUL"] <= rul_threshold).astype(int)
        return df

    def drop_constant_sensors(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove the six sensors that carry no information across operating modes."""
        return df.drop(columns=[c for c in CONSTANT_SENSORS if c in df.columns])
