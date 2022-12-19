from users import Users
from emails import recover_password
import re

# Regex para verificar o e-mail
regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


# Verfica se o e-mail está correto
def verificando_email(email):
    if re.fullmatch(regex, email):
        return True
    else:
        return False


# Coleta o nome de usuário
def get_username():
    while True:
        try:
            usernam = str(input('Nome de Usuário: '))
            break
        except ValueError:
            print('Por favor informe um valor válido.')
    return usernam


# Coleta a senha
def get_password(lg):
    while True:
        try:
            passwor = str(input('Senha: '))
            if lg:
                if len(passwor) < 8:
                    print('Senha muito pequena! Tente uma senha maior.')
                elif len(passwor) > 200:
                    print('Senha muito grande tente algo menor!')
                else:
                    break
            else:
                break
        except ValueError:
            print('Por favor informe um valor válido.')
    return passwor


# Coleta o e-mail do usuário
def get_email():
    email = None
    while True:
        try:
            email = str(input('E-mail: '))
            vemail = verificando_email(email)
            if vemail:
                break
            else:
                print('E-mail inválido!')
        except ValueError:
            print('Por favor informe um valor válido!')
    return email

print('Teste de users.py')

users = Users()

# Início do App
while True:
    login = False
    # Decisão entre Login e Register
    while True:
        try:
            loginorregister = int(input('[1]Logar\n[2]Cadastrar\n:'))
            if loginorregister == 1 or loginorregister == 2:
                break
            else:
                print('Escolha entre as opções apresentadas acima.')
        except ValueError:
            print('Por favor informe um valor válido.')

    # -- Coleta de dados --
    # Username
    username = get_username()

    # Password
    password = get_password(True)

    # Login
    if loginorregister == 1:
        login, user_exists, passwordwrong = users.login(username, password)
        if login:
            print('Login realizado com sucesso!')
        elif not user_exists:
            print('Usuário ainda não cadastrado!')
        elif passwordwrong:
            tentarsenha = True
            while passwordwrong == True and tentarsenha == 1:
                while True:
                    try:
                        print('Senha incorreta!')
                        tentarsenha = int(input('[1]Tentar senha novamente\n[2]Recuperar senha(E-mail)\n[3]Sair\n:'))
                        if tentarsenha == 1 or tentarsenha == 2 or tentarsenha == 3:
                            break
                        else:
                            print('Selecione uma das opções acima!')
                    except ValueError:
                        print('Por favor informe um valor válido!')
                
                # -- Tentar senha novamente --
                if tentarsenha == 1:
                    password = get_password(True)
                    login, user_exists, passwordwrong = users.login(username, password)
                
                # -- Recuperação de Senha --
                elif tentarsenha == 2:
                    recuperado = False
                    while not recuperado:

                        # -- E-mail de recuperação --
                        for usuario in users.usuarios:
                            if username == usuario['Username']:
                                recoveremail = usuario['E-mail']
                                if recoveremail == None:
                                    while True:
                                        try:
                                            print('Esta conta não tem e-mail vinculado.')
                                            vincular = int(input('Deseja vincular um e-mail?\n[1]Sim\n[2]Não\n'))
                                            if vincular == 1:
                                                recoveremail = get_email()
                                                break
                                            elif vincular == 2:
                                                break
                                        except ValueError:
                                            print('Por favor informe um valor válido!')

                        if recoveremail != None:
                            # -- Mandando e-mail para recuperação da senha --
                            print(f'Um código de recuperação foi enviado para o e-mail {recoveremail}.')
                            codigo = recover_password(recoveremail)

                            # -- Código do Usuário --
                            while True:
                                enviarnovamente = 1
                                try:
                                    code = int(input('Código: '))
                                    break
                                except ValueError:
                                    print('Por favor informe um valor válido!')

                            # -- Código é válido --
                            if code == codigo:
                                for usuario in users.usuarios:
                                    if username == usuario['Username']:
                                        senharecuperada = usuario['Password']
                                recuperado = True
                                print(f'Recuperação de Senha completa!\nSenha: {senharecuperada}')
                            
                            # -- Código não é válido --
                            else:
                                print('Código Incorreto!')
                                while True:
                                    try:
                                        enviarnovamente = int(input('[1]Enviar Novamente\n[2]Retornar ao menu principal\n'))
                                        if enviarnovamente == 1 or enviarnovamente == 2:
                                            break
                                    except ValueError:
                                        print('Por favor informe um valor válido!')
                        elif recoveremail == None or vincular == 2:
                            print('Retornando ao menu principal')
                
                # -- Sair --
                elif tentarsenha == 3:
                    break

    # Register
    if loginorregister == 2:
        # E-mail
        while True:
            try:
                vincualar = int(input('Deseja vincular um e-mail a sua conta?\nOBS: Por questões de segurança recomendamos que seja vinculado um e-mail a conta em caso de perda de senha.\n[1]Sim\n[2]Não\n'))
                if vincualar == 1:
                    email = get_email()
                    break
                elif vincualar == 2:
                    email = None
                    break
            except ValueError:
                print('Por favor informe um valor válido!')

        register, user_exists, emailexists = users.register(username, password, email)
        if register:
            print('Usuário cadastrado com sucesso!')
        elif user_exists or emailexists:
            if user_exists:
                print('Usuário já cadastrado! Cadastro não foi realizado.')
            elif emailexists:
                print('Esse e-mail já foi vinculado a uma outra conta.')
            elif user_exists and emailexists:
                print('Usuário já cadastrado! Cadastro não foi realizado.')
                print('Esse e-mail já foi vinculado a uma outra conta.')

    # Saindo do loop se o Login tiver sido realizado com sucesso
    if login:
        break
print('Iniciando outra interface...')
