from AppClass import App
from PyQt6.QtWidgets import QWidget
from PyQt6 import uic

class StartUpUI(QWidget):
    start_up_ui_path = './UIs/StartUp.ui'

    def __init__(self, app: App):
        super().__init__()
        uic.loadUi(self.start_up_ui_path, self)

        self.app = app

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