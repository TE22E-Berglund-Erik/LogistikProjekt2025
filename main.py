import random

# Globala variabler
ids = set()
users = []
login = False

# Funktion för att generera unika ID:n
def generate_id(prefix):
    while True:
        new_id = f"{prefix}{random.randint(1000, 9999)}" # Genererar ett ID med prefix och ett slumpmässigt numme
        if new_id not in ids: # Kollar om ID:t redan finns
            ids.add(new_id)
            return new_id

# Basklass för entiteter med ID
class Entity:
    def __init__(self, prefix):
        self._id = generate_id(prefix) # Genererar ett unikt ID med prefix

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

class Customer(User):
    def __init__(self, username, password, email="", address=""):
        super().__init__(username, password, email, prefix="C")
        self._address = address
        self._orders = []

    def create_order(self, products): # Skapar en order med en lista av produkter
        order = Order(self.id, products) # Skapar en order med ID och produkterna
        self._orders.append(order)
        return order

    def get_orders(self):
        return self._orders

    def get_address(self):
        return self._address

    def set_address(self, new_address):
        self._address = new_address

class Admin(User):
    def __init__(self, username, password, email="", prefix="A"):
        super().__init__(username, password, email, prefix)

    def delete_user(self, user_id):
        to_delete = next((u for u in users if u.id == user_id), None) # Hittar användaren med det angivna ID:t annars none
        if to_delete:
            users.remove(to_delete) # Tar bort användaren från listan
            return True
        return False

    # Skriver ut alla användare
    def list_users(self):
        for u in users:
            print(f"{u.id}: {u.get_username()} ({u.__class__.__name__})") # Skriver ut alla användare med deras ID och typ
 
    # Skapar en ny kund
    def create_customer(self):
        while True:
            username = input("Enter new customer username: ").strip()
            if any(u.get_username() == username for u in users): # Kollar om användarnamnet redan finns i users
                print("Username already exists.")
                continue
            password = input("Enter new customer password: ").strip()
            if not username or not password:
                print("Username and password cannot be empty.")
                continue
            break
        return Customer(username, password)

    #  Ägar klass 
class Owner(Admin):
    def __init__(self, username, password, email=""):
        super().__init__(username, password, email, prefix="O")
        self._has_full_access = True

    # Metod för att skapa en ny admin
    def create_admin(self):
        while True:
            username = input("Enter new admin username: ").strip()
            if any(u.get_username() == username for u in users): # Kollar om användarnamnet redan finns i users
                print("Username already exists.")
                continue
            password = input("Enter new admin password: ").strip()
            if not username or not password:
                print("Username and password cannot be empty.")
                continue
            break
        return Admin(username, password)

# Produkt och orderklasser
class Product(Entity):
    def __init__(self, weight):
        super().__init__("P")
        self._weight = weight

    def get_weight(self):
        return self._weight

class Order(Entity):
    def __init__(self, customer_id, product_list):
        super().__init__("OR")
        self._customer_id = customer_id
        self._product_list = product_list

    def get_total_weight(self):
        return sum(p.get_weight() for p in self._product_list) # Beräknar totalvikten av produkterna i ordern

    def get_customer_id(self):
        return self._customer_id

    def add_product(self, product):
        self._product_list.append(product) # Lägger till en produkt i ordern

    def remove_product(self, product):
        self._product_list.remove(product) # Tar bort en produkt från ordern

    def get_product_list(self):
        return self._product_list # Hämtar produktlistan

    def print_product_list(self): # Skriver ut produktlistan
        for p in self._product_list:
            print(f"- Product ID: {p.id}, Weight: {p.get_weight()} kg") # Skriver ut varje produkt i listan

    def remove_product_by_index(self, index): # Tar bort en produkt från listan baserat på index
        if 0 <= index < len(self._product_list):
            removed = self._product_list[index]
            self._product_list.remove(removed)
            return removed
        return None
    
    
 # Meny som visas för ägare
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
            try:
                user.list_users()
            except Exception as e:
                print(f"Error showing users: {e}")
        elif choice == "2":
            try:
                new_admin = user.create_admin()
                users.append(new_admin)
                print("Admin created.")
            except Exception as e:
                print(f"Error creating admin: {e}")
        elif choice == "3":
            try:
                new_customer = user.create_customer()
                users.append(new_customer)
                print("Customer created.")
            except Exception as e:
                print(f"Error creating customer: {e}")
        elif choice == "4":
            try:
                user_id = input("Enter user ID to delete: ").strip()
                if user.delete_user(user_id):
                    print(f"User {user_id} deleted.")
                else:
                    print("User ID not found.")
            except Exception as e:
                print(f"Error deleting user: {e}")
        elif choice == "5":
            print("Logged out.")
            return
        else:
            print("Invalid choice, please enter 1-5.")

# Meny som visas för admin
def admin_menu(user):
    while True:
        print("\nAdmin Menu")
        print("1. Show all users")
        print("2. Create customer")
        print("3. Delete user by ID")
        print("4. Logout")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            try:
                user.list_users()
            except Exception as e:
                print(f"Error showing users: {e}")
        elif choice == "2":
            try:
                new_customer = user.create_customer()
                users.append(new_customer)
                print("Customer created.")
            except Exception as e:
                print(f"Error creating customer: {e}")
        elif choice == "3":
            try:
                user_id = input("Enter user ID to delete: ").strip()
                to_delete = next((u for u in users if u.id == user_id), None)
                if to_delete:
                    users.remove(to_delete)
                    print(f"User {user_id} deleted.")
                else:
                    print("User ID not found.")
            except Exception as e:
                print(f"Error deleting user: {e}")
        elif choice == "4":
            print("Logged out.")
            return
        else:
            print("Invalid choice, please enter 1-4.")

# Meny som visas för kund
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

        try:
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
                weight = float(input("Enter product weight: ").strip())
                if weight <= 0:
                    print("Weight must be positive.")
                    continue
                product = Product(weight)
                order = user.create_order([product])
                print(f"Order created with ID: {order.id}")
            elif choice == "5":
                orders = user.get_orders()
                for order in orders:
                    print(f"\nOrder {order.id}")
                    print(f"Total weight: {order.get_total_weight()} kg")
                    order.print_product_list()
            elif choice == "6":
                order_id = input("Enter order ID: ").strip() 
                order = next((o for o in user.get_orders() if o.id == order_id), None) # Hittar ordern med det angivna ID:t annars none
                if not order:
                    print("Order not found.")
                    continue
                weight = float(input("Enter new product weight: ").strip())
                if weight <= 0:
                    print("Weight must be positive.")
                    continue
                product = Product(weight)
                order.add_product(product)
                print(f"Product {product.id} added to order {order.id}.")
            elif choice == "7":
                order_id = input("Enter order ID: ").strip()
                order = next((o for o in user.get_orders() if o.id == order_id), None) # Hittar ordern med det angivna ID:t annars none
                if not order:
                    print("Order not found.")
                    continue
                for i, p in enumerate(order.get_product_list()):
                    print(f"{i+1}. {p.id}, {p.get_weight()} kg")
                idx = int(input("Enter product number to remove: ").strip()) - 1
                removed = order.remove_product_by_index(idx)
                if removed:
                    print(f"Removed product {removed.id}.")
                else:
                    print("Invalid index.")
            elif choice == "8":
                print("Logged out.")
                return
            else:
                print("Invalid choice, please enter 1-8.")
        except Exception as e:
            print(f"An error occurred: {e}")

def start_menu():
    while True:
        print("\nMain Menu")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            try:
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
            except Exception as e:
                print(f"Error during registration: {e}")
        elif choice == "2":
            try:
                username = input("Enter username: ").strip()
                password = input("Enter password: ").strip()
                user = next((u for u in users if u.get_username() == username and u.check_password(password)), None) # Hittar användaren med det angivna användarnamnet och lösenordet annars none
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
            except Exception as e:
                print(f"Login failed: {e}")
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