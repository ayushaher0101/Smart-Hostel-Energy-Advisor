"""
Smart Hostel Energy Advisor — Principal Component Analysis (PCA)
================================================================
Reduces dimensionality of the energy consumption dataset and visualises
the underlying structure in 2D space.

Algorithm: PCA (eigenvalue decomposition of the covariance matrix)
Library:   scikit-learn PCA
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(PROJECT_DIR, "dataset")
VIZ_DIR = os.path.join(PROJECT_DIR, "visualizations")
RESULTS_DIR = os.path.join(PROJECT_DIR, "results")
os.makedirs(VIZ_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({"figure.dpi": 150, "savefig.dpi": 150})


def run_pca():
    """Apply PCA and visualise the reduced-dimensionality structure."""
    # ─── Load data ────────────────────────────────────────────────
    # Use the clustered dataset so we can colour PCA plots by cluster
    clustered_path = os.path.join(DATASET_DIR, "clustered_dataset.csv")
    if os.path.exists(clustered_path):
        df = pd.read_csv(clustered_path, parse_dates=["date"])
    else:
        df = pd.read_csv(os.path.join(DATASET_DIR, "cleaned_dataset.csv"),
                         parse_dates=["date"])

    print("=" * 60)
    print("PRINCIPAL COMPONENT ANALYSIS — Dimensionality Reduction")
    print("=" * 60)

    # ─── Feature selection ────────────────────────────────────────
    # Only numerical features — NO identifiers, NO target labels.
    # daily_energy_kwh is EXCLUDED since it's the target variable
    # and including it would dominate the principal components.
    pca_features = ["occupants", "temperature_c", "ac_usage_hours",
                    "lighting_hours", "appliance_count", "is_weekend", "month"]

    X_raw = df[pca_features].copy()
    print(f"\nPCA input features ({len(pca_features)}): {pca_features}")
    print(f"Total samples: {len(X_raw)}")

    # ─── Standardisation ──────────────────────────────────────────
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_raw)
    print(f"✓ Features standardised (mean=0, std=1)")

    # ─── Full PCA (all components) ────────────────────────────────
    # First fit PCA with all components to get variance explained
    pca_full = PCA(n_components=len(pca_features), random_state=42)
    pca_full.fit(X_scaled)

    explained_var = pca_full.explained_variance_ratio_
    cumulative_var = np.cumsum(explained_var)

    print(f"\nExplained Variance Ratio by Component:")
    print(f"{'Component':>12s}  {'Individual':>12s}  {'Cumulative':>12s}")
    print(f"{'─' * 40}")
    for i in range(len(explained_var)):
        print(f"  PC{i+1:>8d}  {explained_var[i]:>12.4f}  {cumulative_var[i]:>12.4f}")

    # How many components for 90%?
    n_90 = np.argmax(cumulative_var >= 0.90) + 1
    n_95 = np.argmax(cumulative_var >= 0.95) + 1
    print(f"\n→ Components for ≥90% variance: {n_90}")
    print(f"→ Components for ≥95% variance: {n_95}")
    print(f"→ Information retained with 2 PCs: {cumulative_var[1]*100:.1f}%")
    print(f"→ Information lost with 2 PCs:     {(1-cumulative_var[1])*100:.1f}%")

    # ─── Reduce to 2 components for visualisation ─────────────────
    pca_2d = PCA(n_components=2, random_state=42)
    X_pca = pca_2d.fit_transform(X_scaled)

    df["PC1"] = X_pca[:, 0]
    df["PC2"] = X_pca[:, 1]

    # ─── Component Loadings ───────────────────────────────────────
    print(f"\nPCA Component Loadings:")
    loadings = pd.DataFrame(
        pca_2d.components_.T,
        index=pca_features,
        columns=["PC1", "PC2"]
    ).round(4)
    print(loadings.to_string())

    print(f"\nInterpretation:")
    # Find the top contributors for each PC
    for pc in ["PC1", "PC2"]:
        top = loadings[pc].abs().sort_values(ascending=False)
        top_feat = top.index[0]
        print(f"  {pc}: Dominated by '{top_feat}' (loading={loadings.loc[top_feat, pc]:.4f})")

    # ─── Save metrics ─────────────────────────────────────────────
    metrics = {
        "algorithm": "Principal Component Analysis (PCA)",
        "n_features": len(pca_features),
        "features": pca_features,
        "n_components_90pct": int(n_90),
        "n_components_95pct": int(n_95),
        "explained_variance_ratio": [round(x, 4) for x in explained_var],
        "cumulative_variance": [round(x, 4) for x in cumulative_var],
        "variance_retained_2pc": round(cumulative_var[1], 4),
        "variance_lost_2pc": round(1 - cumulative_var[1], 4),
        "loadings": loadings.to_dict(),
    }
    with open(os.path.join(RESULTS_DIR, "pca_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"\n✓ Metrics saved to: pca_metrics.json")

    # ─── Plot 1: PCA Scatter Plot (coloured by cluster) ──────────
    fig, ax = plt.subplots(figsize=(10, 7))

    if "cluster_label" in df.columns:
        scatter_colors = {"Low Consumption": "#55A868",
                          "Moderate Consumption": "#4C72B0",
                          "High Consumption": "#C44E52"}
        for label, color in scatter_colors.items():
            mask = df["cluster_label"] == label
            ax.scatter(df.loc[mask, "PC1"], df.loc[mask, "PC2"],
                       c=color, label=label, alpha=0.5, s=20, edgecolors="none")
        ax.legend(title="K-Means Cluster", fontsize=10)
    else:
        ax.scatter(df["PC1"], df["PC2"], alpha=0.4, s=15, c="#4C72B0")

    ax.set_xlabel(f"PC1 ({explained_var[0]*100:.1f}% variance)", fontsize=11)
    ax.set_ylabel(f"PC2 ({explained_var[1]*100:.1f}% variance)", fontsize=11)
    ax.set_title("PCA: 2D Projection of Hostel Energy Data", fontsize=12, pad=10)
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, "pca_scatter.png"))
    plt.close()
    print("✓ Saved: pca_scatter.png")

    # ─── Plot 2: Explained Variance Bar + Cumulative Line ─────────
    fig, ax = plt.subplots(figsize=(10, 6))
    pc_labels = [f"PC{i+1}" for i in range(len(explained_var))]
    bars = ax.bar(pc_labels, explained_var * 100, color="#4C72B0", alpha=0.7,
                  label="Individual")
    ax.plot(pc_labels, cumulative_var * 100, "o-", color="#C44E52", linewidth=2,
            markersize=8, label="Cumulative")
    ax.axhline(y=90, color="gray", linestyle="--", linewidth=1, alpha=0.7)
    ax.text(len(pc_labels)-1, 91, "90% threshold", fontsize=9, color="gray",
            ha="right")

    ax.set_xlabel("Principal Component", fontsize=11)
    ax.set_ylabel("Explained Variance (%)", fontsize=11)
    ax.set_title("PCA: Explained Variance by Component", fontsize=12, pad=10)
    ax.legend(fontsize=10)
    ax.set_ylim(0, 105)

    # Add percentage labels on bars
    for bar, val in zip(bars, explained_var * 100):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f"{val:.1f}%", ha="center", fontsize=9)

    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, "pca_explained_variance.png"))
    plt.close()
    print("✓ Saved: pca_explained_variance.png")

    # ─── Plot 3: Loading Vectors (Biplot-style) ───────────────────
    fig, ax = plt.subplots(figsize=(9, 7))

    # Plot data points (faded)
    ax.scatter(X_pca[:, 0], X_pca[:, 1], alpha=0.1, s=5, c="gray")

    # Plot loading vectors
    scale = max(abs(X_pca[:, 0]).max(), abs(X_pca[:, 1]).max()) * 0.8
    for i, feature in enumerate(pca_features):
        ax.arrow(0, 0,
                 pca_2d.components_[0, i] * scale,
                 pca_2d.components_[1, i] * scale,
                 head_width=0.08 * scale, head_length=0.04 * scale,
                 fc="#C44E52", ec="#C44E52", alpha=0.8, linewidth=1.5)
        ax.text(pca_2d.components_[0, i] * scale * 1.12,
                pca_2d.components_[1, i] * scale * 1.12,
                feature, fontsize=9, fontweight="bold", color="#333333")

    ax.set_xlabel(f"PC1 ({explained_var[0]*100:.1f}%)", fontsize=11)
    ax.set_ylabel(f"PC2 ({explained_var[1]*100:.1f}%)", fontsize=11)
    ax.set_title("PCA: Feature Loading Vectors (Biplot)", fontsize=12, pad=10)
    ax.axhline(y=0, color="gray", linewidth=0.5, alpha=0.5)
    ax.axvline(x=0, color="gray", linewidth=0.5, alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, "pca_biplot.png"))
    plt.close()
    print("✓ Saved: pca_biplot.png")

    return metrics


if __name__ == "__main__":
    run_pca()
