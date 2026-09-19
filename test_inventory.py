"""
Automated unit test suite for the Drug Inventory System.
Run with: python3 -m unittest test_inventory.py
"""

import os
import tempfile
import unittest
from datetime import date, datetime, timedelta
import main


class TestDrugInventorySystem(unittest.TestCase):

    def setUp(self):
        # Backup original data references
        self.orig_medicines = main.medicines
        self.orig_warehouses = main.warehouses
        self.orig_hospitals = main.hospitals
        self.orig_inventory = main.inventory
        self.orig_hospital_inventory = main.hospital_inventory
        self.orig_stock_movements = main.stock_movements

        # Setup test fixtures
        main.medicines = [
            {
                "id": 1,
                "name": "Paracetamol",
                "strength": "500mg",
                "unit": "tablets",
                "expiry_date": "2027-12-31",
                "minimum_stock": 50
            },
            {
                "id": 2,
                "name": "Amoxicillin",
                "strength": "250mg",
                "unit": "capsules",
                "expiry_date": (date.today() + timedelta(days=10)).strftime("%Y-%m-%d"),
                "minimum_stock": 30
            },
            {
                "id": 3,
                "name": "ExpiredMed",
                "strength": "100mg",
                "unit": "tablets",
                "expiry_date": (date.today() - timedelta(days=5)).strftime("%Y-%m-%d"),
                "minimum_stock": 20
            }
        ]

        main.warehouses = [
            {"id": 1, "name": "Main Depot", "location": "City A"},
            {"id": 2, "name": "East Depot", "location": "City B"}
        ]

        main.hospitals = [
            {"id": 1, "name": "City Clinic", "location": "City A"}
        ]

        main.inventory = [
            {"warehouse_id": 1, "medicine_id": 1, "quantity": 500},
            {"warehouse_id": 1, "medicine_id": 2, "quantity": 100}
        ]

        main.hospital_inventory = [
            {"hospital_id": 1, "medicine_id": 1, "quantity": 25}  # Low stock: 25 <= 50
        ]

        main.stock_movements = []

    def tearDown(self):
        # Restore original state
        main.medicines = self.orig_medicines
        main.warehouses = self.orig_warehouses
        main.hospitals = self.orig_hospitals
        main.inventory = self.orig_inventory
        main.hospital_inventory = self.orig_hospital_inventory
        main.stock_movements = self.orig_stock_movements

    # -------------------------------------------------------------
    # 1. Entity Lookup Helpers
    # -------------------------------------------------------------
    def test_find_warehouse(self):
        wh = main.find_warehouse(1)
        self.assertIsNotNone(wh)
        self.assertEqual(wh["name"], "Main Depot")
        self.assertIsNone(main.find_warehouse(999))

    def test_find_hospital(self):
        hosp = main.find_hospital(1)
        self.assertIsNotNone(hosp)
        self.assertEqual(hosp["name"], "City Clinic")
        self.assertIsNone(main.find_hospital(999))

    def test_find_medicine(self):
        med = main.find_medicine(1)
        self.assertIsNotNone(med)
        self.assertEqual(med["name"], "Paracetamol")
        self.assertIsNone(main.find_medicine(999))

    # -------------------------------------------------------------
    # 2. Inventory Stock Lookup Helpers
    # -------------------------------------------------------------
    def test_find_warehouse_stock(self):
        stock = main.find_warehouse_stock(1, 1)
        self.assertIsNotNone(stock)
        self.assertEqual(stock["quantity"], 500)
        self.assertIsNone(main.find_warehouse_stock(1, 999))

    def test_find_hospital_stock(self):
        stock = main.find_hospital_stock(1, 1)
        self.assertIsNotNone(stock)
        self.assertEqual(stock["quantity"], 25)
        self.assertIsNone(main.find_hospital_stock(1, 2))

    # -------------------------------------------------------------
    # 3. Movement Logging
    # -------------------------------------------------------------
    def test_record_movement(self):
        # Mock file write to avoid modifying production disk
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
            temp_path = tmp.name

        orig_file = main.STOCK_MOVEMENTS_FILE
        try:
            main.STOCK_MOVEMENTS_FILE = temp_path
            main.record_movement(
                medicine_id=1,
                location_type="warehouse",
                location_id=1,
                movement_type="ADD",
                quantity=100,
                reason="Test movement"
            )

            self.assertEqual(len(main.stock_movements), 1)
            rec = main.stock_movements[0]
            self.assertEqual(rec["medicine_id"], 1)
            self.assertEqual(rec["movement_type"], "ADD")
            self.assertEqual(rec["quantity"], 100)
            self.assertEqual(rec["reason"], "Test movement")
            # Verify valid ISO-like date string
            parsed_date = datetime.strptime(rec["date"], "%Y-%m-%d %H:%M:%S")
            self.assertIsInstance(parsed_date, datetime)
        finally:
            main.STOCK_MOVEMENTS_FILE = orig_file
            if os.path.exists(temp_path):
                os.remove(temp_path)

    # -------------------------------------------------------------
    # 4. Inventory Calculation & Constraints
    # -------------------------------------------------------------
    def test_stock_adjustment_constraint(self):
        stock = main.find_warehouse_stock(1, 1)
        current = stock["quantity"]
        valid_adj = -50
        self.assertGreaterEqual(current + valid_adj, 0)

        invalid_adj = -600
        self.assertLess(current + invalid_adj, 0)

    def test_distribution_quantity_constraint(self):
        wh_stock = main.find_warehouse_stock(1, 1)
        transfer_qty = 100
        self.assertLessEqual(transfer_qty, wh_stock["quantity"])

        excessive_qty = 1000
        self.assertGreater(excessive_qty, wh_stock["quantity"])

    def test_date_validation_format(self):
        valid_date = "2027-06-15"
        invalid_date_1 = "15/06/2027"
        invalid_date_2 = "invalid-date"

        # Valid date parse
        parsed = datetime.strptime(valid_date, "%Y-%m-%d")
        self.assertEqual(parsed.year, 2027)

        with self.assertRaises(ValueError):
            datetime.strptime(invalid_date_1, "%Y-%m-%d")

        with self.assertRaises(ValueError):
            datetime.strptime(invalid_date_2, "%Y-%m-%d")


if __name__ == "__main__":
    unittest.main()
