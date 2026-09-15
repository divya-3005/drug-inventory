# Drug Inventory & Supply Chain Tracking System (CLI MVP v1)

A command-line drug inventory and supply chain tracking application built in Python. It manages pharmaceutical stock across central warehouses and healthcare facilities, provides proactive alerts for low stock and expiring medicines, and maintains a complete audit trail of every stock movement.

---

## 📌 Problem Statement

In public health networks and hospital supply chains, manual or disjointed inventory management leads to critical challenges:
- **Stockouts:** Hospitals run out of essential life-saving drugs due to lack of visibility into consumption patterns.
- **Medicine Expiry & Wastage:** Drugs expire on shelves before distribution because expiry dates are not systematically monitored.
- **Traceability Gaps:** Difficulties in auditing where medicines were received, where they were distributed, or why quantities changed (e.g., damaged or expired batches).

This system provides a centralized, transparent workflow connecting warehouses, hospitals, stock allocations, patient consumption, and automated alerts.

---

## 🚀 Current Features

* **Medicine Directory:** Register and browse medicines with generic names, strength, dispensing unit, expiry date, and minimum stock thresholds.
* **Facilities Management:** Maintain lists of central supply warehouses and local hospitals/clinics.
* **Warehouse Stock Intake:** Add stock batches directly to warehouse inventory.
* **Inter-Facility Distribution:** Safely transfer stock from a warehouse to a hospital, automatically deducting from the warehouse and crediting the hospital.
* **Hospital Consumption Tracking:** Record patient dispensing and usage, automatically deducting from hospital inventory.
* **Categorized Alerts:**
  - 🟡 **LOW STOCK:** Identifies when warehouse or hospital stock falls to or below a medicine's minimum threshold.
  - 🟠 **EXPIRING SOON:** Flags medications expiring within the next 30 days.
  - 🔴 **EXPIRED:** Flags medications that have passed their expiration date.
* **Executive Dashboard:** Displays instant metrics on total medicines, facilities, inventory records, and active alert counts.
* **Manual Stock Adjustment:** Account for damaged goods, physical count discrepancies, or losses with mandatory audit reasons.
* **Stock Movement Audit Trail:** Automatically logs every transaction (`ADD`, `DISTRIBUTE`, `RECEIVE`, `CONSUME`, `ADJUST`) with timestamp, location, signed quantity, and reason.
* **JSON Data Persistence:** Automatically saves all entities, stock levels, and audit logs to persistent JSON files.

---

## 🧠 How the Application Works

The system operates across a linear, traceable supply chain lifecycle:

```text
               ┌──────────────────────────────┐
               │    1. Add Medicine Entry     │
               └──────────────┬───────────────┘
                              │
               ┌──────────────▼───────────────┐
               │  2. Add Warehouse & Hospital │
               └──────────────┬───────────────┘
                              │
               ┌──────────────▼───────────────┐
               │   3. Add Warehouse Stock     │ (ADD: +Qty to Warehouse)
               └──────────────┬───────────────┘
                              │
               ┌──────────────▼───────────────┐
               │ 4. Distribute to Hospital    │ (DISTRIBUTE: -Qty from WH)
               └──────────────┬───────────────┘ (RECEIVE: +Qty to Hosp)
                              │
               ┌──────────────▼───────────────┐
               │  5. Record Consumption      │ (CONSUME: -Qty from Hosp)
               └──────────────┬───────────────┘
                              │
               ┌──────────────▼───────────────┐
               │ 6. Proactive Alerts / Dash   │ (Checks min_stock & expiry)
               └──────────────┬───────────────┘
                              │
               ┌──────────────▼───────────────┐
               │  7. Audited Adjustments      │ (ADJUST: +/-Qty with Reason)
               └──────────────────────────────┘
                              │
            Recorded in Stock Movement History
```

---

## 📁 Project Structure

```text
drug-inventory/
├── main.py                      # Main application logic, CLI menu, and controllers
├── README.md                    # Project documentation
├── .gitignore                   # Git ignore configuration
└── data/                        # JSON storage directory (database layer)
    ├── medicines.json           # Catalog of registered medicines
    ├── warehouses.json          # Registered warehouse facilities
    ├── hospitals.json           # Registered hospital/clinic facilities
    ├── inventory.json           # Warehouse stock records
    ├── hospital_inventory.json  # Hospital stock records
    └── stock_movements.json     # Complete transaction audit logs
```

---

## 🛠️ Technologies Used

- **Language:** Python 3 (Python 3.7+)
- **Standard Libraries:**
  - `json` — Serialization and persistent file storage
  - `datetime` (`date`, `datetime`, `timedelta`) — Date parsing, arithmetic for expiry calculations, and ISO-style timestamps
- **External Dependencies:** None (zero external packages required; runs natively on pure Python)

---

## 📋 Prerequisites & Installation

### Requirements
- Python 3.7 or higher installed on your computer.

Check your Python version by opening a terminal and running:
```bash
python3 --version
```

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/divya-3005/drug-inventory.git
   ```

2. **Navigate into the project directory:**
   ```bash
   cd drug-inventory
   ```

3. **Run the application:**
   ```bash
   python3 main.py
   ```

---

## 💻 Example Usage Walkthrough

When you start the application, the interactive menu appears:

```text
================================
      DRUG INVENTORY SYSTEM
================================
1. Add Medicine
2. View Medicines
3. Add Warehouse
4. View Warehouses
5. Add Hospital
6. View Hospitals
7. Add Stock
8. View Warehouse Inventory
9. View Hospital Inventory
10. Distribute Medicine
11. Record Consumption
12. View Alerts
13. Dashboard
14. Adjust Stock
15. View Stock History
0. Exit
================================
Enter your choice: 
```

### 1. Register a Medicine (Option 1)
```text
--- Add Medicine ---
Medicine name: Paracetamol
Strength: 500mg
Unit: tablets
Expiry date (YYYY-MM-DD): 2027-12-31
Minimum stock: 50

Medicine added successfully!
```

### 2. View Warehouse Inventory (Option 8)
```text
--- Warehouse Inventory ---

---------------------------------------------------------------------------
Warehouse           Medicine                 Quantity    Status         
---------------------------------------------------------------------------
Central Warehouse   Paracetamol 500mg        500         OK             
---------------------------------------------------------------------------
```

### 3. Check Alerts (Option 12)
If hospital stock drops below the minimum threshold (e.g. 40 tablets left when minimum is 50):
```text
--- Alerts ---

🟡 LOW STOCK
----------------------------------------
Location: District Hospital
Medicine: Paracetamol 500mg
Current stock: 40 tablets
Minimum stock: 50 tablets
```

### 4. Inspect Audit History (Option 15)
```text
--- Stock Movement History ---

------------------------------------------------------------
Date:       2026-09-15 11:45:56
Medicine:   Paracetamol 500mg
Location:   Central Warehouse
Type:       ADD
Quantity:   +500
Reason:     Initial stock

------------------------------------------------------------
Date:       2026-09-15 11:45:56
Medicine:   Paracetamol 500mg
Location:   Central Warehouse
Type:       DISTRIBUTE
Quantity:   -100
Reason:     Distributed to hospital 1

------------------------------------------------------------
Date:       2026-09-15 11:45:56
Medicine:   Paracetamol 500mg
Location:   District Hospital
Type:       RECEIVE
Quantity:   +100
Reason:     Received from warehouse 1

------------------------------------------------------------
Date:       2026-09-15 11:45:56
Medicine:   Paracetamol 500mg
Location:   District Hospital
Type:       CONSUME
Quantity:   -60
Reason:     Medicine consumed

------------------------------------------------------------
Date:       2026-09-15 11:45:56
Medicine:   Paracetamol 500mg
Location:   Central Warehouse
Type:       ADJUST
Quantity:   -20
Reason:     Damaged stock
------------------------------------------------------------
```

---

## 🛡️ Validation and Error Handling

The application enforces data integrity to prevent silent corruption or crashes:

| Validation Rule | Behavior / Message |
| :--- | :--- |
| **Non-Numeric Numbers** | Entering letters or symbols for stock, quantity, or IDs prompts: `❌ Please enter a valid number.` |
| **Negative or Zero Values** | Stock intake, distribution, and consumption require integers > 0 (`❌ Please enter a number greater than 0.`). |
| **Invalid Warehouse / Hospital ID** | Entering an ID not present in memory prompts: `❌ Invalid warehouse.` or `❌ Invalid hospital.` |
| **Invalid Medicine ID** | Entering an unregistered medicine ID prompts: `❌ Invalid medicine.` |
| **Expiry Date Formatting** | Validates strict `YYYY-MM-DD` compliance via `datetime.strptime()` (`❌ Invalid date. Please use YYYY-MM-DD.`). |
| **Insufficient Stock Transfers** | Rejects distributions greater than available warehouse stock (`❌ Insufficient stock!`). |
| **Insufficient Consumption** | Rejects consumption greater than available hospital stock (`❌ Insufficient hospital stock!`). |
| **Negative Inventory from Adjustments** | Adjustments that would drive quantity below 0 are rejected (`❌ Stock cannot become negative.`). |
| **Zero Adjustments** | Rejects zero quantity adjustment (`❌ Adjustment cannot be zero.`). |
| **Empty Adjustment Reason** | Enforces an audit justification string (`❌ Reason cannot be empty.`). |

---

## ✅ Current Status (Completed in CLI MVP v1)

- [x] Full CRUD-style viewing and adding for medicines, warehouses, and hospitals.
- [x] Inflow, distribution, and consumption workflows with quantity validation.
- [x] Two-level stock holding (warehouses and hospitals).
- [x] Formatted table displays for warehouse and hospital inventory.
- [x] Multi-category alert engine (low stock, expiring soon in 30 days, expired).
- [x] Executive dashboard with alert rollup counters.
- [x] Stock adjustments (+/-) with mandatory reasoning.
- [x] Complete append-only audit trail logging in `stock_movements.json`.
- [x] Persistent storage across application restarts using JSON.

---

## 🔮 Possible Future Improvements (Phase 2 & Beyond)

* **Vendor & Procurement Management:** Add vendor profiles, purchase orders (PO), and incoming shipments received into warehouses.
* **Batch / Lot & Serial Tracking:** Support distinct batch numbers, manufactured dates, and batch-specific expiry dates for the same medicine.
* **Relational Database Backend:** Transition from JSON flat files to SQLite or PostgreSQL for concurrency and relational queries.
* **Role-Based Access Control (RBAC):** Authenticated logins for Warehouse Managers, Hospital Pharmacists, and State Administrators.
* **REST API & Web Interface:** Expose endpoints using FastAPI / Flask and build a responsive web dashboard (React / Next.js).
* **Demand Forecasting & Automated Re-ordering:** Predictive analysis based on consumption velocity to suggest order quantities before stockouts happen.
