from AppClass import App
from UserClass import User
from ProductClass import Product
import webbrowser
from PyQt6.QtWidgets import (
    QWidget, QMainWindow, QVBoxLayout, QGridLayout, QLabel, QSpacerItem, QSizePolicy, QPushButton, QDialog, QScrollArea
)
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6 import uic

dialog_ui_path = './UIs/Dialog.ui'


class StartUpUI(QWidget):
    start_up_ui_path = './UIs/StartUp.ui'

    def __init__(self, app: App):
        super().__init__()
        uic.loadUi(self.start_up_ui_path, self)

        self.app = app
        self.main_window = MainUI(self.app, self)

    def loginbuttonClicked(self):
        """This method switches between sign up and login windows when login_button is clicked"""
        self.result_label.setText("")
        self.stackedWidget.setCurrentWidget(self.Login)

    def backbuttonClicked(self):
        """This method switches between login and sign up windows when login_button_2 is clicked"""
        self.result_label_2.setText("")
        self.stackedWidget.setCurrentWidget(self.SignUp)

    def signupOperation(self):
        """"""
        user_name, email = self.username_input.text(), self.email_input.text()
        pass_word, pass_word_repeat = self.password_input.text(), self.password2_input.text()

        result, message = self.app.sign_up(user_name = user_name, email = email, pass_word = pass_word,
                                  pass_word_repeat = pass_word_repeat, users = self.app.users)
        if not result:
            self.result_label.setText(message)
        else:
            self.main_window.show()
            self.close()

    def loginOperation(self):
        """"""
        user_name = self.username_input_2.text()
        pass_word = self.password_input_2.text()

        result, message = self.app.login(user_name = user_name, pass_word = pass_word, users = self.app.users)
        if not result:
            self.result_label_2.setText(message)
        else:
            self.main_window.show()
            self.close()

    def show_again(self):
        self.username_input.setText("")
        self.email_input.setText("")
        self.password_input.setText("")
        self.password2_input.setText("")
        self.username_input_2.setText("")
        self.password_input_2.setText("")
        self.stackedWidget.setCurrentWidget(self.SignUp)

        self.show()


class ProductViewUI(QMainWindow):
    """Product full view. Contains all specifications and buttons to open websites"""
    product_view_ui_path = './UIs/ProductView.ui'

    def __init__(self, app: App, product: Product):
        super().__init__()
        uic.loadUi(self.product_view_ui_path, self)

        self.app = app
        self.product = product

        self.title_label.setText(self.product.title)
        self.product_image.setPixmap(QPixmap(self.product.image))
        if product.main_link in self.app.current_user.favorites:
            self.favorite_button.setChecked(True)

        self.favorite_button.clicked.connect(self.favorite_button_clicked)

        self.create_table()
        self.create_link_buttons()

    def create_table(self):
        row_count = len(self.product.specifications["title"])

        main_layout = QVBoxLayout()
        child_layout = QGridLayout()

        for row in range(row_count):
            label_1, label_2 = QLabel(), QLabel()

            label_1.setText(self.product.specifications["title"][row])
            label_1.setWordWrap(True)
            label_1.setScaledContents(True)

            label_2.setText(self.product.specifications["info"][row])
            label_2.setWordWrap(True)
            label_2.setScaledContents(True)

            child_layout.addWidget(label_1, row, 1)
            child_layout.addWidget(label_2, row, 0)

        main_layout.addLayout(child_layout)
        main_layout.addSpacerItem(QSpacerItem(20, 20, vPolicy = QSizePolicy.Policy.Expanding))

        self.specifications_contents.setLayout(main_layout)

    def create_link_buttons(self):
        layout = QVBoxLayout()

        for site, price in self.product.price.items():
            button = QPushButton()
            button.setText(f"{site}: {price}")

            layout.addWidget(button)

            button.clicked.connect(lambda: webbrowser.open_new_tab(self.product.links[site]))

        layout.addSpacerItem(QSpacerItem(20, 20, vPolicy = QSizePolicy.Policy.Expanding))

        self.sites_contents.setLayout(layout)

    def favorite_button_clicked(self):
        if self.favorite_button.isChecked():
            self.app.add_favorite(self.product.main_link)
        else:
            self.app.remove_favorite(self.product.main_link)


class ProductPreview(QWidget):
    """Product mini preview widgets. Contains product title, image and view button"""
    product_preview_ui_path = './UIs/ProductPreview.ui'

    def __init__(self, app: App, product: Product):
        super().__init__()
        uic.loadUi(self.product_preview_ui_path, self)

        self.app = app
        self.product = product

        self.update_thread = UpdatePriceThread(app, product.main_link)
        self.update_thread.finished.connect(self.price_updated)

        self.product_title.setText(self.product.title)
        self.product_image.setPixmap(QPixmap(self.product.image))

    def viewClicked(self):
        self.update_thread.start()

        self.dialog = QDialog()
        uic.loadUi(dialog_ui_path, self.dialog)
        self.dialog.message.setText("Updating...")
        self.dialog.show()

    def price_updated(self):
        self.dialog.close()

        self.view_product = ProductViewUI(self.app, self.product)
        self.view_product.show()


class UpdatePriceThread(QThread):
    def __init__(self, app: App, product_link: str):
        super().__init__()

        self.app = app
        self.product_link = product_link

    def run(self):
        self.app.update_product_price(self.product_link)


class AddCategoryUI(QWidget):
    """New small widget that opens when user clicks on 'Add category' button"""
    add_category_ui_path = './UIs/AddCategory.ui'

    def __init__(self, app: App, parent_widget: QMainWindow):
        super().__init__()
        uic.loadUi(self.add_category_ui_path, self)

        self.app = app
        self.parent_widget = parent_widget

        self.add_thread = CreateCategoryThread(app)
        self.add_thread.started.connect(self.thread_started)
        self.add_thread.add_signal.connect(self.thread_finished)

    def addbuttonClicked(self):
        category_name = self.category_name_input.text().lower()
        if category_name not in self.app.categories:
            self.add_thread.category_name = category_name
            self.add_thread.start()

    def thread_finished(self, category_name: str):
        self.parent_widget.set_new_category(category_name)

        self.dialog.message.setText("Category added!")
        self.dialog.show()

        self.parent_widget.add_button.setEnabled(True)
        self.parent_widget.add_button_2.setEnabled(True)
        self.parent_widget.search_button.setEnabled(True)

    def thread_started(self):
        self.dialog = QDialog()
        uic.loadUi(dialog_ui_path, self.dialog)
        self.dialog.show()

        self.parent_widget.add_button.setDisabled(True)
        self.parent_widget.add_button_2.setDisabled(True)
        self.parent_widget.search_button.setDisabled(True)


class CreateCategoryThread(QThread):
    """Thread for scraping data"""
    add_signal = pyqtSignal(str)

    def __init__(self, app: App):
        super().__init__()

        self.app = app
        self.category_name = ''

    def set_new_category(self):
        self.app.add_category(self.category_name)

    def run(self):
        self.set_new_category()

        # sending a signal that means data are scraped
        self.add_signal.emit(self.category_name)


class CategoryArea(QScrollArea):
    def __init__(self, app: App, category_name: str):
        super().__init__()

        self.app = app
        self.category_name = category_name

        self.create_product_previews()

    def create_product_previews(self):
        widget = QWidget()
        layout = QGridLayout()

        count = 0
        for link in self.app.categories[self.category_name]:
            product = self.app.products[link]

            product_preview = ProductPreview(self.app, product)
            layout.addWidget(product_preview, *self.calculate_row_column(count))

            count += 1

        widget.setLayout(layout)
        self.setWidget(widget)

    @staticmethod
    def calculate_row_column(num: int):
        row, column = num // 3, num % 3
        return row, column


class MainUI(QMainWindow):
    main_window_ui_path = './UIs/MainWindow.ui'

    def __init__(self, app: App, start_up: StartUpUI):
        super().__init__()
        uic.loadUi(self.main_window_ui_path, self)

        self.app = app
        self.start_up = start_up

        self.full_menu_widget.setHidden(True)

        for category in self.app.categories:
            self.set_category(category)

    def userbuttonClicked(self):
        self.user_page_change_widget.close()

        self.user_page_user_label.setText(f"Username: {self.app.current_user.user_name}")
        self.user_page_email_label.setText(f"Email: {self.app.current_user.email}")

        self.stackedWidget.setCurrentWidget(self.user_page)

    def changeuserinfoClicked(self):
        self.user_page_change_widget.show()

        self.user_page_username_input.setText(self.app.current_user.user_name)
        self.user_page_email_input.setText(self.app.current_user.email)
        self.user_page_password_input.setText("")
        self.user_page_password2_input.setText("")
        self.user_page_result_label.setText("")

    def submitchangesClicked(self):
        current_user = self.app.current_user
        current_user_name, current_email, current_pass_word = current_user.user_name, current_user.email, current_user.pass_word

        new_user_name, new_email = self.user_page_username_input.text(), self.user_page_email_input.text()
        new_pass_word, pass_word_repeat = self.user_page_password_input.text(), self.user_page_password2_input.text()

        result, message = self.app.change_current_user_informations(
            current_user_name = current_user_name, current_email = current_email, current_pass_word = current_pass_word,
            new_user_name = new_user_name, new_email = new_email, new_pass_word = new_pass_word,
            pass_word_repeat = pass_word_repeat, users = self.app.users
        )
        if not result:
            self.user_page_result_label.setText(message)
        else:
            self.user_page_user_label.setText(f"Username: {self.app.current_user.user_name}")
            self.user_page_email_label.setText(f"Email: {self.app.current_user.email}")
            self.user_page_change_widget.close()

    def logoutClicked(self):
        self.start_up.show_again()
        self.close()