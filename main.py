import random

ids = set()
users = []
login = False


def generate_id(prefix):
    while True:
        new_id = f"{prefix}{random.randint(1000, 9999)}"
        if new_id not in ids:
            ids.add(new_id)
            return new_id


class Entity:
    def __init__(self, prefix):
        self._id = generate_id(prefix)  # Generarar id baserat på prefix

    @property
    def id(self):
        return self._id  # Returnera id


class User(Entity):  # Basklass för användare
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


class Customer(User):  # Underklass för kund
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


class Admin(User):  # Underklass för administratör
    def __init__(self, username, password, email="", prefix="A"):
        super().__init__(username, password, email, prefix)

    def delete_user(self, user_id):
        pass

    def show_all_customers(self):
        return []

    def create_user(self, username, password):
        return User(username, password)


class Owner(Admin):  # Underklass för ägare
    def __init__(self, username, password, email=""):
        super().__init__(username, password, email, prefix="O")
        self._has_full_access = True

    def show_all_users(self):
        return []

    def create_admin(self, username, password):
        return Admin(username, password)


class Product(Entity):  # Produktklass
    def __init__(self, weight):
        super().__init__("P")
        self._weight = weight

    def get_weight(self):
        return self._weight


class Order(Entity):  # Orderklass
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


class Transport(Entity):  # Transportklass
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


class Truck(Transport):  # Underklass för lastbil
    def __init__(self, capacity):
        super().__init__(capacity, prefix="TR")


class Warehouse(Entity):  # Lagerklass
    def __init__(self):
        super().__init__("W")
        self._stock = []

    def add_product(self, product):
        self._stock.append(product)

    def remove_product(self, product):
        self._stock.remove(product)

    def list_stock(self):
        return self._stock


erik = Customer("erik", "1234", "bober@gmail.com", "Storgatan 1")
users.append(erik)  # Lägg till användare i listan

while login == False:  # Huvudmeny
    print("\n1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter choice: ")

    if choice == "1":
        username = input("Enter username: ")
        # Kontrollera om användarnamnet redan finns
        if any(username == user.username for user in users):
            print("Username already exists")
            continue
        password = input("Enter password: ")
        user = User(username, password)
        users.append(user)
        print("Registration successful")

    elif choice == "2":
        username = input("Enter username: ")
        password = input("Enter password: ") 
        user = next((user for user in users if user.get_username() == username and user.check_password(password)))  # Hitta användaren
        if user:
            print("Login successful")
            login = True

    elif choice == "3":
        break

    if isinstance(user, Admin): # Om användaren är administratör
        while True:
            print("\nAdmin Menu")
            print("1. Show all users")
            print("2. Create admin")
            print("3. Logout")
            choice = input("Enter choice: ")

            if choice == "1":
                for u in users:
                    print(f"{u.id}: {u.username}") # Visa alla användare
            elif choice == "2":
                username = input("Enter new admin username: ")
                password = input("Enter new admin password: ")
                new_admin = Admin(username, password)
                users.append(new_admin)
                print("Admin created")
            elif choice == "3":
                print("Logged out.")
                login = False
                break

    else:
        while True: # Kundmeny
            print("\nCustomer Menu") 
            print("1. View profile")
            print("2. Logout")
            choice = input("Enter choice: ")

            if choice == "1":
                print(user.view_profile())
            elif choice == "2":
                print("Logged out.")
                login = False
                break
