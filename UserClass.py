class User:
    def __init__(self, user_name: str, email: str, pass_word: str, favorites: list = []):
        self._user_name = user_name
        self._email = email
        self._pass_word = pass_word
        self.favorites = favorites                 # [Digikala link]

    @property
    def user_name(self):
        return self._user_name

    @property
    def pass_word(self):
        return self._pass_word

    @property
    def email(self):
        return self._email

    def get_informations(self):
        return {"user_name": self.user_name, "email": self.email, "pass_word": self.pass_word, "favorites": self.favorites}