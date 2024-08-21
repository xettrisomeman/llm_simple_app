

class IncorrectPassword(Exception):
    def __init__(self, message="Incorrect Password!"):
        self.message = message
        super().__init__(self.message)


class UsernameDoesNotExist(Exception):
    def __init__(self, message="Username does not exist!"):
        self.message = message
        super().__init__(self.message)



class UsernameAlreadyExist(Exception):
    def __init__(self, message="Username already exist!"):
        self.message = message
        super().__init__(self.message)


class PasswordDoesNotMatch(Exception):
    def __init__(self, message="Password does not match!"):
        self.message = message
        super().__init__(self.message)
