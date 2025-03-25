import random

ids = set()

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
