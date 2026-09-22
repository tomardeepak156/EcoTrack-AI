import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FACTORS_FILE = BASE_DIR / "emission_factors.json"

with open(FACTORS_FILE, "r", encoding="utf-8") as file:
    EMISSION_FACTORS = json.load(file)

ACTIVITY_TYPES = {
    "car": "Car",
    "bus": "Bus",
    "flight": "Flight",
    "electricity": "Electricity",
    "veg_meal": "Veg Meal",
    "non_veg_meal": "Non-Veg Meal",
}


def calculate_activity(activity_type, quantity):
    """
    Calculate CO2e for a logged activity.

    Activity Logger values must be greater than zero.
    """
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")

    factors = {
        "car": EMISSION_FACTORS["transport"]["car"]["factor"],
        "bus": EMISSION_FACTORS["transport"]["bus"]["factor"],
        "flight": EMISSION_FACTORS["transport"]["flight"]["factor"],
        "electricity": EMISSION_FACTORS["electricity"]["grid"]["factor"],
        "veg_meal": EMISSION_FACTORS["food"]["veg_meal"]["factor"],
        "non_veg_meal": EMISSION_FACTORS["food"]["non_veg_meal"]["factor"],
    }

    if activity_type not in factors:
        raise ValueError(f"Unknown activity type: {activity_type}")

    return quantity * factors[activity_type]


def get_activity_unit(activity_type):
    if activity_type in {"car", "bus", "flight"}:
        return "km"
    if activity_type == "electricity":
        return "kWh"
    return "meal"


def calculate_transport(distance_km, vehicle):
    """
    Legacy dashboard transport calculation.

    Zero distance is allowed because the dashboard uses zero
    to mean that no transport was entered for the day.
    """
    if distance_km == 0:
        return 0.0

    if distance_km < 0:
        raise ValueError("Distance cannot be negative.")

    mapping = {
        "car_petrol": "car",
        "car_diesel": "car",
        "motorcycle": "car",
        "bus": "bus",
        "train": "bus",
    }

    activity_type = mapping.get(vehicle, vehicle)

    return calculate_activity(activity_type, distance_km)


def calculate_electricity(kwh):
    """
    Legacy dashboard electricity calculation.

    Zero electricity is allowed because the dashboard uses zero
    to mean that no electricity consumption was entered.
    """
    if kwh == 0:
        return 0.0

    if kwh < 0:
        raise ValueError("Electricity consumption cannot be negative.")

    return calculate_activity("electricity", kwh)


def calculate_total(
    transport=0,
    electricity=0,
    food=0,
    flight=0,
    shopping=0,
    waste=0
):
    values = [
        transport,
        electricity,
        food,
        flight,
        shopping,
        waste
    ]

    if any(value < 0 for value in values):
        raise ValueError("Carbon values cannot be negative.")

    return sum(values)


def calculate_breakdown(
    transport=0,
    electricity=0,
    food=0,
    flight=0,
    shopping=0,
    waste=0
):
    breakdown = {
        "Transport": transport,
        "Electricity": electricity,
        "Food": food,
        "Flight": flight,
        "Shopping": shopping,
        "Waste": waste
    }

    breakdown["Total"] = sum(breakdown.values())

    return breakdown
