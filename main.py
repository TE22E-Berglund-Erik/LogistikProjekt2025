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

class Objekt:
    def __init__(self, id):
        self.id = id

class User(Objekt):
    def __init__(self, username, password):
        super().__init__(generate_id("U"))
        self.username = username
        self.password = password

class Customer(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.id = generate_id("C")

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.id = generate_id("A")

class Owner(Admin):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.id = generate_id("O")

class Product(Objekt):
    def __init__(self, weight):
        super().__init__(generate_id("P"))
        self.weight = weight

class Order(Objekt):
    def __init__(self, customer_id, product_list):
        super().__init__(generate_id("OR"))
        self.customer_id = customer_id
        self.product_list = product_list

class Transport(Objekt):
    def __init__(self, capacity):
        super().__init__(generate_id("T"))
        self.capacity = capacity

class Truck(Transport):
    def __init__(self, capacity):
        super().__init__(capacity)
        self.id = generate_id("TR")

class Warehouse(Objekt):
    def __init__(self):
        super().__init__(generate_id("W"))
        self.stock = []

while login == False:
    print("\n1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter choice: ")
    
    if choice == "1":
        username = input("Enter username: ")
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
        user = next((user for user in users if user.username == username and user.password == password))
        if user:
            print("Login successful")
            login = True


    elif choice == "3":
        break

        
    if isinstance(user, Admin):
        while True:
            print("\nAdmin Menu")
            print("1. Show all users")
            print("2. Create admin")
            print("3. Logout")
            choice = input("Enter choice: ")

            if choice == "1":
                for u in users:
                    print(f"{u.id}: {u.username}")
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
        while True:
            print("\nCustomer Menu")
            print("1. View profile")
            print("2. Logout")
            choice = input("Enter choice: ")

            if choice == "1":
                print(f"Username: {user.username}, ID: {user.id}")
            elif choice == "2":
                print("Logged out.")
                login = False
                break
            

