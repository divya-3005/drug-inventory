# Drug Inventory and Supply Chain Management System

A Python-based command-line interface (CLI) application for monitoring and auditing pharmaceutical distribution across regional warehouses and healthcare facilities.

---

## Overview

Public health drug distribution networks frequently encounter stockouts, avoidable medication expiration, and audit discrepancies due to decentralized records. This application provides a unified tracking system that manages the pharmaceutical lifecycle from warehouse intake to hospital consumption, incorporating automated threshold alerts, manual adjustments, and an immutable transaction log.

---

## Core Capabilities

- **Catalog Management**: Register and track medicines with standardized generic names, dosages, units, expiration dates, and safety buffer thresholds.
- **Multi-Echelon Facility Support**: Model independent storage facilities (warehouses) and dispensing endpoints (hospitals and clinics).
- **Two-Tier Inventory Ledger**: Separate balance tracking for warehouse stockpiles and hospital floor stock.
- **Inter-Facility Distribution**: Atomic transfer logic that decrements dispatching warehouse stock and increments receiving hospital stock.
- **Consumption Logging**: Real-time recording of hospital dispensing to prevent discrepancies between theoretical and physical counts.
- **Multi-Level Threshold & Expiration Alerts**:
  - **Low Stock**: Triggers when facility inventory meets or falls below defined safety levels.
  - **Expiring Soon**: Flags lots expiring within 30 days.
  - **Expired**: Flags lots that have surpassed their expiration date.
- **Audited Stock Adjustments**: Record inventory modifications (e.g., damaged goods, physical count reconciliations) with mandatory justification strings.
- **End-to-End Movement History**: Every state-changing transaction (`ADD`, `DISTRIBUTE`, `RECEIVE`, `CONSUME`, `ADJUST`) is logged with timestamps, facility identifiers, signed quantities, and audit notes.
- **System Dashboard**: Centralized summary of active catalog entities, facility counts, total stock records, and categorized alert totals.
- **Flat-File JSON Persistence**: Zero-dependency database layer using structured JSON files.

---

## Architecture and Data Flow

```text
               +-----------------------+
               |   Medicine Registry   |
               +-----------+-----------+
                           |
                           v
               +-----------------------+
               | Warehouse Intake (ADD)|
               +-----------+-----------+
                           |
                           v
               +-----------------------+
               | Distribution Transfer |
               | (WH: -Qty / Hosp: +Qty|
               +-----------+-----------+
                           |
                           v
               +-----------------------+
               | Hospital Consumption  |
               | (Hosp: -Qty)          |
               +-----------+-----------+
                           |
             +-------------+-------------+
             |                           |
             v                           v
+------------------------+   +-----------------------+
| Real-time Alerts Engine|   | Operational Dashboard |
+------------------------+   +-----------------------+
             |                           |
             +-------------+-------------+
                           |
                           v
             +---------------------------+
             | Transaction Audit History |
             |   (stock_movements.json)  |
             +---------------------------+
```

---

## Project Structure

```text
drug-inventory/
├── main.py                      # Application entry point, CLI interface, and business logic
├── README.md                    # Technical documentation
├── .gitignore                   # Version control exclusion rules
└── data/                        # File-based persistence layer
    ├── medicines.json           # Catalog of registered pharmaceutical items
    ├── warehouses.json          # Warehouse facility records
    ├── hospitals.json           # Hospital and healthcare center records
    ├── inventory.json           # Warehouse inventory levels
    ├── hospital_inventory.json  # Hospital inventory levels
    └── stock_movements.json     # Append-only transaction audit log
```

---

## Technical Specifications

- **Runtime**: Python 3.7+
- **External Dependencies**: None (Standard Library only: `json`, `datetime`)
- **Storage Format**: Indented JSON flat files

---

## Installation and Execution

### Prerequisites

Verify that Python 3 is installed on your workstation:

```bash
python3 --version
```

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/divya-3005/drug-inventory.git
   cd drug-inventory
   ```

2. Launch the application:
   ```bash
   python3 main.py
   ```

---

## Command Reference

The interactive CLI provides the following operational commands:

| Command | Function | Description |
| :--- | :--- | :--- |
| `1` | **Add Medicine** | Register a new drug entry with name, strength, unit, expiry, and minimum threshold |
| `2` | **View Medicines** | Display the full catalog of registered pharmaceuticals |
| `3` | **Add Warehouse** | Register a primary supply storage facility |
| `4` | **View Warehouses** | List registered warehouse locations |
| `5` | **Add Hospital** | Register a healthcare dispensing facility |
| `6` | **View Hospitals** | List registered hospital locations |
| `7` | **Add Stock** | Record an incoming shipment into a specific warehouse |
| `8` | **View Warehouse Inventory** | Formatted tabular view of warehouse stock levels and thresholds |
| `9` | **View Hospital Inventory** | Formatted tabular view of hospital stock levels and thresholds |
| `10` | **Distribute Medicine** | Transfer stock from a warehouse to a hospital |
| `11` | **Record Consumption** | Deduct dispensed medication from hospital stock |
| `12` | **View Alerts** | Display low-stock warnings and expiring/expired medications |
| `13` | **Dashboard** | Display high-level system metrics and alert counters |
| `14` | **Adjust Stock** | Apply manual stock revisions (+/-) with required justification |
| `15` | **View Stock History** | Display chronological audit trail of all inventory transactions |
| `0` | **Exit** | Terminate the application session safely |

---

## Validation and Integrity Controls

To protect against state corruption, the application enforces the following runtime checks:

- **Type Safety**: Rejects non-numeric values for identifiers, counts, and quantities.
- **Positive Bounds**: Rejects inputs `<= 0` during stock intake, distribution, and consumption.
- **Foreign Key Verification**: Confirms warehouse, hospital, and medicine IDs exist in memory before proceeding.
- **Date Compliance**: Strict ISO-style format checking (`YYYY-MM-DD`) via `datetime.strptime`.
- **Transfer Solvency**: Prevents distributions that exceed available warehouse balance.
- **Dispensation Solvency**: Prevents consumption exceeding current hospital balance.
- **Non-Negative Invariants**: Rejects manual stock adjustments that would result in negative balances.
- **Mandatory Audit Trail**: Requires a non-empty reason string for every manual inventory adjustment.

---

## Verification and Testing

The current implementation has been validated against an end-to-end integration test suite:

1. **Intake**: Stocking 500 units into central storage.
2. **Transfer**: Distributing 100 units to a district clinic (Warehouse: 400, Clinic: 100).
3. **Dispensation**: Consuming 60 units (Clinic: 40, triggering low-stock alert against a 50-unit threshold).
4. **Adjustment**: Reconciling warehouse stock by -20 units with reason "Damaged stock" (Warehouse: 380).
5. **Audit Verification**: Validating all entries (`ADD`, `DISTRIBUTE`, `RECEIVE`, `CONSUME`, `ADJUST`) in `stock_movements.json`.
6. **Persistence Recovery**: Restarting runtime and confirming state recovery from flat-file storage.

---

## Development Roadmap

Planned capabilities for subsequent development phases:

- **Phase 2 — Procurement Lifecycle**: Integration of vendor registries, purchase order generation, and receiving workflows.
- **Phase 3 — Batch & Lot Tracking**: Lot-level granularity allowing multiple expiration dates and serial numbers per product SKU.
- **Phase 4 — Persistence Migration**: Transition from JSON flat files to a relational database backend (SQLite / PostgreSQL) for atomic multi-user transactions.
- **Phase 5 — Web Service & Interface**: RESTful API endpoints (FastAPI) coupled with a web-based dashboard interface.
