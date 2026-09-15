import json
from datetime import date, datetime, timedelta


MEDICINES_FILE = "data/medicines.json"
WAREHOUSES_FILE = "data/warehouses.json"
HOSPITALS_FILE = "data/hospitals.json"
INVENTORY_FILE = "data/inventory.json"
HOSPITAL_INVENTORY_FILE = "data/hospital_inventory.json"
STOCK_MOVEMENTS_FILE = "data/stock_movements.json"


def load_data(filename):
    with open(filename, "r") as file:
        return json.load(file)


def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


medicines = load_data(MEDICINES_FILE)
warehouses = load_data(WAREHOUSES_FILE)
hospitals = load_data(HOSPITALS_FILE)
inventory = load_data(INVENTORY_FILE)
hospital_inventory = load_data(HOSPITAL_INVENTORY_FILE)
stock_movements = load_data(STOCK_MOVEMENTS_FILE)


def get_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))

            if value <= 0:
                print("❌ Please enter a number greater than 0.")
                continue

            return value

        except ValueError:
            print("❌ Please enter a valid number.")


def get_valid_warehouse_id():
    while True:
        try:
            warehouse_id = int(input("Select warehouse: "))

            for warehouse in warehouses:
                if warehouse["id"] == warehouse_id:
                    return warehouse_id

            print("❌ Invalid warehouse.")

        except ValueError:
            print("❌ Please enter a valid number.")


def get_valid_hospital_id():
    while True:
        try:
            hospital_id = int(input("Select hospital: "))

            for hospital in hospitals:
                if hospital["id"] == hospital_id:
                    return hospital_id

            print("❌ Invalid hospital.")

        except ValueError:
            print("❌ Please enter a valid number.")


def get_valid_medicine_id():
    while True:
        try:
            medicine_id = int(input("Select medicine: "))

            for medicine in medicines:
                if medicine["id"] == medicine_id:
                    return medicine_id

            print("❌ Invalid medicine.")

        except ValueError:
            print("❌ Please enter a valid number.")


def find_warehouse(warehouse_id):
    for warehouse in warehouses:
        if warehouse["id"] == warehouse_id:
            return warehouse
    return None


def find_hospital(hospital_id):
    for hospital in hospitals:
        if hospital["id"] == hospital_id:
            return hospital
    return None


def find_medicine(medicine_id):
    for medicine in medicines:
        if medicine["id"] == medicine_id:
            return medicine
    return None


def find_warehouse_stock(warehouse_id, medicine_id):
    for stock in inventory:
        if (
            stock["warehouse_id"] == warehouse_id
            and stock["medicine_id"] == medicine_id
        ):
            return stock

    return None


def find_hospital_stock(hospital_id, medicine_id):
    for stock in hospital_inventory:
        if (
            stock["hospital_id"] == hospital_id
            and stock["medicine_id"] == medicine_id
        ):
            return stock

    return None


def record_movement(
    medicine_id,
    location_type,
    location_id,
    movement_type,
    quantity,
    reason=""
):
    movement = {
        "medicine_id": medicine_id,
        "location_type": location_type,
        "location_id": location_id,
        "movement_type": movement_type,
        "quantity": quantity,
        "reason": reason,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    stock_movements.append(movement)

    save_data(
        STOCK_MOVEMENTS_FILE,
        stock_movements
    )



def view_dashboard():
    print("\n========================================")
    print("              DASHBOARD")
    print("========================================")

    print(f"\nMedicines:        {len(medicines)}")
    print(f"Warehouses:       {len(warehouses)}")
    print(f"Hospitals:        {len(hospitals)}")

    print(f"\nWarehouse Stock:  {len(inventory)} records")
    print(f"Hospital Stock:   {len(hospital_inventory)} records")

    # -------------------------
    # COUNT ALERTS
    # -------------------------

    today = date.today()
    expiry_limit = today + timedelta(days=30)

    low_stock_count = 0
    expired_count = 0
    expiring_soon_count = 0

    # Warehouse low stock
    for stock in inventory:
        medicine = find_medicine(stock["medicine_id"])

        if medicine is None:
            continue

        if stock["quantity"] <= medicine["minimum_stock"]:
            low_stock_count += 1

    # Hospital low stock
    for stock in hospital_inventory:
        medicine = find_medicine(stock["medicine_id"])

        if medicine is None:
            continue

        if stock["quantity"] <= medicine["minimum_stock"]:
            low_stock_count += 1

    # Expiry alerts
    for medicine in medicines:
        expiry = datetime.strptime(
            medicine["expiry_date"],
            "%Y-%m-%d"
        ).date()

        if expiry < today:
            expired_count += 1

        elif expiry <= expiry_limit:
            expiring_soon_count += 1

    print("\n----------------------------------------")
    print("              ALERT SUMMARY")
    print("----------------------------------------")

    print(f"\n🔴 Expired:          {expired_count}")
    print(f"🟠 Expiring Soon:    {expiring_soon_count}")
    print(f"🟡 Low Stock:        {low_stock_count}")

    print("\n========================================")


def adjust_stock():
    print("\n--- Adjust Stock ---")

    if not warehouses:
        print("No warehouses found.")
        return

    if not medicines:
        print("No medicines found.")
        return

    if not inventory:
        print("No warehouse stock found.")
        return

    # Select warehouse
    print("\nWarehouses:")

    for warehouse in warehouses:
        print(f"{warehouse['id']}. {warehouse['name']}")

    warehouse_id = get_valid_warehouse_id()

    # Select medicine
    print("\nMedicines:")

    for medicine in medicines:
        print(
            f"{medicine['id']}. "
            f"{medicine['name']} {medicine['strength']}"
        )

    medicine_id = get_valid_medicine_id()

    # Find stock
    stock = find_warehouse_stock(
        warehouse_id,
        medicine_id
    )

    if stock is None:
        print("\n❌ This medicine is not available in this warehouse.")
        return

    print(f"\nCurrent stock: {stock['quantity']}")

    # Adjustment
    while True:
        try:
            adjustment = int(
                input("Adjustment quantity (+/-): ")
            )

            if adjustment == 0:
                print("❌ Adjustment cannot be zero.")
                continue

            new_quantity = stock["quantity"] + adjustment

            if new_quantity < 0:
                print("❌ Stock cannot become negative.")
                continue

            break

        except ValueError:
            print("❌ Please enter a valid number.")

    reason = input("Reason: ").strip()

    if not reason:
        print("❌ Reason cannot be empty.")
        return

    # Update stock
    stock["quantity"] = new_quantity

    save_data(INVENTORY_FILE, inventory)

    print("\n✅ Stock adjusted successfully!")
    print(f"Previous stock: {new_quantity - adjustment}")
    print(f"Adjustment: {adjustment:+}")
    print(f"New stock: {new_quantity}")
    print(f"Reason: {reason}")


def show_menu():
    print("\n================================")
    print("      DRUG INVENTORY SYSTEM")
    print("================================")
    print("1. Add Medicine")
    print("2. View Medicines")
    print("3. Add Warehouse")
    print("4. View Warehouses")
    print("5. Add Hospital")
    print("6. View Hospitals")
    print("7. Add Stock")
    print("8. View Warehouse Inventory")
    print("9. View Hospital Inventory")
    print("10. Distribute Medicine")
    print("11. Record Consumption")
    print("12. View Alerts")
    print("13. Dashboard")
    print("14. Adjust Stock")
    print("0. Exit")
    print("================================")

def pause():
    input("\nPress Enter to return to the menu...")

def add_medicine():
    print("\n--- Add Medicine ---")

    name = input("Medicine name: ")
    strength = input("Strength: ")
    unit = input("Unit: ")
    while True:
        expiry_date = input("Expiry date (YYYY-MM-DD): ")

        try:
            datetime.strptime(expiry_date, "%Y-%m-%d")
            break
        except ValueError:
            print("❌ Invalid date. Please use YYYY-MM-DD.")

    minimum_stock = get_positive_integer("Minimum stock: ")

    medicine = {
        "id": len(medicines) + 1,
        "name": name,
        "strength": strength,
        "unit": unit,
        "expiry_date": expiry_date,
        "minimum_stock": minimum_stock
    }

    medicines.append(medicine)

    save_data(MEDICINES_FILE, medicines)

    print("\nMedicine added successfully!")



def view_medicines():
    print("\n--- Medicines ---")

    if not medicines:
        print("No medicines found.")
        return

    for medicine in medicines:
        print(f"\nID: {medicine['id']}")
        print(f"Name: {medicine['name']}")
        print(f"Strength: {medicine['strength']}")
        print(f"Unit: {medicine['unit']}")
        print(f"Expiry: {medicine['expiry_date']}")
        print(f"Minimum stock: {medicine['minimum_stock']}")

def add_warehouse():
    print("\n--- Add Warehouse ---")

    name = input("Warehouse name: ")
    location = input("Location: ")

    warehouse = {
        "id": len(warehouses) + 1,
        "name": name,
        "location": location
    }

    warehouses.append(warehouse)

    save_data(WAREHOUSES_FILE, warehouses)

    print("\nWarehouse added successfully!")

def view_warehouses():
    print("\n--- Warehouses ---")

    if not warehouses:
        print("No warehouses found.")
        return

    for warehouse in warehouses:
        print(f"\nID: {warehouse['id']}")
        print(f"Name: {warehouse['name']}")
        print(f"Location: {warehouse['location']}")


def add_hospital():
    print("\n--- Add Hospital ---")

    name = input("Hospital name: ")
    location = input("Location: ")

    hospital = {
        "id": len(hospitals) + 1,
        "name": name,
        "location": location
    }

    hospitals.append(hospital)

    save_data(HOSPITALS_FILE, hospitals)

    print("\nHospital added successfully!")

def view_hospitals():
    print("\n--- Hospitals ---")

    if not hospitals:
        print("No hospitals found.")
        return

    for hospital in hospitals:
        print(f"\nID: {hospital['id']}")
        print(f"Name: {hospital['name']}")
        print(f"Location: {hospital['location']}")

def add_stock():
    print("\n--- Add Stock ---")

    if not warehouses:
        print("No warehouses found. Please add a warehouse first.")
        return

    if not medicines:
        print("No medicines found. Please add a medicine first.")
        return

    print("\nWarehouses:")

    for warehouse in warehouses:
        print(f"{warehouse['id']}. {warehouse['name']}")

    warehouse_id = get_valid_warehouse_id()

    print("\nMedicines:")

    for medicine in medicines:
        print(
            f"{medicine['id']}. "
            f"{medicine['name']} {medicine['strength']}"
        )

    medicine_id = get_valid_medicine_id()

    quantity = get_positive_integer("Quantity: ")

    stock = find_warehouse_stock(warehouse_id, medicine_id)

    if stock:
        stock["quantity"] += quantity

        save_data(
            INVENTORY_FILE,
            inventory
        )

        record_movement(
            medicine_id,
            "warehouse",
            warehouse_id,
            "ADD",
            quantity,
            "Stock added"
        )

        print("\nStock updated successfully!")
        return

    stock = {
        "warehouse_id": warehouse_id,
        "medicine_id": medicine_id,
        "quantity": quantity
    }

    inventory.append(stock)

    save_data(
        INVENTORY_FILE,
        inventory
    )

    record_movement(
        medicine_id,
        "warehouse",
        warehouse_id,
        "ADD",
        quantity,
        "Initial stock"
    )

    print("\nStock added successfully!")

def view_inventory():
    print("\n--- Warehouse Inventory ---")

    if not inventory:
        print("No inventory found.")
        return

    print("\n" + "-" * 75)
    print(
        f"{'Warehouse':<20}"
        f"{'Medicine':<25}"
        f"{'Quantity':<12}"
        f"{'Status':<15}"
    )
    print("-" * 75)

    for stock in inventory:
        warehouse = find_warehouse(stock["warehouse_id"])
        medicine = find_medicine(stock["medicine_id"])

        if warehouse is None or medicine is None:
            continue

        quantity = stock["quantity"]

        if quantity <= medicine["minimum_stock"]:
            status = "LOW STOCK"
        else:
            status = "OK"

        medicine_name = (
            f"{medicine['name']} {medicine['strength']}"
        )

        print(
            f"{warehouse['name']:<20}"
            f"{medicine_name:<25}"
            f"{quantity:<12}"
            f"{status:<15}"
        )

    print("-" * 75)

def distribute_medicine():
    print("\n--- Distribute Medicine ---")

    if not warehouses:
        print("No warehouses found.")
        return

    if not hospitals:
        print("No hospitals found.")
        return

    if not medicines:
        print("No medicines found.")
        return

    if not inventory:
        print("No stock available in warehouses.")
        return

    print("\nWarehouses:")

    for warehouse in warehouses:
        print(f"{warehouse['id']}. {warehouse['name']}")

    warehouse_id = get_valid_warehouse_id()

    print("\nHospitals:")

    for hospital in hospitals:
        print(f"{hospital['id']}. {hospital['name']}")

    hospital_id = get_valid_hospital_id()

    print("\nMedicines:")

    for medicine in medicines:
        print(
            f"{medicine['id']}. "
            f"{medicine['name']} {medicine['strength']}"
        )

    medicine_id = get_valid_medicine_id()

    quantity = get_positive_integer("Quantity to distribute: ")

    warehouse_stock = find_warehouse_stock(
        warehouse_id,
        medicine_id
    )

    if warehouse_stock is None:
        print("\nMedicine is not available in this warehouse.")
        return

    # Check if enough stock exists
    if warehouse_stock["quantity"] < quantity:
        print("\nInsufficient stock!")
        print(f"Available: {warehouse_stock['quantity']}")
        print(f"Requested: {quantity}")
        return

    # Remove stock from warehouse
    warehouse_stock["quantity"] -= quantity

    save_data(
        INVENTORY_FILE,
        inventory
    )

    record_movement(
        medicine_id,
        "warehouse",
        warehouse_id,
        "DISTRIBUTE",
        -quantity,
        f"Distributed to hospital {hospital_id}"
    )

    hospital_stock = find_hospital_stock(
        hospital_id,
        medicine_id
    )

    if hospital_stock:
        hospital_stock["quantity"] += quantity

        save_data(
            HOSPITAL_INVENTORY_FILE,
            hospital_inventory
        )

        record_movement(
            medicine_id,
            "hospital",
            hospital_id,
            "RECEIVE",
            quantity,
            f"Received from warehouse {warehouse_id}"
        )

        print("\nMedicine distributed successfully!")
        return

    # Hospital does not have this medicine yet
    new_stock = {
        "hospital_id": hospital_id,
        "medicine_id": medicine_id,
        "quantity": quantity
    }

    hospital_inventory.append(new_stock)

    save_data(
        HOSPITAL_INVENTORY_FILE,
        hospital_inventory
    )

    record_movement(
        medicine_id,
        "hospital",
        hospital_id,
        "RECEIVE",
        quantity,
        f"Received from warehouse {warehouse_id}"
    )

    print("\nMedicine distributed successfully!")

def view_hospital_inventory():
    print("\n--- Hospital Inventory ---")

    if not hospital_inventory:
        print("No hospital inventory found.")
        return

    print("\n" + "-" * 75)
    print(
        f"{'Hospital':<20}"
        f"{'Medicine':<25}"
        f"{'Quantity':<12}"
        f"{'Status':<15}"
    )
    print("-" * 75)

    for stock in hospital_inventory:
        hospital = find_hospital(stock["hospital_id"])
        medicine = find_medicine(stock["medicine_id"])

        if hospital is None or medicine is None:
            continue

        quantity = stock["quantity"]

        if quantity <= medicine["minimum_stock"]:
            status = "LOW STOCK"
        else:
            status = "OK"

        medicine_name = (
            f"{medicine['name']} {medicine['strength']}"
        )

        print(
            f"{hospital['name']:<20}"
            f"{medicine_name:<25}"
            f"{quantity:<12}"
            f"{status:<15}"
        )

    print("-" * 75)

def record_consumption():
    print("\n--- Record Consumption ---")

    if not hospitals:
        print("No hospitals found.")
        return

    if not medicines:
        print("No medicines found.")
        return

    if not hospital_inventory:
        print("No hospital inventory found.")
        return

    print("\nHospitals:")

    for hospital in hospitals:
        print(f"{hospital['id']}. {hospital['name']}")

    hospital_id = get_valid_hospital_id()

    print("\nMedicines:")

    for medicine in medicines:
        print(
            f"{medicine['id']}. "
            f"{medicine['name']} {medicine['strength']}"
        )

    medicine_id = get_valid_medicine_id()

    quantity = get_positive_integer("Quantity consumed: ")

    hospital_stock = find_hospital_stock(
        hospital_id,
        medicine_id
    )

    if hospital_stock is None:
        print("\nThis medicine is not available at this hospital.")
        return

    # Check if hospital has enough stock
    if hospital_stock["quantity"] < quantity:
        print("\nInsufficient hospital stock!")
        print(f"Available: {hospital_stock['quantity']}")
        print(f"Requested: {quantity}")
        return

    # Remove consumed quantity
    hospital_stock["quantity"] -= quantity

    save_data(HOSPITAL_INVENTORY_FILE, hospital_inventory)

    print("\nConsumption recorded successfully!")


def view_alerts():
    print("\n--- Alerts ---")

    today = date.today()
    expiry_limit = today + timedelta(days=30)

    low_stock_found = False
    expired_found = False
    expiring_soon_found = False

    # -------------------------
    # LOW STOCK - WAREHOUSES
    # -------------------------

    for stock in inventory:
        medicine = find_medicine(stock["medicine_id"])
        warehouse = find_warehouse(stock["warehouse_id"])

        if medicine is None or warehouse is None:
            continue

        if stock["quantity"] <= medicine["minimum_stock"]:

            if not low_stock_found:
                print("\n🟡 LOW STOCK")
                print("-" * 40)
                low_stock_found = True

            print(
                f"Location: {warehouse['name']}\n"
                f"Medicine: {medicine['name']} {medicine['strength']}\n"
                f"Current stock: {stock['quantity']} {medicine['unit']}\n"
                f"Minimum stock: {medicine['minimum_stock']} {medicine['unit']}\n"
            )

    # -------------------------
    # LOW STOCK - HOSPITALS
    # -------------------------

    for stock in hospital_inventory:
        medicine = find_medicine(stock["medicine_id"])
        hospital = find_hospital(stock["hospital_id"])

        if medicine is None or hospital is None:
            continue

        if stock["quantity"] <= medicine["minimum_stock"]:

            if not low_stock_found:
                print("\n🟡 LOW STOCK")
                print("-" * 40)
                low_stock_found = True

            print(
                f"Location: {hospital['name']}\n"
                f"Medicine: {medicine['name']} {medicine['strength']}\n"
                f"Current stock: {stock['quantity']} {medicine['unit']}\n"
                f"Minimum stock: {medicine['minimum_stock']} {medicine['unit']}\n"
            )

    # -------------------------
    # EXPIRY ALERTS
    # -------------------------

    for medicine in medicines:

        expiry = datetime.strptime(
            medicine["expiry_date"],
            "%Y-%m-%d"
        ).date()

        # EXPIRED
        if expiry < today:

            if not expired_found:
                print("\n🔴 EXPIRED")
                print("-" * 40)
                expired_found = True

            print(
                f"Medicine: {medicine['name']} {medicine['strength']}\n"
                f"Expiry date: {medicine['expiry_date']}\n"
            )

        # EXPIRING SOON
        elif expiry <= expiry_limit:

            if not expiring_soon_found:
                print("\n🟠 EXPIRING SOON")
                print("-" * 40)
                expiring_soon_found = True

            print(
                f"Medicine: {medicine['name']} {medicine['strength']}\n"
                f"Expiry date: {medicine['expiry_date']}\n"
            )

    # -------------------------
    # NO ALERTS
    # -------------------------

    if (
        not low_stock_found
        and not expired_found
        and not expiring_soon_found
    ):
        print("\n✅ No alerts. Everything looks good!")



def main():
    while True:
        show_menu()

        choice = input("Enter your choice: ")

        if choice == "0":
            print("Goodbye!")
            break

        elif choice == "1":
            add_medicine()
            pause()

        elif choice == "2":
            view_medicines()
            pause()

        elif choice == "3":
            add_warehouse()
            pause()

        elif choice == "4":
            view_warehouses()
            pause()

        elif choice == "5":
            add_hospital()
            pause()

        elif choice == "6":
            view_hospitals()
            pause()

        elif choice == "7":
            add_stock()
            pause()

        elif choice == "8":
            view_inventory()
            pause()

        elif choice == "9":
            view_hospital_inventory()
            pause()

        elif choice == "10":
            distribute_medicine()
            pause()

        elif choice == "11":
            record_consumption()
            pause()

        elif choice == "12":
            view_alerts()
            pause()

        elif choice == "13":
            view_dashboard()
            pause()

        elif choice == "14":
            adjust_stock()
            pause()


if __name__ == "__main__":
    main()