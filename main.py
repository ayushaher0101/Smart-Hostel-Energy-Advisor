"""
Smart Hostel Energy Advisor — Main Pipeline
=============================================
Runs the entire project pipeline from data generation to PCA.
Execute this file to reproduce all results.
"""

import os
import sys

# Ensure src/ is importable
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(PROJECT_DIR, "src")
sys.path.insert(0, SRC_DIR)

from data_generation import generate_dataset
from preprocessing import preprocess
from eda import run_eda
from linear_regression import run_linear_regression
from decision_tree import run_decision_tree
from kmeans import run_kmeans
from pca import run_pca


def main():
    print("\n" + "=" * 60)
    print("  SMART HOSTEL ENERGY ADVISOR - Full Pipeline")
    print("  Ayush Aher | 25BIT028 | PDEU")
    print("=" * 60)

    print("\n\n" + "=" * 60)
    print("STEP 1/7: DATASET GENERATION")
    print("=" * 60)
    generate_dataset()

    print("\n\n" + "=" * 60)
    print("STEP 2/7: DATA PREPROCESSING")
    print("=" * 60)
    preprocess()

    print("\n\n" + "=" * 60)
    print("STEP 3/7: EXPLORATORY DATA ANALYSIS")
    print("=" * 60)
    run_eda()

    print("\n\n" + "=" * 60)
    print("STEP 4/7: LINEAR REGRESSION")
    print("=" * 60)
    lr_metrics = run_linear_regression()

    print("\n\n" + "=" * 60)
    print("STEP 5/7: DECISION TREE")
    print("=" * 60)
    dt_metrics = run_decision_tree()

    print("\n\n" + "=" * 60)
    print("STEP 6/7: K-MEANS CLUSTERING")
    print("=" * 60)
    km_metrics = run_kmeans()

    print("\n\n" + "=" * 60)
    print("STEP 7/7: PRINCIPAL COMPONENT ANALYSIS")
    print("=" * 60)
    pca_metrics = run_pca()

    # ─── Summary ──────────────────────────────────────────────────
    print("\n\n" + "=" * 60)
    print("  PIPELINE COMPLETE - RESULTS SUMMARY")
    print("=" * 60)
    print(f"\n  Linear Regression:")
    print(f"    R² = {lr_metrics['R2']:.4f}   RMSE = {lr_metrics['RMSE']:.4f} kWh")
    print(f"\n  Decision Tree:")
    print(f"    Accuracy = {dt_metrics['accuracy']:.4f}   F1 = {dt_metrics['f1_score']:.4f}")
    print(f"\n  K-Means Clustering:")
    print(f"    k = {km_metrics['chosen_k']}   Silhouette = {km_metrics['silhouette_score']:.4f}")
    print(f"\n  PCA:")
    print(f"    Variance retained (2 PCs) = {pca_metrics['variance_retained_2pc']*100:.1f}%")

    print(f"\n  Output directories:")
    print(f"    Dataset:        {os.path.join(PROJECT_DIR, 'dataset')}")
    print(f"    Visualizations: {os.path.join(PROJECT_DIR, 'visualizations')}")
    print(f"    Results:        {os.path.join(PROJECT_DIR, 'results')}")
    print("=" * 60)


if __name__ == "__main__":
    main()
