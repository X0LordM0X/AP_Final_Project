import json
from threading import Thread
from UserClass import User
from ProductClass import Product
from SignUpAndLogin import check_sign_up_informations, check_login_informations

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

    @check_sign_up_informations
    def sign_up(self, *, user_name: str, email: str, pass_word: str, pass_word_repeat: str, users: dict):
        new_user = User(user_name, email, pass_word)

        self.current_user = new_user
        self.users[user_name] = new_user

        Thread(target = self.set_informations, args = (True, )).start()

        return "you signed up successfully."

    @check_login_informations
    def login(self, *, user_name: str, pass_word: str, users: dict):
        self.current_user = users[user_name]
        return "you logged in successfully."

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