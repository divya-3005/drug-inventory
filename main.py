import json
from datetime import date, datetime, timedelta


MEDICINES_FILE = "data/medicines.json"
WAREHOUSES_FILE = "data/warehouses.json"
HOSPITALS_FILE = "data/hospitals.json"
INVENTORY_FILE = "data/inventory.json"
HOSPITAL_INVENTORY_FILE = "data/hospital_inventory.json"


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
    print("0. Exit")
    print("================================")

def pause():
    input("\nPress Enter to return to the menu...")

def add_medicine():
    print("\n--- Add Medicine ---")

    name = input("Medicine name: ")
    strength = input("Strength: ")
    unit = input("Unit: ")
    expiry_date = input("Expiry date (YYYY-MM-DD): ")
    minimum_stock = int(input("Minimum stock: "))

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

    warehouse_id = int(input("Select warehouse: "))

    print("\nMedicines:")

    for medicine in medicines:
        print(
            f"{medicine['id']}. "
            f"{medicine['name']} {medicine['strength']}"
        )

    medicine_id = int(input("Select medicine: "))

    quantity = int(input("Quantity: "))

    for stock in inventory:
        if (
            stock["warehouse_id"] == warehouse_id
            and stock["medicine_id"] == medicine_id
        ):
            stock["quantity"] += quantity

            save_data(INVENTORY_FILE, inventory)

            print("\nStock updated successfully!")
            return

    stock = {
        "warehouse_id": warehouse_id,
        "medicine_id": medicine_id,
        "quantity": quantity
    }

    inventory.append(stock)

    save_data(INVENTORY_FILE, inventory)

    print("\nStock added successfully!")

def view_inventory():
    print("\n--- Inventory ---")

    if not inventory:
        print("No inventory found.")
        return

    for stock in inventory:

        warehouse = None
        medicine = None

        for w in warehouses:
            if w["id"] == stock["warehouse_id"]:
                warehouse = w

        for m in medicines:
            if m["id"] == stock["medicine_id"]:
                medicine = m

        print("\n-----------------------------")
        print(f"Warehouse: {warehouse['name']}")
        print(f"Medicine: {medicine['name']} {medicine['strength']}")
        print(f"Quantity: {stock['quantity']} {medicine['unit']}")

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

    warehouse_id = int(input("Select warehouse: "))

    print("\nHospitals:")

    for hospital in hospitals:
        print(f"{hospital['id']}. {hospital['name']}")

    hospital_id = int(input("Select hospital: "))

    print("\nMedicines:")

    for medicine in medicines:
        print(
            f"{medicine['id']}. "
            f"{medicine['name']} {medicine['strength']}"
        )

    medicine_id = int(input("Select medicine: "))

    quantity = int(input("Quantity to distribute: "))

    # Find warehouse stock
    warehouse_stock = None

    for stock in inventory:
        if (
            stock["warehouse_id"] == warehouse_id
            and stock["medicine_id"] == medicine_id
        ):
            warehouse_stock = stock
            break

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

    save_data(INVENTORY_FILE, inventory)

    # Check if hospital already has this medicine
    for stock in hospital_inventory:
        if (
            stock["hospital_id"] == hospital_id
            and stock["medicine_id"] == medicine_id
        ):
            stock["quantity"] += quantity

            save_data(HOSPITAL_INVENTORY_FILE, hospital_inventory)

            print("\nMedicine distributed successfully!")
            return

    # Hospital does not have this medicine yet
    new_stock = {
        "hospital_id": hospital_id,
        "medicine_id": medicine_id,
        "quantity": quantity
    }

    hospital_inventory.append(new_stock)

    save_data(HOSPITAL_INVENTORY_FILE, hospital_inventory)

    print("\nMedicine distributed successfully!")

def view_hospital_inventory():
    print("\n--- Hospital Inventory ---")

    if not hospital_inventory:
        print("No hospital inventory found.")
        return

    for stock in hospital_inventory:

        hospital = None
        medicine = None

        for h in hospitals:
            if h["id"] == stock["hospital_id"]:
                hospital = h

        for m in medicines:
            if m["id"] == stock["medicine_id"]:
                medicine = m

        print("\n-----------------------------")
        print(f"Hospital: {hospital['name']}")
        print(f"Medicine: {medicine['name']} {medicine['strength']}")
        print(f"Quantity: {stock['quantity']} {medicine['unit']}")

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

    hospital_id = int(input("Select hospital: "))

    print("\nMedicines:")

    for medicine in medicines:
        print(
            f"{medicine['id']}. "
            f"{medicine['name']} {medicine['strength']}"
        )

    medicine_id = int(input("Select medicine: "))

    quantity = int(input("Quantity consumed: "))

    # Find hospital stock
    hospital_stock = None

    for stock in hospital_inventory:
        if (
            stock["hospital_id"] == hospital_id
            and stock["medicine_id"] == medicine_id
        ):
            hospital_stock = stock
            break

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

    alerts_found = False

    # Check warehouse inventory
    for stock in inventory:

        medicine = None
        warehouse = None

        for m in medicines:
            if m["id"] == stock["medicine_id"]:
                medicine = m
                break

        for w in warehouses:
            if w["id"] == stock["warehouse_id"]:
                warehouse = w
                break

        # Low stock alert
        if stock["quantity"] <= medicine["minimum_stock"]:
            print("\n⚠️ LOW STOCK")
            print(f"Medicine: {medicine['name']} {medicine['strength']}")
            print(f"Location: {warehouse['name']}")
            print(f"Current stock: {stock['quantity']}")
            print(f"Minimum stock: {medicine['minimum_stock']}")

            alerts_found = True

    # Check hospital inventory
    for stock in hospital_inventory:

        medicine = None
        hospital = None

        for m in medicines:
            if m["id"] == stock["medicine_id"]:
                medicine = m
                break

        for h in hospitals:
            if h["id"] == stock["hospital_id"]:
                hospital = h
                break

        # Low stock alert
        if stock["quantity"] <= medicine["minimum_stock"]:
            print("\n⚠️ LOW STOCK")
            print(f"Medicine: {medicine['name']} {medicine['strength']}")
            print(f"Location: {hospital['name']}")
            print(f"Current stock: {stock['quantity']}")
            print(f"Minimum stock: {medicine['minimum_stock']}")

            alerts_found = True

    # Check medicine expiry
    for medicine in medicines:

        expiry = datetime.strptime(
            medicine["expiry_date"],
            "%Y-%m-%d"
        ).date()

        if expiry < today:
            print("\n🔴 EXPIRED")
            print(f"Medicine: {medicine['name']} {medicine['strength']}")
            print(f"Expiry date: {medicine['expiry_date']}")

            alerts_found = True

        elif expiry <= expiry_limit:
            print("\n⚠️ EXPIRING SOON")
            print(f"Medicine: {medicine['name']} {medicine['strength']}")
            print(f"Expiry date: {medicine['expiry_date']}")

            alerts_found = True

    if not alerts_found:
        print("\nNo alerts. Everything looks good!")


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


if __name__ == "__main__":
    main()