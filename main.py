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
        pass

    def show_all_customers(self):
        return []

    def create_user(self, username, password):
        return User(username, password)

# Underklass för ägare
class Owner(Admin):
    def __init__(self, username, password, email=""):
        super().__init__(username, password, email, prefix="O")
        self._has_full_access = True

    def show_all_users(self):
        return []

    def create_admin(self, username, password):
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

# Skapa testanvändare
erik = Customer("erik", "1234", "bober@gmail.com", "Storgatan 1")
users.append(erik)

# Startmeny med felhantering
while not login:
    print("\n1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter choice: ").strip()

    if choice == "1":
        username = input("Enter username: ").strip()
        if not username:
            print("Username cannot be empty.")
            continue
        if any(username == user.get_username() for user in users):
            print("Username already exists.")
            continue
        password = input("Enter password: ").strip()
        if not password:
            print("Password cannot be empty.")
            continue
        user = User(username, password)
        users.append(user)
        print("Registration successful.")

    elif choice == "2":
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        user = next((u for u in users if u.get_username() == username and u.check_password(password)), None)
        if user:
            print("Login successful.")
            login = True
        else:
            print("Invalid username or password.")

    elif choice == "3":
        print("Exiting program.")
        break

    else:
        print("Invalid choice, please enter 1, 2 or 3.")
        continue

    # Meny för administratör
    if isinstance(user, Admin):
        while True:
            print("\nAdmin Menu")
            print("1. Show all users")
            print("2. Create admin")
            print("3. Logout")
            choice = input("Enter choice: ").strip()

            if choice == "1":
                for u in users:
                    print(f"{u.id}: {u.get_username()}")
            elif choice == "2":
                username = input("Enter new admin username: ").strip()
                password = input("Enter new admin password: ").strip()
                if not username or not password:
                    print("Username and password cannot be empty.")
                    continue
                new_admin = Admin(username, password)
                users.append(new_admin)
                print("Admin created.")
            elif choice == "3":
                print("Logged out.")
                login = False
                break
            else:
                print("Invalid choice, please enter 1, 2 or 3.")

    # Meny för kund
    elif isinstance(user, Customer):
        while True:
            print("\nCustomer Menu")
            print("1. View profile")
            print("2. Create order")
            print("3. Logout")
            choice = input("Enter choice: ").strip()

            if choice == "1":
                print(user.view_profile())
            elif choice == "2":
                product_weight = float(input("Enter product weight: "))
                product = Product(product_weight)
                order = user.create_order([product])
                print(f"Order created with ID: {order.id}")
            elif choice == "3":
                print("Logged out.")
                login = False
                break
            else:
                print("Invalid choice, please enter 1, 2 or 3.")