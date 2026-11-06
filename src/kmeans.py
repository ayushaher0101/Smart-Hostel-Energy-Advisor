"""
Smart Hostel Energy Advisor — K-Means Clustering
==================================================
Groups hostel records into clusters based on energy-related features
to discover distinct consumption patterns.

Algorithm: K-Means (centroid-based partitional clustering)
Library:   scikit-learn KMeans
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
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(PROJECT_DIR, "dataset")
VIZ_DIR = os.path.join(PROJECT_DIR, "visualizations")
RESULTS_DIR = os.path.join(PROJECT_DIR, "results")
os.makedirs(VIZ_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({"figure.dpi": 150, "savefig.dpi": 150})


def run_kmeans():
    """Apply K-Means clustering and analyse consumption patterns."""
    # ─── Load data ────────────────────────────────────────────────
    df = pd.read_csv(os.path.join(DATASET_DIR, "cleaned_dataset.csv"),
                     parse_dates=["date"])

    print("=" * 60)
    print("K-MEANS CLUSTERING — Consumption Pattern Discovery")
    print("=" * 60)

    # ─── Feature selection ────────────────────────────────────────
    # All numerical features relevant to energy behaviour.
    # Identifiers (hostel_id, date) and the raw target are INCLUDED
    # for clustering since K-Means is unsupervised — we want to
    # discover natural groupings including consumption levels.
    cluster_features = ["occupants", "temperature_c", "ac_usage_hours",
                        "lighting_hours", "appliance_count", "is_weekend",
                        "daily_energy_kwh"]

    X_raw = df[cluster_features].copy()
    print(f"\nClustering features ({len(cluster_features)}): {cluster_features}")
    print(f"Total samples: {len(X_raw)}")

    # ─── Standardisation ──────────────────────────────────────────
    # K-Means uses Euclidean distance, so features must be on the
    # same scale. StandardScaler transforms each feature to have
    # mean=0, std=1.
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_raw)
    print(f"\n✓ Features standardised (mean=0, std=1)")

    # ─── Elbow Method ─────────────────────────────────────────────
    # The elbow method plots inertia (within-cluster sum of squares)
    # against number of clusters. The "elbow" point where the rate
    # of decrease sharply changes suggests a good k value.
    print(f"\nRunning Elbow Method (k=2 to k=10)...")
    k_range = range(2, 11)
    inertias = []
    silhouette_scores = []

    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10, max_iter=300)
        km.fit(X_scaled)
        inertias.append(km.inertia_)
        sil = silhouette_score(X_scaled, km.labels_)
        silhouette_scores.append(sil)
        print(f"  k={k:2d}  |  Inertia: {km.inertia_:10.2f}  |  Silhouette: {sil:.4f}")

    # ─── Select optimal k ─────────────────────────────────────────
    # Pick k with best silhouette score (among k=2..10)
    best_k_idx = np.argmax(silhouette_scores)
    best_k = list(k_range)[best_k_idx]
    print(f"\n→ Best silhouette score at k={best_k} ({silhouette_scores[best_k_idx]:.4f})")
    print(f"  Using k=3 for interpretability (Low/Moderate/High consumption)")

    # We'll use k=3 for interpretability, unless the elbow strongly
    # suggests otherwise. Three clusters map well to the domain problem.
    chosen_k = 3

    # ─── Final K-Means with chosen k ──────────────────────────────
    km_final = KMeans(n_clusters=chosen_k, random_state=42, n_init=10, max_iter=300)
    df["cluster"] = km_final.fit_predict(X_scaled)
    final_silhouette = silhouette_score(X_scaled, df["cluster"])

    print(f"\n{'─' * 40}")
    print(f"FINAL CLUSTERING (k={chosen_k})")
    print(f"{'─' * 40}")
    print(f"  Silhouette Score: {final_silhouette:.4f}")
    print(f"  Inertia:          {km_final.inertia_:.2f}")

    # ─── Cluster Profile Analysis ─────────────────────────────────
    # Analyse each cluster's characteristics BEFORE assigning labels.
    print(f"\nCluster Profiles (mean values):")
    profile = df.groupby("cluster")[cluster_features].mean().round(2)
    print(profile.to_string())

    # Assign descriptive labels based on daily_energy_kwh mean
    cluster_energy_means = profile["daily_energy_kwh"].sort_values()
    label_map = {}
    labels_ordered = ["Low Consumption", "Moderate Consumption", "High Consumption"]
    for i, (cluster_id, _) in enumerate(cluster_energy_means.items()):
        label_map[cluster_id] = labels_ordered[i]

    df["cluster_label"] = df["cluster"].map(label_map)

    print(f"\nCluster label assignment (based on mean energy):")
    for cluster_id, label in sorted(label_map.items()):
        count = (df["cluster"] == cluster_id).sum()
        mean_energy = profile.loc[cluster_id, "daily_energy_kwh"]
        print(f"  Cluster {cluster_id} → {label:25s} (n={count}, mean={mean_energy:.1f} kWh)")

    # ─── Save metrics ─────────────────────────────────────────────
    metrics = {
        "algorithm": "K-Means Clustering",
        "chosen_k": chosen_k,
        "silhouette_score": round(final_silhouette, 4),
        "inertia": round(km_final.inertia_, 2),
        "cluster_sizes": df["cluster"].value_counts().to_dict(),
        "cluster_labels": label_map,
        "elbow_data": {
            "k_values": list(k_range),
            "inertias": [round(x, 2) for x in inertias],
            "silhouette_scores": [round(x, 4) for x in silhouette_scores],
        },
        "cluster_profiles": profile.to_dict(),
    }
    with open(os.path.join(RESULTS_DIR, "kmeans_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2, default=str)
    print(f"\n✓ Metrics saved to: kmeans_metrics.json")

    # ─── Plot 1: Elbow Curve ──────────────────────────────────────
    fig, ax1 = plt.subplots(figsize=(10, 5))
    color1 = "#4C72B0"
    ax1.plot(list(k_range), inertias, "o-", color=color1, linewidth=2, markersize=8)
    ax1.set_xlabel("Number of Clusters (k)", fontsize=11)
    ax1.set_ylabel("Inertia (WCSS)", fontsize=11, color=color1)
    ax1.tick_params(axis="y", labelcolor=color1)
    ax1.set_title("K-Means: Elbow Method & Silhouette Score", fontsize=12, pad=10)
    ax1.set_xticks(list(k_range))

    # Secondary y-axis for silhouette
    ax2 = ax1.twinx()
    color2 = "#DD8452"
    ax2.plot(list(k_range), silhouette_scores, "s--", color=color2, linewidth=2, markersize=8)
    ax2.set_ylabel("Silhouette Score", fontsize=11, color=color2)
    ax2.tick_params(axis="y", labelcolor=color2)

    # Mark chosen k
    ax1.axvline(x=chosen_k, color="gray", linestyle=":", linewidth=1.5, alpha=0.7)
    ax1.annotate(f"Chosen k={chosen_k}", xy=(chosen_k, inertias[chosen_k-2]),
                 xytext=(chosen_k+0.5, inertias[chosen_k-2]),
                 fontsize=10, color="gray")

    fig.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, "km_elbow_curve.png"))
    plt.close()
    print("✓ Saved: km_elbow_curve.png")

    # ─── Plot 2: Cluster Distribution ─────────────────────────────
    fig, ax = plt.subplots(figsize=(8, 5))
    cluster_counts = df["cluster_label"].value_counts()
    colors_bar = ["#55A868", "#4C72B0", "#C44E52"]
    ordered_labels = ["Low Consumption", "Moderate Consumption", "High Consumption"]
    ordered_counts = [cluster_counts.get(l, 0) for l in ordered_labels]
    ax.bar(ordered_labels, ordered_counts, color=colors_bar)
    ax.set_xlabel("Cluster", fontsize=11)
    ax.set_ylabel("Number of Records", fontsize=11)
    ax.set_title("K-Means: Cluster Distribution", fontsize=12, pad=10)

    # Add count labels on bars
    for i, (label, count) in enumerate(zip(ordered_labels, ordered_counts)):
        ax.text(i, count + 10, str(count), ha="center", fontsize=11, fontweight="bold")

    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, "km_cluster_distribution.png"))
    plt.close()
    print("✓ Saved: km_cluster_distribution.png")

    # ─── Plot 3: 2D Cluster Scatter (using top 2 features) ───────
    # Use occupants and ac_usage_hours as the two most descriptive axes
    fig, ax = plt.subplots(figsize=(10, 7))
    scatter_colors = {"Low Consumption": "#55A868",
                      "Moderate Consumption": "#4C72B0",
                      "High Consumption": "#C44E52"}
    for label, color in scatter_colors.items():
        mask = df["cluster_label"] == label
        ax.scatter(df.loc[mask, "occupants"],
                   df.loc[mask, "daily_energy_kwh"],
                   c=color, label=label, alpha=0.5, s=20, edgecolors="none")

    ax.set_xlabel("Number of Occupants", fontsize=11)
    ax.set_ylabel("Daily Energy Consumption (kWh)", fontsize=11)
    ax.set_title("K-Means: Cluster Scatter Plot (Occupants vs Energy)", fontsize=12, pad=10)
    ax.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, "km_cluster_scatter.png"))
    plt.close()
    print("✓ Saved: km_cluster_scatter.png")

    # Save clustered dataset for PCA
    df.to_csv(os.path.join(DATASET_DIR, "clustered_dataset.csv"), index=False)
    print(f"✓ Clustered dataset saved for PCA")

    return metrics


if __name__ == "__main__":
    run_kmeans()
