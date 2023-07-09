import json
from threading import Thread, Lock
from UserClass import User
from ProductClass import Product
from SignUpAndLogin import check_sign_up_informations, check_login_informations, check_change_informations
from DigiKalaScraping import DigiKalaScrape


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

    @check_change_informations
    def change_current_user_informations(self, *, current_user_name: str, current_email: str, current_pass_word: str,
                                         new_user_name: str, new_email: str, new_pass_word: str, pass_word_repeat: str,
                                         users: dict):
        self.current_user._user_name, self.current_user._email = new_user_name, new_email
        if new_pass_word: self.current_user._pass_word = new_pass_word

        del self.users[current_user_name]
        self.users[new_user_name] = self.current_user

        Thread(target = self.set_informations, args = (True, )).start()

        return "changes has been saved successfully."

    def add_category(self, category_name: str):
        category_products = DigiKalaScrape()

        results = category_products.scrape_category(category_name, self.products)

        self.products.update(results)
        self.categories[category_name.lower()] = [link for link in results]

        Thread(target = self.set_informations, args = (False, True, True)).start()

    def update_price_thread(self, site: str, product_link: str):
        price = DigiKalaScrape.scraping_product_price(product_link, DigiKalaScrape.path)
        self.products[product_link].update_price(site, price)

    def update_product_price(self, product_link: str):
        threads = []
        for site, link in self.products[product_link].links.items():
            threads.append(Thread(target = self.update_price_thread, args = (site, link)))

        for t in threads: t.start()
        for t in threads: t.join()

    def check_matching(self, key_word: str, product: Product, mutex: Lock):
        words = key_word.lower().split()

        matched = True if [word in product.title.lower() for word in words].count(True) >= (len(words) / 2) else False

        if matched:
            mutex.acquire()
            self.search_results.append(product)
            mutex.release()

    def clear_search_result(self):
        self.search_results = []

    def search(self, key_word: str):
        self.search_results = []
        mutex = Lock()

        threads = [Thread(target = self.check_matching, args = (key_word, product, mutex)) for product in self.products.values()]
        for t in threads: t.start()
        for t in threads: t.join()

        result_count = len(self.search_results)
        if result_count < 5:
            product_count = 5 - result_count

            matched_products = DigiKalaScrape()

            results = matched_products.scrape_category(key_word, self.products, product_count)
            self.products.update(results)

            self.search_results += list(results.values())

    def add_favorite(self, product_link):
        self.current_user.favorites.append(product_link)

        Thread(target = self.set_informations, args = (True, False, False)).start()

    def remove_favorite(self, product_link):
        self.current_user.favorites.remove(product_link)

        Thread(target = self.set_informations, args = (True, False, False)).start()

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