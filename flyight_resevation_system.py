import json
import os

FLIGHTS_FILE = "flights.json"
PASSENGERS_FILE = "passengers.json"
STAFF_FILE = "staff.json"

ADMIN_PASSWORD = "1234"

CITIES = [
    "Istanbul", "Ankara", "Izmir", "Bursa", "Antalya",
    "Adana", "Konya", "Gaziantep", "Kayseri", "Mersin"
]

WELCOME_CODE = "WELCOME20"
WELCOME_DISCOUNT = 0.20
LOYALTY_DISCOUNT = 0.04

flights = []
passengers = []
staff_members = []


def load_data():
    global flights, passengers, staff_members

    if os.path.exists(FLIGHTS_FILE):
        with open(FLIGHTS_FILE, "r", encoding="utf-8") as file:
            flights = json.load(file)

    if os.path.exists(PASSENGERS_FILE):
        with open(PASSENGERS_FILE, "r", encoding="utf-8") as file:
            passengers = json.load(file)

    if os.path.exists(STAFF_FILE):
        with open(STAFF_FILE, "r", encoding="utf-8") as file:
            staff_members = json.load(file)


def save_data():
    with open(FLIGHTS_FILE, "w", encoding="utf-8") as file:
        json.dump(flights, file, indent=4, ensure_ascii=False)

    with open(PASSENGERS_FILE, "w", encoding="utf-8") as file:
        json.dump(passengers, file, indent=4, ensure_ascii=False)

    with open(STAFF_FILE, "w", encoding="utf-8") as file:
        json.dump(staff_members, file, indent=4, ensure_ascii=False)


def find_flight(flight_no):
    for flight in flights:
        if flight["flight_no"] == flight_no:
            return flight
    return None


def find_passenger(username):
    for passenger in passengers:
        if passenger["username"] == username:
            return passenger
    return None


def find_staff(username):
    for staff in staff_members:
        if staff["username"] == username:
            return staff
    return None


def get_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            print("Value must be greater than 0.\n")
        except ValueError:
            print("Invalid number.\n")


def get_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print("Value must be greater than 0.\n")
        except ValueError:
            print("Invalid number.\n")


def create_seats(seat_count):
    seats = []

    for i in range(1, seat_count + 1):
        seats.append({
            "seat_no": i,
            "status": "empty",
            "passenger": None
        })

    return seats


def show_cities():
    print("\n--- Available Cities ---")
    for city in CITIES:
        print("-", city)


def list_flights():
    if len(flights) == 0:
        print("No flights found.\n")
        return

    print("\n--- Flights ---")
    for flight in flights:
        empty_seats = 0

        for seat in flight["seats"]:
            if seat["status"] == "empty":
                empty_seats += 1

        print(
            f"{flight['flight_no']} | "
            f"{flight['from']} -> {flight['to']} | "
            f"Date: {flight['date']} | "
            f"Price: {flight['price']} TL | "
            f"Empty Seats: {empty_seats}"
        )


def show_seats(flight):
    print("\n--- Seat Map ---")

    for seat in flight["seats"]:
        if seat["status"] == "empty":
            print(f"Seat {seat['seat_no']}: Empty")
        else:
            print(f"Seat {seat['seat_no']}: Taken")


def add_flight():
    print("\n--- Add Flight ---")
    show_cities()

    flight_no = input("Flight number: ").upper()
    from_city = input("From: ").title()
    to_city = input("To: ").title()

    if from_city not in CITIES or to_city not in CITIES:
        print("Flights can only be created between selected major cities in Turkey.\n")
        return

    if from_city == to_city:
        print("Departure and destination cities cannot be the same.\n")
        return

    date = input("Date: ")
    price = get_float("Ticket price: ")
    seat_count = get_int("Seat count: ")

    flight = {
        "flight_no": flight_no,
        "from": from_city,
        "to": to_city,
        "date": date,
        "price": price,
        "seats": create_seats(seat_count),
        "assigned_staff": []
    }

    flights.append(flight)
    save_data()

    print("Flight added successfully.\n")


def add_staff():
    print("\n--- Add Staff ---")

    username = input("Username: ")

    if find_staff(username):
        print("This username already exists.\n")
        return

    password = input("Password: ")
    name = input("Name: ").title()
    surname = input("Surname: ").title()
    role = input("Role (pilot/cabin): ").lower()

    if role != "pilot" and role != "cabin":
        print("Role must be pilot or cabin.\n")
        return

    salary = get_float("Salary: ")

    staff = {
        "username": username,
        "password": password,
        "name": name,
        "surname": surname,
        "role": role,
        "salary": salary
    }

    staff_members.append(staff)
    save_data()

    print("Staff added successfully.\n")


def delete_staff():
    if len(staff_members) == 0:
        print("No staff found.\n")
        return

    list_staff()

    username = input("Enter staff username to delete: ")
    staff = find_staff(username)

    if staff:
        staff_members.remove(staff)

        for flight in flights:
            flight["assigned_staff"] = [
                assigned for assigned in flight["assigned_staff"]
                if assigned["username"] != username
            ]

        save_data()
        print("Staff deleted successfully.\n")
    else:
        print("Staff not found.\n")


def list_staff():
    if len(staff_members) == 0:
        print("No staff found.\n")
        return

    print("\n--- Staff List ---")
    for staff in staff_members:
        print(
            f"Username: {staff['username']} | "
            f"{staff['name']} {staff['surname']} | "
            f"Role: {staff['role']} | "
            f"Salary: {staff['salary']} TL"
        )


def assign_staff_to_flight():
    if len(flights) == 0:
        print("No flights found.\n")
        return

    if len(staff_members) == 0:
        print("No staff found.\n")
        return

    list_flights()
    flight_no = input("Flight number: ").upper()
    flight = find_flight(flight_no)

    if not flight:
        print("Flight not found.\n")
        return

    list_staff()
    username = input("Staff username to assign: ")
    staff = find_staff(username)

    if not staff:
        print("Staff not found.\n")
        return

    for assigned in flight["assigned_staff"]:
        if assigned["username"] == username:
            print("This staff is already assigned to this flight.\n")
            return

    flight["assigned_staff"].append({
        "username": staff["username"],
        "name": staff["name"],
        "surname": staff["surname"],
        "role": staff["role"],
        "salary": staff["salary"]
    })

    save_data()
    print("Staff assigned to flight.\n")


def show_flight_staff():
    list_flights()
    flight_no = input("Flight number: ").upper()
    flight = find_flight(flight_no)

    if not flight:
        print("Flight not found.\n")
        return

    if len(flight["assigned_staff"]) == 0:
        print("No staff assigned to this flight.\n")
        return

    print("\n--- Assigned Staff ---")
    for staff in flight["assigned_staff"]:
        print(
            f"{staff['name']} {staff['surname']} | "
            f"Role: {staff['role']} | "
            f"Salary: {staff['salary']} TL"
        )


def register_passenger():
    print("\n--- Passenger Register ---")

    username = input("Username: ")

    if find_passenger(username):
        print("This username already exists.\n")
        return

    password = input("Password: ")
    name = input("Name: ").title()
    surname = input("Surname: ").title()

    passenger = {
        "username": username,
        "password": password,
        "name": name,
        "surname": surname,
        "balance": 0,
        "tickets": [],
        "transactions": [],
        "discount_code": WELCOME_CODE,
        "discount_used": False,
        "flight_count": 0
    }

    passengers.append(passenger)
    save_data()

    print("Passenger registered successfully.")
    print(f"Your new member discount code: {WELCOME_CODE}\n")


def passenger_login():
    username = input("Username: ")
    password = input("Password: ")

    passenger = find_passenger(username)

    if passenger and passenger["password"] == password:
        print("Login successful.\n")
        return passenger

    print("Login failed.\n")
    return None


def staff_login():
    username = input("Username: ")
    password = input("Password: ")

    staff = find_staff(username)

    if staff and staff["password"] == password:
        print("Login successful.\n")
        return staff

    print("Login failed.\n")
    return None


def add_balance(passenger):
    amount = get_float("Amount to add: ")

    passenger["balance"] += amount

    passenger["transactions"].append({
        "type": "Balance Added",
        "amount": amount
    })

    save_data()
    print(f"Balance added. Current balance: {passenger['balance']} TL\n")


def show_balance(passenger):
    print(f"\nCurrent balance: {passenger['balance']} TL\n")


def show_transactions(passenger):
    if len(passenger["transactions"]) == 0:
        print("No transactions found.\n")
        return

    print("\n--- Transaction History ---")
    for transaction in passenger["transactions"]:
        print(transaction)


def calculate_ticket_price(passenger, flight):
    discount_rate = 0
    discount_type = "No Discount"

    code = input("Enter discount code or press Enter: ").upper()

    if code == passenger["discount_code"] and not passenger["discount_used"]:
        discount_rate = WELCOME_DISCOUNT
        discount_type = "Welcome Discount 20%"
        passenger["discount_used"] = True

    elif passenger["flight_count"] != 0 and passenger["flight_count"] % 10 == 0:
        discount_rate = LOYALTY_DISCOUNT
        discount_type = "Loyalty Discount 4%"

    final_price = flight["price"] * (1 - discount_rate)

    return final_price, discount_type, discount_rate
    
def book_ticket(passenger):
    if len(flights) == 0:
        print("No flights found.\n")
        return

    print("\n--- Select Route ---")
    from_city = input("From: ").title()
    to_city = input("To: ").title()

    available_flights = [
        f for f in flights
        if f["from"] == from_city and f["to"] == to_city
    ]

    if not available_flights:
        print("No flights found for this route.\n")
        return

    print("\n--- Available Flights ---")
    for i, f in enumerate(available_flights, start=1):
        empty = sum(1 for s in f["seats"] if s["status"] == "empty")

        print(
            f"{i}- {f['flight_no']} | Date: {f['date']} | "
            f"Price: {f['price']} TL | Empty Seats: {empty}"
        )

    try:
        choice = int(input("Select flight number: "))
        selected_flight = available_flights[choice - 1]
    except:
        print("Invalid selection.\n")
        return

    show_seats(selected_flight)

    try:
        seat_no = int(input("Select seat number: "))
    except:
        print("Invalid seat.\n")
        return

    selected_seat = None

    for seat in selected_flight["seats"]:
        if seat["seat_no"] == seat_no:
            selected_seat = seat

    if not selected_seat or selected_seat["status"] == "taken":
        print("Seat not available.\n")
        return

    final_price, discount_type, discount_rate = calculate_ticket_price(passenger, selected_flight)

    if passenger["balance"] < final_price:
        print("Insufficient balance.\n")
        return

    passenger["balance"] -= final_price
    passenger["flight_count"] += 1

    selected_seat["status"] = "taken"
    selected_seat["passenger"] = passenger["username"]

    ticket = {
        "flight_no": selected_flight["flight_no"],
        "from": selected_flight["from"],
        "to": selected_flight["to"],
        "date": selected_flight["date"],
        "paid_price": final_price,
        "seat_no": seat_no
    }

    passenger["tickets"].append(ticket)

    save_data()

    print("Ticket booked successfully.\n")

def list_my_tickets(passenger):
    if len(passenger["tickets"]) == 0:
        print("You have no tickets.\n")
        return

    print("\n--- My Tickets ---")
    for i, ticket in enumerate(passenger["tickets"], start=1):
        print(
            f"{i}- {ticket['flight_no']} | "
            f"{ticket['from']} -> {ticket['to']} | "
            f"Date: {ticket['date']} | "
            f"Seat: {ticket['seat_no']} | "
            f"Paid: {ticket['paid_price']:.2f} TL | "
            f"{ticket['discount_type']}"
        )


def cancel_ticket(passenger):
    if len(passenger["tickets"]) == 0:
        print("You have no tickets to cancel.\n")
        return

    list_my_tickets(passenger)

    try:
        choice = int(input("Select ticket number to cancel: "))
    except ValueError:
        print("Invalid input.\n")
        return

    if choice < 1 or choice > len(passenger["tickets"]):
        print("Invalid ticket selection.\n")
        return

    ticket = passenger["tickets"].pop(choice - 1)
    flight = find_flight(ticket["flight_no"])

    if flight:
        for seat in flight["seats"]:
            if seat["seat_no"] == ticket["seat_no"]:
                seat["status"] = "empty"
                seat["passenger"] = None

    passenger["balance"] += ticket["paid_price"]

    passenger["transactions"].append({
        "type": "Ticket Refund",
        "flight_no": ticket["flight_no"],
        "amount": ticket["paid_price"]
    })

    save_data()
    print("Ticket cancelled successfully.")
    print(f"Refunded: {ticket['paid_price']:.2f} TL\n")


def update_ticket(passenger):
    if len(passenger["tickets"]) == 0:
        print("You have no tickets to update.\n")
        return

    list_my_tickets(passenger)

    try:
        choice = int(input("Select ticket number to update: "))
    except ValueError:
        print("Invalid input.\n")
        return

    if choice < 1 or choice > len(passenger["tickets"]):
        print("Invalid ticket selection.\n")
        return

    old_ticket = passenger["tickets"][choice - 1]
    old_flight = find_flight(old_ticket["flight_no"])

    print("\n1- Change seat")
    print("2- Change flight")
    update_choice = input("Choice: ")

    if update_choice == "1":
        if not old_flight:
            print("Flight not found.\n")
            return

        show_seats(old_flight)

        try:
            new_seat_no = int(input("New seat number: "))
        except ValueError:
            print("Invalid seat number.\n")
            return

        selected_seat = None

        for seat in old_flight["seats"]:
            if seat["seat_no"] == new_seat_no:
                selected_seat = seat

        if not selected_seat:
            print("Seat not found.\n")
            return

        if selected_seat["status"] == "taken":
            print("This seat is already taken.\n")
            return

        for old_seat in old_flight["seats"]:
            if old_seat["seat_no"] == old_ticket["seat_no"]:
                old_seat["status"] = "empty"
                old_seat["passenger"] = None

        selected_seat["status"] = "taken"
        selected_seat["passenger"] = passenger["username"]
        old_ticket["seat_no"] = new_seat_no

        save_data()
        print("Seat updated successfully.\n")

    elif update_choice == "2":
        list_flights()
        new_flight_no = input("New flight number: ").upper()
        new_flight = find_flight(new_flight_no)

        if not new_flight:
            print("New flight not found.\n")
            return

        show_seats(new_flight)

        try:
            new_seat_no = int(input("New seat number: "))
        except ValueError:
            print("Invalid seat number.\n")
            return

        selected_seat = None

        for seat in new_flight["seats"]:
            if seat["seat_no"] == new_seat_no:
                selected_seat = seat

        if not selected_seat:
            print("Seat not found.\n")
            return

        if selected_seat["status"] == "taken":
            print("This seat is already taken.\n")
            return

        price_difference = new_flight["price"] - old_ticket["paid_price"]

        if price_difference > 0:
            if passenger["balance"] < price_difference:
                print("Insufficient balance for price difference.\n")
                return

            passenger["balance"] -= price_difference

            passenger["transactions"].append({
                "type": "Ticket Upgrade Payment",
                "amount": price_difference
            })

        elif price_difference < 0:
            refund = abs(price_difference)
            passenger["balance"] += refund

            passenger["transactions"].append({
                "type": "Ticket Change Refund",
                "amount": refund
            })

        if old_flight:
            for old_seat in old_flight["seats"]:
                if old_seat["seat_no"] == old_ticket["seat_no"]:
                    old_seat["status"] = "empty"
                    old_seat["passenger"] = None

        selected_seat["status"] = "taken"
        selected_seat["passenger"] = passenger["username"]

        old_ticket["flight_no"] = new_flight["flight_no"]
        old_ticket["from"] = new_flight["from"]
        old_ticket["to"] = new_flight["to"]
        old_ticket["date"] = new_flight["date"]
        old_ticket["original_price"] = new_flight["price"]
        old_ticket["paid_price"] = new_flight["price"]
        old_ticket["discount_type"] = "No Discount"
        old_ticket["discount_rate"] = 0
        old_ticket["seat_no"] = new_seat_no

        save_data()
        print("Ticket updated successfully.")
        print(f"Current balance: {passenger['balance']:.2f} TL\n")

    else:
        print("Invalid choice.\n")


def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1- Add Flight")
        print("2- List Flights")
        print("3- Add Staff")
        print("4- Delete Staff")
        print("5- List Staff")
        print("6- Assign Staff to Flight")
        print("7- Show Flight Staff")
        print("8- Exit")

        choice = input("Choice: ")

        if choice == "1":
            add_flight()
        elif choice == "2":
            list_flights()
        elif choice == "3":
            add_staff()
        elif choice == "4":
            delete_staff()
        elif choice == "5":
            list_staff()
        elif choice == "6":
            assign_staff_to_flight()
        elif choice == "7":
            show_flight_staff()
        elif choice == "8":
            break
        else:
            print("Invalid choice.\n")


def staff_menu(staff):
    while True:
        print(f"\n--- Staff Menu ({staff['role']}) ---")
        print("1- Show My Information")
        print("2- List Flights")
        print("3- Exit")

        choice = input("Choice: ")

        if choice == "1":
            print("\n--- My Information ---")
            print(f"Name: {staff['name']} {staff['surname']}")
            print(f"Role: {staff['role']}")
            print(f"Salary: {staff['salary']} TL")
        elif choice == "2":
            list_flights()
        elif choice == "3":
            break
        else:
            print("Invalid choice.\n")


def passenger_menu(passenger):
    while True:
        print("\n--- Passenger Menu ---")
        print(f"Balance: {passenger['balance']:.2f} TL")
        print(f"Completed Flights: {passenger['flight_count']}")
        print("1- List Flights")
        print("2- Book Ticket")
        print("3- My Tickets")
        print("4- Cancel Ticket")
        print("5- Update Ticket")
        print("6- Add Balance")
        print("7- Show Balance")
        print("8- Transaction History")
        print("9- Exit")

        choice = input("Choice: ")

        if choice == "1":
            list_flights()
        elif choice == "2":
            book_ticket(passenger)
        elif choice == "3":
            list_my_tickets(passenger)
        elif choice == "4":
            cancel_ticket(passenger)
        elif choice == "5":
            update_ticket(passenger)
        elif choice == "6":
            add_balance(passenger)
        elif choice == "7":
            show_balance(passenger)
        elif choice == "8":
            show_transactions(passenger)
        elif choice == "9":
            break
        else:
            print("Invalid choice.\n")


def main():
    load_data()

    while True:
        print("\n=== Flight Reservation System ===")
        print("1- Admin Login")
        print("2- Staff Login")
        print("3- Passenger Login")
        print("4- Passenger Register")
        print("5- Exit")

        choice = input("Choice: ")

        if choice == "1":
            password = input("Admin password: ")

            if password == ADMIN_PASSWORD:
                admin_menu()
            else:
                print("Wrong admin password.\n")

        elif choice == "2":
            staff = staff_login()

            if staff:
                staff_menu(staff)

        elif choice == "3":
            passenger = passenger_login()

            if passenger:
                passenger_menu(passenger)

        elif choice == "4":
            register_passenger()

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice.\n")


main()