"""
Generate the conceptual illustration for Smart Hostel Energy Advisor.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
VIZ_DIR = os.path.join(PROJECT_DIR, "visualizations")

fig, ax = plt.subplots(figsize=(11, 7))
ax.set_xlim(0, 11)
ax.set_ylim(0, 7)
ax.axis("off")

# Colors
c_hostel = "#EFF6FF"
b_hostel = "#3B82F6"
c_meter = "#FEF3C7"
b_meter = "#F59E0B"
c_ml = "#DCFCE7"
b_ml = "#10B981"
c_action = "#F3E8FF"
b_action = "#8B5CF6"

def draw_card(x, y, w, h, title, items, bg, border):
    patch = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2",
                                  facecolor=bg, edgecolor=border, linewidth=2)
    ax.add_patch(patch)
    ax.text(x + w/2, y + h - 0.4, title, ha="center", va="center",
            fontsize=11, fontweight="bold", color="#1F2937")
    line_y = y + h - 0.9
    for item in items:
        ax.text(x + 0.3, line_y, f"- {item}", ha="left", va="center",
                fontsize=9.5, color="#374151")
        line_y -= 0.45

def draw_conn(x1, y1, x2, y2, label=""):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color="#4B5563", lw=2, mutation_scale=15))
    if label:
        ax.text((x1 + x2)/2, (y1 + y2)/2 + 0.25, label, ha="center", va="center",
                fontsize=8.5, color="#4B5563", fontweight="semibold")

# 1. Physical Layer
draw_card(0.5, 1.5, 2.2, 4.2, "Hostel Facilities",
          ["5 Hostel Blocks", "100-300 Occupants", "ACs & Heating", "Room Lighting", "Common Appliances"],
          c_hostel, b_hostel)

# 2. Data Collection Layer
draw_card(3.1, 1.5, 2.2, 4.2, "Smart Metering",
          ["Sub-metered logs", "Daily kWh Readings", "Weather sensors", "Occupancy logs", "Appliance counts"],
          c_meter, b_meter)

# 3. AI / ML Analytics Engine
draw_card(5.7, 1.0, 2.3, 5.2, "ML Advisory Core",
          ["Linear Regression:\n  Load forecasting",
           "Decision Tree:\n  Wastage classification",
           "K-Means Clustering:\n  Pattern identification",
           "PCA:\n  Dimensionality check"],
          c_ml, b_ml)

# 4. Action & Advisory Layer
draw_card(8.4, 1.5, 2.2, 4.2, "Smart Advisory",
          ["Peak load shaving", "HVAC schedule advice", "Hostel benchmarking", "Energy savings (kWh)", "Cost cut alerts"],
          c_action, b_action)

# Arrows
draw_conn(2.7, 3.6, 3.1, 3.6, "Meter Readings")
draw_conn(5.3, 3.6, 5.7, 3.6, "Data Feed")
draw_conn(8.0, 3.6, 8.4, 3.6, "Actionable Insights")

# Overall title
ax.text(5.5, 6.6, "Smart Hostel Energy Advisor: Conceptual Architecture",
        ha="center", va="center", fontsize=14, fontweight="bold", color="#1E3A5F")

plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, "conceptual_architecture.png"), dpi=200, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved conceptual_architecture.png")
