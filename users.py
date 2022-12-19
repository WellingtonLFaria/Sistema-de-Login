class Users:
    def __init__(self):
        self.usuarios = []


    # Registrando um novo usuário
    def register(self, username, password, email=None):
        user_exists = False
        email_exists = False
        register = False

        for usuario in self.usuarios:
            if username == usuario['Username']:
                user_exists = True
                break
        
        for usuario in self.usuarios:
            if email == usuario['E-mail']:
                email_exists = True
                break
        
        if user_exists or email_exists:
            return register, user_exists, email_exists
        else:
            user = {'Username': username, 'Password': password, 'E-mail': email}
            self.usuarios.append(user)
            return register, user_exists, email_exists


    # Fazendo login de um usuário
    def login(self, username, password):
        user_exists = False
        passwordwrong = False
        login = False

        for usuario in self.usuarios:
            if username == usuario['Username']:
                user_exists = True
                if password == usuario['Password']:
                    login = True
                else:
                    passwordwrong = True

        return login, user_exists, passwordwrong
