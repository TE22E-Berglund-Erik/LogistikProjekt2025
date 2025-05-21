import random

# Globala variabler
ids = set()
users = []
login = False

# Funktion för att generera unika ID:n
def generate_id(prefix):
    while True:
        new_id = f"{prefix}{random.randint(1000, 9999)}"
        if new_id not in ids:
            ids.add(new_id)
            return new_id

# Basklass för entiteter med ID
class Entity:
    def __init__(self, prefix):
        self._id = generate_id(prefix)  # Genererar ID med prefix

    @property
    def id(self):
        return self._id

# Basklass för användare
class User(Entity):
    def __init__(self, username, password, email="", prefix="U"):
        super().__init__(prefix)
        self._username = username
        self._email = email
        self.__password = password

    def check_password(self, password_input):
        return self.__password == password_input

    def view_profile(self):
        return f"Username: {self._username}, Email: {self._email}, ID: {self.id}"

    def get_username(self):
        return self._username

    def get_email(self):
        return self._email

    def set_email(self, new_email):
        self._email = new_email

# Underklass för kund
class Customer(User):
    def __init__(self, username, password, email="", address=""):
        super().__init__(username, password, email, prefix="C")
        self._address = address
        self._orders = []

    def create_order(self, products):
        order = Order(self.id, products)
        self._orders.append(order)
        return order

    def get_orders(self):
        return self._orders

    def get_address(self):
        return self._address

    def set_address(self, new_address):
        self._address = new_address

# Underklass för administratör
class Admin(User):
    def __init__(self, username, password, email="", prefix="A"):
        super().__init__(username, password, email, prefix)

    def delete_user(self, user_id):
        to_delete = next((u for u in users if u.id == user_id), None)
        if to_delete:
            users.remove(to_delete)
            return True
        return False
    
    def list_users(self):
        for u in users:
            print(f"{u.id}: {u.get_username()} ({u.__class__.__name__})")

    def create_customer(self):
        while True:
            username = input("Enter new customer username: ").strip()
            if any(u.get_username() == username for u in users):
                print("Username already exists.")
                continue
            password = input("Enter new customer password: ").strip()
            if not username or not password:
                print("Username and password cannot be empty.")
                continue
            break
        return Customer(username, password)
    
# Underklass för ägare
class Owner(Admin):
    def __init__(self, username, password, email=""):
        super().__init__(username, password, email, prefix="O")
        self._has_full_access = True

    def create_admin(self):
        while True:
            username = input("Enter new admin username: ").strip()
            if any(u.get_username() == username for u in users):
                print("Username already exists.")
                continue
            password = input("Enter new admin password: ").strip()
            if not username or not password:
                print("Username and password cannot be empty.")
                continue
            break
        return Admin(username, password)


# Produktklass
class Product(Entity):
    def __init__(self, weight):
        super().__init__("P")
        self._weight = weight

    def get_weight(self):
        return self._weight

# Orderklass
class Order(Entity):
    def __init__(self, customer_id, product_list):
        super().__init__("OR")
        self._customer_id = customer_id
        self._product_list = product_list

    def get_total_weight(self):
        return sum(p.get_weight() for p in self._product_list)

    def get_customer_id(self):
        return self._customer_id

    def add_product(self, product):
        self._product_list.append(product)

    def remove_product(self, product):
        self._product_list.remove(product)

    def get_product_list(self):
        return self._product_list

    def print_product_list(self):
        for p in self._product_list:
            print(f"- Product ID: {p.id}, Weight: {p.get_weight()} kg")

    def remove_product_by_index(self, index):
        if 0 <= index < len(self._product_list):
            removed = self._product_list[index]
            self._product_list.remove(removed)
            return removed
        return None


# Transportklass
class Transport(Entity):
    def __init__(self, capacity, prefix="T"):
        super().__init__(prefix)
        self._capacity = capacity
        self._orders = []

    def add_order(self, order):
        self._orders.append(order)

    def get_orders(self):
        return self._orders

    def is_overloaded(self):  # Kontrollera om transporten är överbelastad
        return sum(order.get_total_weight() for order in self._orders) > self._capacity

    def get_capacity(self):
        return self._capacity

# Underklass för lastbil
class Truck(Transport):
    def __init__(self, capacity):
        super().__init__(capacity, prefix="TR")
        
# Lagerklass
class Warehouse(Entity):
    def __init__(self):
        super().__init__("W")
        self._stock = []

    def add_product(self, product):
        self._stock.append(product)

    def remove_product(self, product):
        self._stock.remove(product)

    def list_stock(self):
        return self._stock

# Owner meny
def owner_menu(user):
    while True:
        print("\nOwner Menu")
        print("1. Show all users")
        print("2. Create admin")
        print("3. Create customer")
        print("4. Delete user by ID")
        print("5. Logout")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            for u in users:
                user.list_users()  # Visar alla användare med ID och typ
        elif choice == "2":
            new_admin = user.create_admin()
            users.append(new_admin)
            print("Admin created.")
        elif choice == "3":
            new_customer = user.create_customer()
            users.append(new_customer)
            print("Customer created.")
        elif choice == "4":
            user_id = input("Enter user ID to delete: ").strip()
            if user.delete_user(user_id):
                print(f"User {user_id} deleted.")
            else:
                print("User ID not found.")
        elif choice == "5":
            print("Logged out.")
            return
        else:
            print("Invalid choice, please enter 1-5.")

# Admin meny
def admin_menu(user):
    while True:
        print("\nAdmin Menu")
        print("1. Show all users")
        print("2. Create customer")
        print("3. Delete user by ID")
        print("4. Logout")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            for u in users:
                user.list_users() # Visar alla användare med ID och typ
        elif choice == "2":
            new_customer = user.create_customer()
            users.append(new_customer)
            print("Customer created.")
        elif choice == "3":
            user_id = input("Enter user ID to delete: ").strip()
            to_delete = next((u for u in users if u.id == user_id))
            if to_delete:
                users.remove(to_delete)
                print(f"User {user_id} deleted.")
            else:
                print("User ID not found.")
        elif choice == "4":
            print("Logged out.")
            return
        else:
            print("Invalid choice, please enter 1-4.")

# Customer meny
def customer_menu(user):
    while True:
        print("\nCustomer Menu")
        print("1. View profile")
        print("2. Change email")
        print("3. Change address")
        print("4. Create order")
        print("5. View orders")
        print("6. Add product to existing order")
        print("7. Remove product from existing order")
        print("8. Logout")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            print(user.view_profile())
            print(f"Address: {user.get_address()}")
        elif choice == "2":
            new_email = input("Enter new email: ").strip()
            user.set_email(new_email)
            print("Email updated.")
        elif choice == "3":
            new_address = input("Enter new address: ").strip()
            user.set_address(new_address)
            print("Address updated.")
        elif choice == "4":
            try:
                weight = float(input("Enter product weight: ").strip())
                if weight <= 0:
                    print("Weight must be positive.")
                    continue
                product = Product(weight)
                order = user.create_order([product])
                print(f"Order created with ID: {order.id}")
            except ValueError:
                print("Invalid weight. Please enter a number.")
        elif choice == "5":
            orders = user.get_orders()
            for order in orders:
                print(f"\nOrder {order.id}")
                print(f"Total weight: {order.get_total_weight()} kg")
                order.print_product_list()
        elif choice == "6":
            order_id = input("Enter order ID: ").strip()
            order = next((o for o in user.get_orders() if o.id == order_id))
            weight = float(input("Enter new product weight: ").strip())
            if weight <= 0:
                print("Weight must be positive.")
                continue
            product = Product(weight)
            order.add_product(product)
            print(f"Product {product.id} added to order {order.id}.")
        elif choice == "7":
            order_id = input("Enter order ID: ").strip()
            order = next((o for o in user.get_orders() if o.id == order_id))
            for i, p in enumerate(order.get_product_list()):
                print(f"{i+1}. {p.id}, {p.get_weight()} kg")
            idx = int(input("Enter product number to remove: ").strip()) - 1
            removed = order.remove_product_by_index(idx)
            if removed:
                print(f"Removed product {removed.id}.")
        elif choice == "8":
            print("Logged out.")
            return
        else:
            print("Invalid choice, please enter 1-8.")


# Funktion för huvudmenyn
def start_menu():
    while True:
        print("\nMain Menu")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            username = input("Enter username: ").strip()
            if not username:
                print("Username cannot be empty.")
                continue
            if any(username == u.get_username() for u in users):
                print("Username already exists.")
                continue
            password = input("Enter password: ").strip()
            if not password:
                print("Password cannot be empty.")
                continue
            user = Customer(username, password)
            users.append(user)
            print("Registration successful. You can now log in.")

        elif choice == "2":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            user = next((u for u in users if u.get_username() ==
                        username and u.check_password(password)))
            if user:
                print("Login successful.")
                if isinstance(user, Owner):
                    owner_menu(user)
                elif isinstance(user, Admin):
                    admin_menu(user)
                elif isinstance(user, Customer):
                    customer_menu(user)
            else:
                print("Invalid username or password.")
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid choice, please enter 1, 2 or 3.")


# Test användare
for i in range(1, 10):
    admin = Admin(f"admin{i}", f"password{i}")
    users.append(admin)
for i in range(1, 1000):
    customer = Customer(f"customer{i}", f"password{i}")
    users.append(customer)

# Skapa en ägare
owner = Owner("owner", "password")
users.append(owner)

# Kör startmenyn
start_menu()
