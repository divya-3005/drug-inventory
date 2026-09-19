"""
Seed script to initialize realistic demonstration data for the Drug Inventory System.
Run with: python3 seed_data.py
"""

import json
import os
from datetime import date, timedelta


def seed_database():
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)

    today = date.today()
    exp_soon = (today + timedelta(days=15)).strftime("%Y-%m-%d")
    exp_expired = (today - timedelta(days=10)).strftime("%Y-%m-%d")
    exp_safe_1 = (today + timedelta(days=365)).strftime("%Y-%m-%d")
    exp_safe_2 = (today + timedelta(days=500)).strftime("%Y-%m-%d")
    exp_safe_3 = (today + timedelta(days=700)).strftime("%Y-%m-%d")

    medicines = [
        {
            "id": 1,
            "name": "Paracetamol",
            "strength": "500mg",
            "unit": "tablets",
            "expiry_date": exp_safe_1,
            "minimum_stock": 100
        },
        {
            "id": 2,
            "name": "Amoxicillin",
            "strength": "250mg",
            "unit": "capsules",
            "expiry_date": exp_soon,
            "minimum_stock": 50
        },
        {
            "id": 3,
            "name": "Metformin",
            "strength": "500mg",
            "unit": "tablets",
            "expiry_date": exp_safe_2,
            "minimum_stock": 40
        },
        {
            "id": 4,
            "name": "Ibuprofen",
            "strength": "400mg",
            "unit": "tablets",
            "expiry_date": exp_safe_3,
            "minimum_stock": 60
        },
        {
            "id": 5,
            "name": "Azithromycin",
            "strength": "500mg",
            "unit": "tablets",
            "expiry_date": exp_expired,
            "minimum_stock": 30
        }
    ]

    warehouses = [
        {
            "id": 1,
            "name": "Central Medical Depot",
            "location": "New Delhi"
        },
        {
            "id": 2,
            "name": "Northern Regional Warehouse",
            "location": "Chandigarh"
        }
    ]

    hospitals = [
        {
            "id": 1,
            "name": "City General Hospital",
            "location": "New Delhi"
        },
        {
            "id": 2,
            "name": "District Care Clinic",
            "location": "Chandigarh"
        }
    ]

    inventory = [
        {"warehouse_id": 1, "medicine_id": 1, "quantity": 1000},
        {"warehouse_id": 1, "medicine_id": 2, "quantity": 300},
        {"warehouse_id": 1, "medicine_id": 3, "quantity": 500},
        {"warehouse_id": 2, "medicine_id": 4, "quantity": 400},
        {"warehouse_id": 2, "medicine_id": 5, "quantity": 50}
    ]

    hospital_inventory = [
        {"hospital_id": 1, "medicine_id": 1, "quantity": 250},
        {"hospital_id": 1, "medicine_id": 2, "quantity": 20},  # Low stock (20 <= 50)
        {"hospital_id": 2, "medicine_id": 3, "quantity": 15}   # Low stock (15 <= 40)
    ]

    stock_movements = [
        {
            "medicine_id": 1,
            "location_type": "warehouse",
            "location_id": 1,
            "movement_type": "ADD",
            "quantity": 1250,
            "reason": "Initial procurement intake",
            "date": (today - timedelta(days=5)).strftime("%Y-%m-%d 09:30:00")
        },
        {
            "medicine_id": 1,
            "location_type": "warehouse",
            "location_id": 1,
            "movement_type": "DISTRIBUTE",
            "quantity": -250,
            "reason": "Distributed to hospital 1",
            "date": (today - timedelta(days=4)).strftime("%Y-%m-%d 11:15:00")
        },
        {
            "medicine_id": 1,
            "location_type": "hospital",
            "location_id": 1,
            "movement_type": "RECEIVE",
            "quantity": 250,
            "reason": "Received from warehouse 1",
            "date": (today - timedelta(days=4)).strftime("%Y-%m-%d 11:15:00")
        },
        {
            "medicine_id": 2,
            "location_type": "warehouse",
            "location_id": 1,
            "movement_type": "ADD",
            "quantity": 400,
            "reason": "Initial procurement intake",
            "date": (today - timedelta(days=3)).strftime("%Y-%m-%d 10:00:00")
        },
        {
            "medicine_id": 2,
            "location_type": "warehouse",
            "location_id": 1,
            "movement_type": "DISTRIBUTE",
            "quantity": -100,
            "reason": "Distributed to hospital 1",
            "date": (today - timedelta(days=2)).strftime("%Y-%m-%d 14:00:00")
        },
        {
            "medicine_id": 2,
            "location_type": "hospital",
            "location_id": 1,
            "movement_type": "RECEIVE",
            "quantity": 100,
            "reason": "Received from warehouse 1",
            "date": (today - timedelta(days=2)).strftime("%Y-%m-%d 14:00:00")
        },
        {
            "medicine_id": 2,
            "location_type": "hospital",
            "location_id": 1,
            "movement_type": "CONSUME",
            "quantity": -80,
            "reason": "Outpatient dispensary consumption",
            "date": (today - timedelta(days=1)).strftime("%Y-%m-%d 16:30:00")
        }
    ]

    files = {
        "medicines.json": medicines,
        "warehouses.json": warehouses,
        "hospitals.json": hospitals,
        "inventory.json": inventory,
        "hospital_inventory.json": hospital_inventory,
        "stock_movements.json": stock_movements
    }

    for filename, data in files.items():
        filepath = os.path.join(data_dir, filename)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        print(f"✅ Populated {filepath} ({len(data)} records)")

    print("\n🎉 Seed data successfully initialized!")


if __name__ == "__main__":
    seed_database()
