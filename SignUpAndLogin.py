def check_email(email: str):
    try:
        part1, part2 = email.split('@')
        part2, part3 = part2.split('.')

        if part1.isalnum() and part2.isalnum() and part3.isalnum():
            return True
    except:
        pass

    return False

def check_password(pass_word: str):
    result, error, copy_pass = True, None, pass_word
    special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']

    special_chars_existence = False
    for s_c in special_chars:
        if s_c in pass_word:
            special_chars_existence = True
            copy_pass = copy_pass.replace(s_c, '')

    digit_existence, upper_word_existence = False, False
    for item in pass_word:
        if item.isdigit(): digit_existence = True
        if item.isupper(): upper_word_existence = True

    if not all((special_chars_existence, digit_existence, upper_word_existence, copy_pass.isalnum())):
        result, error = False, "password must contain alphanumeric and special characters."

    elif len(pass_word) < 8:
        result, error = False, "password must contain a minimum of 8 characters."

    return result, error

def check_sign_up_informations(func):

    def check(*args, **kwargs):
        user_name, email = kwargs['user_name'], kwargs['email']
        pass_word, pass_word_repeat = kwargs['pass_word'], kwargs['pass_word_repeat']
        users = kwargs['users']

        if not user_name.isalnum():
            return False, "username must only contain alphanumeric characters."

        if user_name in users:
            return False, "this username is already taken."

        if not check_email(email):
            return False, "email is invalid."

        check_password_result, error = check_password(pass_word)
        if not check_password_result:
            return False, error

        if pass_word != pass_word_repeat:
            return False, "passwords doesn't match."

        return True, func(*args, **kwargs)

    return check

def check_login_informations(func):

    def check(*args, **kwargs):
        user_name, pass_word = kwargs['user_name'], kwargs['pass_word']
        users = kwargs['users']

        try:
            user = users[user_name]

            if user.pass_word != pass_word:
                raise Exception
        except:
            return False, "wrong informations."

        return True, func(*args, **kwargs)

    return check