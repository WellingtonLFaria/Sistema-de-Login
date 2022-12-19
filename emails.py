import ssl
import os
import smtplib
from random import choices
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()

# E-mail e Senha usados para o envio de e-mails
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')


# Função que faz o envio do código de recuperação de senha
def recover_password(recoveremail):
    # Código de recuperação de senha
    code = ''
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    for number in choices(numbers, k=6):
        code += str(number)
    
    # Estrutura do e-mail
    titulo = 'Recuperação de Senha'
    corpo = f'Código: {code}'

    # Informações de envio do E-mail
    msg = EmailMessage()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recoveremail
    msg['Subject'] = titulo
    msg.set_content(corpo)

    context = ssl.create_default_context()

    # Enviando o e-mail
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_ADDRESS, recoveremail, msg.as_string())
    
    # Retornando o código de recuperação de senha
    return int(code)
