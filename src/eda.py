"""
Smart Hostel Energy Advisor — Exploratory Data Analysis (EDA)
==============================================================
Generates all EDA visualisations and prints summary statistics.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # non-interactive backend for saving figures
import matplotlib.pyplot as plt
import seaborn as sns
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(PROJECT_DIR, "dataset")
VIZ_DIR = os.path.join(PROJECT_DIR, "visualizations")
os.makedirs(VIZ_DIR, exist_ok=True)

# ─── Consistent styling ───────────────────────────────────────────
plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 150,
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "figure.figsize": (10, 6),
})
sns.set_theme(style="whitegrid", palette="muted")


def run_eda():
    """Perform full EDA and save visualisations."""
    filepath = os.path.join(DATASET_DIR, "cleaned_dataset.csv")
    df = pd.read_csv(filepath, parse_dates=["date"])

    print("=" * 60)
    print("EXPLORATORY DATA ANALYSIS")
    print("=" * 60)

    # ─── 1. Dataset overview ──────────────────────────────────────
    print(f"\n1. DATASET OVERVIEW")
    print(f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"\n   Data Types:")
    print(df.dtypes.to_string())
    print(f"\n   Missing Values: {df.isnull().sum().sum()}")
    print(f"   Duplicates:     {df.duplicated().sum()}")

    # ─── 2. Descriptive statistics ────────────────────────────────
    print(f"\n2. DESCRIPTIVE STATISTICS")
    numeric_cols = ["occupants", "temperature_c", "ac_usage_hours",
                    "lighting_hours", "appliance_count", "daily_energy_kwh"]
    stats = df[numeric_cols].describe().round(2)
    print(stats.to_string())

    # Save stats to results
    results_dir = os.path.join(PROJECT_DIR, "results")
    os.makedirs(results_dir, exist_ok=True)
    stats.to_csv(os.path.join(results_dir, "descriptive_statistics.csv"))

    # ─── 3. Correlation Heatmap ───────────────────────────────────
    print(f"\n3. Generating correlation heatmap...")
    fig, ax = plt.subplots(figsize=(9, 7))
    corr_matrix = df[numeric_cols].corr().round(2)
    sns.heatmap(corr_matrix, annot=True, cmap="RdYlBu_r", center=0,
                square=True, linewidths=0.5, ax=ax, fmt=".2f",
                vmin=-1, vmax=1)
    ax.set_title("Correlation Heatmap — Hostel Energy Features", fontsize=13, pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, "correlation_heatmap.png"))
    plt.close()
    print("   Saved: correlation_heatmap.png")

    print(f"\n   Correlation matrix:")
    print(corr_matrix.to_string())

    # ─── 4. Feature distributions ─────────────────────────────────
    print(f"\n4. Generating feature distribution plots...")
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    axes = axes.flatten()
    for i, col in enumerate(numeric_cols):
        sns.histplot(df[col], kde=True, ax=axes[i], color=sns.color_palette("muted")[i])
        axes[i].set_title(f"Distribution of {col}")
        axes[i].set_xlabel(col)
        axes[i].set_ylabel("Frequency")
    plt.suptitle("Feature Distributions", fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, "feature_distributions.png"), bbox_inches="tight")
    plt.close()
    print("   Saved: feature_distributions.png")

    # ─── 5. Energy consumption by hostel ──────────────────────────
    print(f"\n5. Generating energy by hostel boxplot...")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x="hostel_id", y="daily_energy_kwh", palette="Set2", ax=ax)
    ax.set_title("Daily Energy Consumption by Hostel", fontsize=13)
    ax.set_xlabel("Hostel ID")
    ax.set_ylabel("Daily Energy (kWh)")
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, "energy_by_hostel.png"))
    plt.close()
    print("   Saved: energy_by_hostel.png")

    # ─── 6. Energy vs Temperature ─────────────────────────────────
    print(f"\n6. Generating energy vs temperature scatter...")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x="temperature_c", y="daily_energy_kwh",
                    hue="hostel_id", alpha=0.5, ax=ax, palette="Set2", s=20)
    ax.set_title("Energy Consumption vs Temperature", fontsize=13)
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Daily Energy (kWh)")
    ax.legend(title="Hostel", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, "energy_vs_temperature.png"), bbox_inches="tight")
    plt.close()
    print("   Saved: energy_vs_temperature.png")

    # ─── 7. Monthly energy trend ──────────────────────────────────
    print(f"\n7. Generating monthly energy trend...")
    monthly = df.groupby("month")["daily_energy_kwh"].mean()
    fig, ax = plt.subplots(figsize=(10, 5))
    monthly.plot(kind="bar", color=sns.color_palette("coolwarm", 12), ax=ax)
    ax.set_title("Average Daily Energy Consumption by Month", fontsize=13)
    ax.set_xlabel("Month")
    ax.set_ylabel("Average Daily Energy (kWh)")
    ax.set_xticklabels(["Jan","Feb","Mar","Apr","May","Jun",
                         "Jul","Aug","Sep","Oct","Nov","Dec"], rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, "monthly_energy_trend.png"))
    plt.close()
    print("   Saved: monthly_energy_trend.png")

    # ─── 8. Weekend vs Weekday ────────────────────────────────────
    print(f"\n8. Generating weekend vs weekday comparison...")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df, x="is_weekend", y="daily_energy_kwh", palette="pastel", ax=ax)
    ax.set_xticklabels(["Weekday", "Weekend"])
    ax.set_title("Energy Consumption: Weekday vs Weekend", fontsize=13)
    ax.set_xlabel("")
    ax.set_ylabel("Daily Energy (kWh)")
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, "weekend_vs_weekday.png"))
    plt.close()
    print("   Saved: weekend_vs_weekday.png")

    # ─── 9. Energy vs AC usage ────────────────────────────────────
    print(f"\n9. Generating energy vs AC usage scatter...")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x="ac_usage_hours", y="daily_energy_kwh",
                    hue="hostel_id", alpha=0.5, ax=ax, palette="Set2", s=20)
    ax.set_title("Energy Consumption vs AC Usage Hours", fontsize=13)
    ax.set_xlabel("AC Usage Hours")
    ax.set_ylabel("Daily Energy (kWh)")
    ax.legend(title="Hostel", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, "energy_vs_ac_usage.png"), bbox_inches="tight")
    plt.close()
    print("   Saved: energy_vs_ac_usage.png")

    print(f"\n{'=' * 60}")
    print(f"EDA COMPLETE — {9} visualisations saved to: {VIZ_DIR}")
    print("=" * 60)

    return df


if __name__ == "__main__":
    run_eda()
