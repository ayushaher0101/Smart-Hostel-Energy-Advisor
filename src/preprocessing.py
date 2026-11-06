"""
Smart Hostel Energy Advisor — Data Preprocessing
=================================================
Cleans the raw dataset, performs basic checks, and prepares it for ML.
Also generates the Decision Tree classification target.
"""

import pandas as pd
import numpy as np
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(PROJECT_DIR, "dataset")


def load_and_clean(filepath: str) -> pd.DataFrame:
    """Load the raw dataset and perform cleaning steps."""
    df = pd.read_csv(filepath)
    print("=" * 60)
    print("DATA CLEANING REPORT")
    print("=" * 60)

    # 1. Shape
    print(f"\n1. Dataset shape: {df.shape[0]} rows × {df.shape[1]} columns")

    # 2. Data types
    print(f"\n2. Data types:")
    print(df.dtypes.to_string())

    # 3. Missing values
    missing = df.isnull().sum()
    print(f"\n3. Missing values:")
    if missing.sum() == 0:
        print("   No missing values found. ✓")
    else:
        print(missing[missing > 0].to_string())

    # 4. Duplicates
    dups = df.duplicated().sum()
    print(f"\n4. Duplicate rows: {dups}")
    if dups > 0:
        df = df.drop_duplicates()
        print(f"   Removed {dups} duplicates. New shape: {df.shape}")

    # 5. Parse date column
    df["date"] = pd.to_datetime(df["date"])
    print(f"\n5. Date column parsed. Range: {df['date'].min()} to {df['date'].max()}")

    # 6. Value range checks
    print(f"\n6. Value range checks:")
    print(f"   Temperature: {df['temperature_c'].min():.1f}°C to {df['temperature_c'].max():.1f}°C")
    print(f"   Occupants:   {df['occupants'].min()} to {df['occupants'].max()}")
    print(f"   AC hours:    {df['ac_usage_hours'].min():.1f} to {df['ac_usage_hours'].max():.1f}")
    print(f"   Energy:      {df['daily_energy_kwh'].min():.1f} to {df['daily_energy_kwh'].max():.1f} kWh")

    return df


def create_classification_target(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create the Decision Tree classification target.

    Strategy: For each hostel, compute the 75th percentile of
    daily_energy_kwh. Records above this threshold are labelled
    'High', otherwise 'Normal'.

    Per-hostel thresholds avoid bias from different hostel sizes
    (a large hostel naturally uses more energy than a small one).
    """
    print(f"\n{'=' * 60}")
    print("CLASSIFICATION TARGET CREATION")
    print("=" * 60)

    thresholds = df.groupby("hostel_id")["daily_energy_kwh"].quantile(0.75)
    print("\nPer-hostel 75th percentile thresholds (kWh):")
    for hostel, threshold in thresholds.items():
        print(f"  {hostel}: {threshold:.2f} kWh")

    # Apply threshold per hostel
    df["consumption_category"] = df.apply(
        lambda row: "High" if row["daily_energy_kwh"] > thresholds[row["hostel_id"]]
        else "Normal",
        axis=1
    )

    counts = df["consumption_category"].value_counts()
    print(f"\nClass distribution:")
    print(f"  Normal: {counts.get('Normal', 0)} ({counts.get('Normal', 0)/len(df)*100:.1f}%)")
    print(f"  High:   {counts.get('High', 0)} ({counts.get('High', 0)/len(df)*100:.1f}%)")

    return df


def preprocess():
    """Run the full preprocessing pipeline."""
    raw_path = os.path.join(DATASET_DIR, "raw_dataset.csv")
    df = load_and_clean(raw_path)
    df = create_classification_target(df)

    # Save cleaned dataset
    cleaned_path = os.path.join(DATASET_DIR, "cleaned_dataset.csv")
    df.to_csv(cleaned_path, index=False)
    print(f"\n✓ Cleaned dataset saved: {cleaned_path}")
    print(f"  Final shape: {df.shape}")

    return df


if __name__ == "__main__":
    preprocess()
