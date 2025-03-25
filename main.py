 

class Objekt:
    def __init__(self, id):
        self.id = id
        
class User(Objekt):
    def __init__(self, id, username, password):
        super().__init__(id)
        self.username = username
        self.password = password

class Customer(User):
    def __init__(self, id, username, password):
        super().__init__(id, username, password)

class Admin(User):
    def __init__(self, id, username, password):
        super().__init__(id, username, password)
        
class Owner(Admin):
    def __init__(self, id, username, password):
        super().__init__(id, username, password)
    
class Product(Objekt):
    def __init__(self, id, weight):
        super().__init__(id)
        self.weight = weight
        
class Order(Objekt):
    def __init__(self, id, customer_id, product_list):
        super().__init__(id)
        self.customer_id = customer_id
        self.product_list = product_list

class Transport(Objekt):
    def __init__(self, id, capacity):
        super().__init__(id)
        self.capacity = capacity

class Truck(Transport):
    def __init__(self, id, capacity):
        super().__init__(id, capacity)

class Warehouse(Objekt):
    def __init__(self, id):
        super().__init__(id)
        self.stock = []
        
    