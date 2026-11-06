"""
Smart Hostel Energy Advisor — Decision Tree Classifier
=======================================================
Classifies hostel energy consumption as 'Normal' or 'High' to identify
the factors contributing to high electricity usage.

Algorithm: Decision Tree (CART) with Gini impurity
Library:   scikit-learn DecisionTreeClassifier
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, classification_report)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(PROJECT_DIR, "dataset")
VIZ_DIR = os.path.join(PROJECT_DIR, "visualizations")
RESULTS_DIR = os.path.join(PROJECT_DIR, "results")
os.makedirs(VIZ_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({"figure.dpi": 150, "savefig.dpi": 150})


def run_decision_tree():
    """Train and evaluate a Decision Tree Classifier."""
    # ─── Load data ────────────────────────────────────────────────
    df = pd.read_csv(os.path.join(DATASET_DIR, "cleaned_dataset.csv"),
                     parse_dates=["date"])

    print("=" * 60)
    print("DECISION TREE — High Consumption Classification")
    print("=" * 60)

    # ─── Feature and target selection ─────────────────────────────
    # IMPORTANT: daily_energy_kwh is EXCLUDED to prevent target leakage.
    # The classification label (consumption_category) was derived from
    # daily_energy_kwh, so including it would make the model trivially perfect.
    feature_cols = ["occupants", "temperature_c", "ac_usage_hours",
                    "lighting_hours", "appliance_count", "is_weekend", "month"]

    X = df[feature_cols]
    y = df["consumption_category"]

    print(f"\nFeatures ({len(feature_cols)}): {feature_cols}")
    print(f"Target: consumption_category (Normal / High)")
    print(f"\nClass distribution:")
    print(y.value_counts().to_string())

    # ─── Train-Test Split (80/20) ─────────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"\nTrain set: {len(X_train)} samples")
    print(f"Test set:  {len(X_test)} samples")

    # ─── Train the Decision Tree ──────────────────────────────────
    # max_depth=5 to keep the tree interpretable and avoid overfitting.
    # criterion='gini' uses Gini impurity for splitting.
    dt_model = DecisionTreeClassifier(
        criterion="gini",
        max_depth=5,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=42
    )
    dt_model.fit(X_train, y_train)

    # ─── Predictions ──────────────────────────────────────────────
    y_pred = dt_model.predict(X_test)

    # ─── Evaluation Metrics ───────────────────────────────────────
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, pos_label="High")
    recall = recall_score(y_test, y_pred, pos_label="High")
    f1 = f1_score(y_test, y_pred, pos_label="High")
    cm = confusion_matrix(y_test, y_pred, labels=["Normal", "High"])

    print(f"\n{'─' * 40}")
    print(f"EVALUATION METRICS (Test Set)")
    print(f"{'─' * 40}")
    print(f"  Accuracy:  {accuracy:.4f}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall:    {recall:.4f}")
    print(f"  F1-Score:  {f1:.4f}")
    print(f"{'─' * 40}")

    print(f"\nConfusion Matrix:")
    print(f"              Predicted")
    print(f"              Normal  High")
    print(f"  Actual Normal  {cm[0][0]:5d}  {cm[0][1]:5d}")
    print(f"  Actual High    {cm[1][0]:5d}  {cm[1][1]:5d}")

    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Normal", "High"]))

    # ─── Feature Importance ───────────────────────────────────────
    importance_df = pd.DataFrame({
        "Feature": feature_cols,
        "Importance": dt_model.feature_importances_
    }).sort_values("Importance", ascending=False)

    print(f"Feature Importance:")
    for _, row in importance_df.iterrows():
        bar = "█" * int(row["Importance"] * 50)
        print(f"  {row['Feature']:20s}: {row['Importance']:.4f}  {bar}")

    # Save metrics
    metrics = {
        "algorithm": "Decision Tree Classifier",
        "criterion": "gini",
        "max_depth": 5,
        "features": feature_cols,
        "train_size": len(X_train),
        "test_size": len(X_test),
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "confusion_matrix": cm.tolist(),
        "feature_importance": {row["Feature"]: round(row["Importance"], 4)
                               for _, row in importance_df.iterrows()},
    }
    with open(os.path.join(RESULTS_DIR, "decision_tree_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"\n✓ Metrics saved to: decision_tree_metrics.json")

    # ─── Plot 1: Confusion Matrix ─────────────────────────────────
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Normal", "High"],
                yticklabels=["Normal", "High"], ax=ax,
                annot_kws={"size": 14})
    ax.set_xlabel("Predicted Label", fontsize=11)
    ax.set_ylabel("Actual Label", fontsize=11)
    ax.set_title("Decision Tree: Confusion Matrix", fontsize=12, pad=10)
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, "dt_confusion_matrix.png"))
    plt.close()
    print("✓ Saved: dt_confusion_matrix.png")

    # ─── Plot 2: Decision Tree Visualisation ──────────────────────
    fig, ax = plt.subplots(figsize=(24, 10))
    plot_tree(dt_model, feature_names=feature_cols,
              class_names=["Normal", "High"], filled=True,
              rounded=True, ax=ax, fontsize=8, proportion=True)
    ax.set_title("Decision Tree Visualisation", fontsize=14, pad=20)
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, "dt_tree_visualisation.png"),
                bbox_inches="tight")
    plt.close()
    print("✓ Saved: dt_tree_visualisation.png")

    # ─── Plot 3: Feature Importance Bar Chart ─────────────────────
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = sns.color_palette("viridis", len(importance_df))
    ax.barh(importance_df["Feature"], importance_df["Importance"], color=colors)
    ax.set_xlabel("Importance Score (Gini)", fontsize=11)
    ax.set_title("Decision Tree: Feature Importance", fontsize=12, pad=10)
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, "dt_feature_importance.png"))
    plt.close()
    print("✓ Saved: dt_feature_importance.png")

    return metrics


if __name__ == "__main__":
    run_decision_tree()
