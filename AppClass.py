import json
from UserClass import User
from ProductClass import Product

class App:
    users_file_path = './Files/Users.txt'
    products_file_path = './Files/Products.txt'
    categories_file_path = './Files/Categories.txt'

    def __init__(self):
        self.users = {}                       # [username: User object]
        self.current_user = None              # User object or None
        self.products = {}                    # {DigiKala link: Product object}
        self.categories = {}                  # {category name: [DigiKala link]}
        self.get_informations()

    def get_informations(self):
        """This method gets users informations from database"""
        with open(self.users_file_path, 'r') as file:
            self.users = {key: User(**value) for key, value in json.loads(file.read()).items()}

        with open(self.products_file_path, 'r') as file:
            self.products = {key: Product(**value) for key, value in json.loads(file.read()).items()}

        with open(self.categories_file_path, 'r') as file:
            self.categories = {key: value for key, value in json.loads(file.read()).items()}

    def set_informations(self, user: bool = False, product: bool = False, category: bool = False):
        """This method saves users informations to database"""
        if user:
            with open(self.users_file_path, 'w') as file:
                temp = {key: value.get_informations() for key, value in self.users.items()}
                print(json.dumps(temp, indent = 4), file = file)

        if product:
            with open(self.products_file_path, 'w') as file:
                temp = {key: value.get_informations() for key, value in self.products.items()}
                print(json.dumps(temp, indent = 4), file = file)

        if category:
            with open(self.categories_file_path, 'w') as file:
                print(json.dumps(self.categories, indent = 4), file = file)