"""
Smart Hostel Energy Advisor — Linear Regression
=================================================
Predicts daily electricity consumption (kWh) using hostel-related features.

Algorithm: Ordinary Least Squares (OLS) Linear Regression
Library:   scikit-learn LinearRegression
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
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(PROJECT_DIR, "dataset")
VIZ_DIR = os.path.join(PROJECT_DIR, "visualizations")
RESULTS_DIR = os.path.join(PROJECT_DIR, "results")
os.makedirs(VIZ_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({"figure.dpi": 150, "savefig.dpi": 150})


def run_linear_regression():
    """Train and evaluate a Linear Regression model."""
    # ─── Load data ────────────────────────────────────────────────
    df = pd.read_csv(os.path.join(DATASET_DIR, "cleaned_dataset.csv"),
                     parse_dates=["date"])

    print("=" * 60)
    print("LINEAR REGRESSION — Energy Consumption Prediction")
    print("=" * 60)

    # ─── Feature and target selection ─────────────────────────────
    # We use numerical features that influence energy consumption.
    # hostel_id, date, consumption_category are excluded.
    feature_cols = ["occupants", "temperature_c", "ac_usage_hours",
                    "lighting_hours", "appliance_count", "is_weekend", "month"]

    X = df[feature_cols]
    y = df["daily_energy_kwh"]

    print(f"\nFeatures ({len(feature_cols)}): {feature_cols}")
    print(f"Target: daily_energy_kwh")
    print(f"Total samples: {len(X)}")

    # ─── Train-Test Split (80/20) ─────────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    print(f"\nTrain set: {len(X_train)} samples")
    print(f"Test set:  {len(X_test)} samples")

    # ─── Train the model ──────────────────────────────────────────
    model = LinearRegression()
    model.fit(X_train, y_train)

    # ─── Coefficients ─────────────────────────────────────────────
    print(f"\nModel Coefficients:")
    print(f"  Intercept: {model.intercept_:.4f}")
    coeff_df = pd.DataFrame({
        "Feature": feature_cols,
        "Coefficient": model.coef_
    }).sort_values("Coefficient", key=abs, ascending=False)

    for _, row in coeff_df.iterrows():
        print(f"  {row['Feature']:20s}: {row['Coefficient']:+.4f}")

    # ─── Predictions ──────────────────────────────────────────────
    y_pred = model.predict(X_test)

    # ─── Evaluation Metrics ───────────────────────────────────────
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print(f"\n{'─' * 40}")
    print(f"EVALUATION METRICS (Test Set)")
    print(f"{'─' * 40}")
    print(f"  MAE  (Mean Absolute Error):      {mae:.4f} kWh")
    print(f"  MSE  (Mean Squared Error):       {mse:.4f}")
    print(f"  RMSE (Root Mean Squared Error):  {rmse:.4f} kWh")
    print(f"  R²   (Coefficient of Determination): {r2:.4f}")
    print(f"{'─' * 40}")

    # Save metrics to JSON
    metrics = {
        "algorithm": "Linear Regression",
        "features": feature_cols,
        "train_size": len(X_train),
        "test_size": len(X_test),
        "MAE": round(mae, 4),
        "MSE": round(mse, 4),
        "RMSE": round(rmse, 4),
        "R2": round(r2, 4),
        "intercept": round(model.intercept_, 4),
        "coefficients": {f: round(c, 4) for f, c in zip(feature_cols, model.coef_)},
    }
    with open(os.path.join(RESULTS_DIR, "linear_regression_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"\n✓ Metrics saved to: linear_regression_metrics.json")

    # ─── Plot 1: Actual vs Predicted ──────────────────────────────
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(y_test, y_pred, alpha=0.4, s=15, color="#4C72B0", edgecolors="none")

    # Perfect prediction line
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    ax.plot([min_val, max_val], [min_val, max_val], "r--", linewidth=1.5,
            label="Perfect Prediction")

    ax.set_xlabel("Actual Energy Consumption (kWh)", fontsize=11)
    ax.set_ylabel("Predicted Energy Consumption (kWh)", fontsize=11)
    ax.set_title("Linear Regression: Actual vs Predicted Energy Consumption",
                 fontsize=12, pad=10)
    ax.legend(fontsize=10)

    # Add metrics text box
    textstr = f"R² = {r2:.4f}\nRMSE = {rmse:.2f} kWh\nMAE = {mae:.2f} kWh"
    props = dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.8)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=9,
            verticalalignment="top", bbox=props)

    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, "lr_actual_vs_predicted.png"))
    plt.close()
    print("✓ Saved: lr_actual_vs_predicted.png")

    # ─── Plot 2: Residual Plot ────────────────────────────────────
    residuals = y_test.values - y_pred
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(y_pred, residuals, alpha=0.4, s=15, color="#DD8452", edgecolors="none")
    ax.axhline(y=0, color="red", linestyle="--", linewidth=1)
    ax.set_xlabel("Predicted Energy Consumption (kWh)", fontsize=11)
    ax.set_ylabel("Residuals (Actual - Predicted)", fontsize=11)
    ax.set_title("Linear Regression: Residual Plot", fontsize=12, pad=10)
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, "lr_residual_plot.png"))
    plt.close()
    print("✓ Saved: lr_residual_plot.png")

    # ─── Plot 3: Coefficient Bar Chart ────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ["#55A868" if c > 0 else "#C44E52" for c in coeff_df["Coefficient"]]
    ax.barh(coeff_df["Feature"], coeff_df["Coefficient"], color=colors)
    ax.set_xlabel("Coefficient Value", fontsize=11)
    ax.set_title("Linear Regression: Feature Coefficients", fontsize=12, pad=10)
    ax.axvline(x=0, color="gray", linestyle="-", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, "lr_coefficients.png"))
    plt.close()
    print("✓ Saved: lr_coefficients.png")

    return metrics


if __name__ == "__main__":
    run_linear_regression()
