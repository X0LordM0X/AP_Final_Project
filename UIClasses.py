from AppClass import App
from PyQt6.QtWidgets import QWidget, QMainWindow
from PyQt6 import uic


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