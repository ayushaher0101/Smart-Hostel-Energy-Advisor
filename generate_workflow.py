"""
Generate the project workflow diagram for the report.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
VIZ_DIR = os.path.join(PROJECT_DIR, "visualizations")

fig, ax = plt.subplots(figsize=(10, 14))
ax.set_xlim(0, 10)
ax.set_ylim(0, 16)
ax.axis("off")

# Colors
blue = "#3B82F6"
green = "#22C55E"
orange = "#F59E0B"
purple = "#8B5CF6"
gray = "#6B7280"
light_blue = "#DBEAFE"
light_green = "#DCFCE7"
light_orange = "#FEF3C7"
light_purple = "#EDE9FE"

def draw_box(x, y, w, h, text, facecolor, edgecolor, fontsize=10, bold=False):
    rect = mpatches.FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle="round,pad=0.15", facecolor=facecolor,
        edgecolor=edgecolor, linewidth=1.8
    )
    ax.add_patch(rect)
    weight = "bold" if bold else "normal"
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize,
            fontweight=weight, color="#1F2937")

def draw_arrow(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=gray, lw=1.5))

# Title
ax.text(5, 15.5, "Smart Hostel Energy Advisor", fontsize=16,
        ha="center", va="center", fontweight="bold", color="#1E3A5F")
ax.text(5, 15.0, "Project Workflow", fontsize=11,
        ha="center", va="center", color=gray)

# Step 1
draw_box(5, 14.0, 4, 0.6, "Problem Definition", light_blue, blue, 10, True)
draw_arrow(5, 13.7, 5, 13.1)

# Step 2
draw_box(5, 12.8, 4, 0.6, "Synthetic Dataset Generation\n(1825 records)", light_blue, blue, 9)
draw_arrow(5, 12.5, 5, 11.9)

# Step 3
draw_box(5, 11.6, 4, 0.6, "Exploratory Data Analysis", light_blue, blue, 10)
draw_arrow(5, 11.3, 5, 10.7)

# Step 4
draw_box(5, 10.4, 4, 0.6, "Data Cleaning & Preprocessing", light_blue, blue, 10)
draw_arrow(5, 10.1, 5, 9.5)

# Step 5
draw_box(5, 9.2, 4, 0.6, "Feature Selection & Scaling", light_blue, blue, 10)

# Branch arrows
draw_arrow(5, 8.9, 2.5, 8.1)
draw_arrow(5, 8.9, 5, 8.1)
draw_arrow(5, 8.9, 7.5, 8.1)

# ML Models row 1
draw_box(2.5, 7.8, 3.2, 0.6, "Linear Regression\n(Prediction)", light_green, green, 9)
draw_box(5, 7.8, 3.2, 0.6, "Decision Tree\n(Classification)", light_green, green, 9)
draw_box(7.5, 7.8, 3.2, 0.6, "K-Means Clustering\n(Pattern Discovery)", light_green, green, 9)

# PCA below K-Means
draw_arrow(7.5, 7.5, 7.5, 6.9)
draw_box(7.5, 6.6, 3.2, 0.6, "PCA\n(Dimensionality Reduction)", light_purple, purple, 9)

# Converge arrows
draw_arrow(2.5, 7.5, 5, 5.9)
draw_arrow(5, 7.5, 5, 5.9)
draw_arrow(7.5, 6.3, 5, 5.9)

# Step 6
draw_box(5, 5.6, 4, 0.6, "Model Evaluation", light_orange, orange, 10, True)
draw_arrow(5, 5.3, 5, 4.7)

# Step 7
draw_box(5, 4.4, 4, 0.6, "Visualisation & Interpretation", light_orange, orange, 10)
draw_arrow(5, 4.1, 5, 3.5)

# Step 8
draw_box(5, 3.2, 4, 0.6, "Energy Consumption Insights", light_orange, orange, 10)
draw_arrow(5, 2.9, 5, 2.3)

# Step 9
draw_box(5, 2.0, 4, 0.6, "Conclusion & Recommendations", light_blue, blue, 10, True)

plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, "project_workflow.png"), dpi=200,
            bbox_inches="tight", facecolor="white")
plt.close()
print("Saved: project_workflow.png")
