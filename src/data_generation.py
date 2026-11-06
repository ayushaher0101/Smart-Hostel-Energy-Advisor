"""
Smart Hostel Energy Advisor — Synthetic Dataset Generation
===========================================================
Generates realistic synthetic electricity consumption data for 5 university
hostels over 365 days (1 full year).

Assumptions (documented for academic transparency):
- 5 hostels with different capacities typical of a mid-size Indian university.
- Temperature follows a sinusoidal pattern modelling Ahmedabad's climate
  (PDEU location): hot summers (~40°C), mild winters (~15°C).
- AC usage increases sharply when temperature exceeds ~28°C.
- Weekend occupancy is slightly lower (some students go home).
- Energy consumption is a function of occupants, temperature, AC usage,
  lighting, and appliance count, with added random noise (~10-15%).

THIS IS A SYNTHETIC DATASET — NOT ACTUAL UNIVERSITY DATA.
"""

import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta

# ─── Reproducibility ───────────────────────────────────────────────
np.random.seed(42)

# ─── Project paths ─────────────────────────────────────────────────
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(PROJECT_DIR, "dataset")
os.makedirs(DATASET_DIR, exist_ok=True)

# ─── Hostel Configuration ──────────────────────────────────────────
# Each hostel has a unique capacity and a base power factor that
# represents differences in infrastructure (older vs newer buildings,
# different appliance efficiency, etc.)
HOSTELS = {
    "H1": {"capacity": 120, "base_power_factor": 1.00},
    "H2": {"capacity": 150, "base_power_factor": 1.05},
    "H3": {"capacity": 200, "base_power_factor": 0.95},
    "H4": {"capacity": 250, "base_power_factor": 1.10},
    "H5": {"capacity": 300, "base_power_factor": 0.98},
}

# ─── Date range: 1 year ────────────────────────────────────────────
START_DATE = datetime(2025, 1, 1)
NUM_DAYS = 365

def generate_temperature(day_of_year: int) -> float:
    """
    Simulate daily average temperature for Ahmedabad climate.

    Uses a sinusoidal model:
        T = mean_temp + amplitude * sin(2π * (day - phase_shift) / 365)

    Ahmedabad: mean ~28°C, amplitude ~10°C, peak around day 150 (late May).
    Random noise of ±2°C added for realism.
    """
    mean_temp = 28.0
    amplitude = 10.0
    phase_shift = 80  # peak heat around late May (day ~150)
    temp = mean_temp + amplitude * np.sin(2 * np.pi * (day_of_year - phase_shift) / 365)
    noise = np.random.normal(0, 2.0)
    return round(max(12.0, min(45.0, temp + noise)), 1)


def generate_occupancy(capacity: int, is_weekend: bool, month: int) -> int:
    """
    Simulate daily hostel occupancy.

    - Weekdays: 85-95% occupancy
    - Weekends: 65-80% occupancy (some students go home)
    - Exam months (March, April, October, November): +5% occupancy
    - Summer vacation (May-June): 30-50% occupancy
    """
    if month in [5, 6]:  # summer vacation — many students leave
        rate = np.random.uniform(0.30, 0.50)
    elif is_weekend:
        rate = np.random.uniform(0.65, 0.80)
    elif month in [3, 4, 10, 11]:  # exam period — more students stay
        rate = np.random.uniform(0.88, 0.97)
    else:
        rate = np.random.uniform(0.82, 0.95)

    return int(capacity * rate)


def generate_ac_usage(temperature: float, occupants: int, capacity: int) -> float:
    """
    Simulate AC usage hours based on temperature and occupancy.

    Logic:
    - Below 22°C: almost no AC (0-1 hours)
    - 22-28°C: moderate usage (1-5 hours)
    - 28-35°C: heavy usage (5-12 hours)
    - Above 35°C: very heavy usage (10-18 hours)

    Scaled by occupancy ratio (fewer people → fewer ACs running).
    """
    occupancy_ratio = occupants / capacity

    if temperature < 22:
        base_hours = np.random.uniform(0, 1.0)
    elif temperature < 28:
        base_hours = np.random.uniform(1.0, 5.0)
    elif temperature < 35:
        base_hours = np.random.uniform(5.0, 12.0)
    else:
        base_hours = np.random.uniform(10.0, 18.0)

    return round(base_hours * occupancy_ratio, 1)


def generate_lighting_hours(month: int, is_weekend: bool) -> float:
    """
    Simulate daily lighting usage hours.

    - Winter months (Nov-Feb): longer nights → 10-14 hours of lighting
    - Summer months (Apr-Jul): shorter nights → 7-10 hours
    - Other months: 8-12 hours
    - Weekends: slightly less usage (common areas less active)
    """
    if month in [11, 12, 1, 2]:
        base = np.random.uniform(10.0, 14.0)
    elif month in [4, 5, 6, 7]:
        base = np.random.uniform(7.0, 10.0)
    else:
        base = np.random.uniform(8.0, 12.0)

    if is_weekend:
        base *= np.random.uniform(0.85, 0.95)

    return round(base, 1)


def generate_appliance_count(occupants: int) -> int:
    """
    Simulate active appliance count.

    Assumes roughly 0.8-1.2 active appliances per occupant
    (phones charging, laptops, fans, water heaters, etc.)
    Plus a base of 10-20 common-area appliances (washing machines,
    corridor lights, water pumps).
    """
    personal = int(occupants * np.random.uniform(0.8, 1.2))
    common = np.random.randint(10, 21)
    return personal + common


def calculate_energy(occupants, temperature, ac_usage_hours,
                     lighting_hours, appliance_count, base_power_factor):
    """
    Calculate daily energy consumption (kWh) using a realistic model.

    Energy = base_power_factor * (
        occupant_contribution   +
        ac_contribution         +
        lighting_contribution   +
        appliance_contribution  +
        temperature_premium     +
        random_noise
    )

    This is intentionally NOT a simple linear formula to ensure
    the ML models have something meaningful to learn while not
    being trivially perfect.
    """
    # Base load per occupant (lighting, fans, common area share)
    occupant_energy = 0.45 * occupants

    # AC is the biggest power consumer
    ac_energy = 1.8 * ac_usage_hours + 0.05 * ac_usage_hours ** 1.3

    # Lighting contribution
    lighting_energy = 0.35 * lighting_hours

    # Appliance contribution (diminishing returns at scale)
    appliance_energy = 0.12 * appliance_count + 0.001 * appliance_count ** 1.2

    # Extra cooling/heating load when temperature is extreme
    if temperature > 35:
        temp_premium = 2.5 * (temperature - 35)
    elif temperature < 18:
        temp_premium = 1.5 * (18 - temperature)
    else:
        temp_premium = 0.0

    subtotal = (occupant_energy + ac_energy + lighting_energy +
                appliance_energy + temp_premium)

    # Apply hostel-specific factor and add noise (±10-15%)
    noise_factor = np.random.normal(1.0, 0.12)
    noise_factor = max(0.75, min(1.25, noise_factor))  # clamp

    energy = base_power_factor * subtotal * noise_factor
    return round(max(10.0, energy), 2)  # floor at 10 kWh


def generate_dataset():
    """Generate the full synthetic dataset and save to CSV."""
    records = []

    for hostel_id, config in HOSTELS.items():
        capacity = config["capacity"]
        base_pf = config["base_power_factor"]

        for day_offset in range(NUM_DAYS):
            date = START_DATE + timedelta(days=day_offset)
            day_of_year = date.timetuple().tm_yday
            month = date.month
            day_of_week = date.weekday()  # 0=Monday, 6=Sunday
            is_weekend = 1 if day_of_week >= 5 else 0

            temperature = generate_temperature(day_of_year)
            occupants = generate_occupancy(capacity, bool(is_weekend), month)
            ac_usage = generate_ac_usage(temperature, occupants, capacity)
            lighting = generate_lighting_hours(month, bool(is_weekend))
            appliances = generate_appliance_count(occupants)

            energy = calculate_energy(
                occupants, temperature, ac_usage,
                lighting, appliances, base_pf
            )

            records.append({
                "hostel_id": hostel_id,
                "date": date.strftime("%Y-%m-%d"),
                "month": month,
                "day_of_week": day_of_week,
                "is_weekend": is_weekend,
                "occupants": occupants,
                "temperature_c": temperature,
                "ac_usage_hours": ac_usage,
                "lighting_hours": lighting,
                "appliance_count": appliances,
                "daily_energy_kwh": energy,
            })

    df = pd.DataFrame(records)

    # Save raw dataset
    raw_path = os.path.join(DATASET_DIR, "raw_dataset.csv")
    df.to_csv(raw_path, index=False)
    print(f"✓ Raw dataset saved: {raw_path}")
    print(f"  Shape: {df.shape}")
    print(f"  Columns: {list(df.columns)}")
    print(f"\nFirst 5 rows:")
    print(df.head().to_string(index=False))
    print(f"\nBasic statistics:")
    print(df.describe().round(2).to_string())

    return df


if __name__ == "__main__":
    df = generate_dataset()
