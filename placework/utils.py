import secrets
import uuid
from datetime import timedelta

import bcrypt
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone

from common.utils import log
from placework.models import PasswordHistory, PasswordResetCode


def hash_password(password):
    # Gera um salt aleatório e crie o hash da senha
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def check_password(password, hashed_password):
    # Verifique se a senha fornecida corresponde ao hash armazenado
    return bcrypt.checkpw(
        password.encode('utf-8'), hashed_password.encode('utf-8')
    )


def change_password(user, new_password):
    # Recupere as últimas 5 senhas do histórico do usuário
    password_history = list(
        PasswordHistory.objects.filter(user=user).order_by('-id')
    )[:5]

    # Verifique se a nova senha corresponde a uma das senhas no histórico
    for history_entry in password_history:
        if check_password(new_password, history_entry.hashed_password):
            return False
    # Adicione a nova senha ao histórico
    hashed_password = hash_password(new_password)
    PasswordHistory.objects.create(user=user, hashed_password=hashed_password)

    # Certifique-se de que o histórico de senhas contenha no máximo 5 entradas
    if len(password_history) >= 5:
        oldest_entry = password_history[-1]
        oldest_entry.delete()

    # Atualize a senha do usuário
    user.set_password(new_password)
    user.save()
    return True


def generate_reset_code(user):
    # Gera um PasswordResetCode com código de redefinição de senha
    code = uuid.uuid4()
    expiration_time = timezone.now() + timedelta(hours=1)
    reset_code = PasswordResetCode(
        user=user, code=code, expiration_time=expiration_time
    )
    reset_code.save()
    return code


def is_reset_code_valid(reset_code):
    return timezone.now() > reset_code.expiration_time


def generate_password():
    # Gerar uma senha hexadecimal com 8 caracteres (4 bytes)
    return secrets.token_hex(4)


def send_password_email(user, code):
    subject = 'Solicitação de Redefinição. Nova senha gerada'
    message = f'Senha alterada com sucesso. Use a senha: {code} para acessar sua conta.\n \
                A Nova senha tem prazo de expiração de 1 hora para troca.'
    from_email = 'noreply@email.com'
    recipient_list = [user.email]
    if subject and message and from_email:
        try:
            send_mail(
                subject,
                message,
                from_email,
                recipient_list,
                fail_silently=False,
            )
        except Exception as e:
            log(str(e))
            print(str(e))
            return False


def send_reset_code_email(request, user, code):
    subject = 'Solicitação de Redefinição de Senha'

    link = f'http://{request.get_host()}/password_reset_confirm/{code}'
    if request.is_secure():
        link = f'https://{request.get_host()}/password_reset_confirm/{code}'

    message = f'Use o seguinte link para redefinir sua senha: {link}'
    from_email = 'noreply@email.com'
    recipient_list = [user.email]
    try:
        send_mail(
            subject, message, from_email, recipient_list, fail_silently=False
        )
        return True
    except Exception as e:
        log(str(e))
        print(str(e))
        return False


def send_register_code_email(request, user, code):
    subject = 'Solicitação de Cadastro'

    link = f'http://{request.get_host()}/cadastro/active_email/{user.email}/{code}'
    if request.is_secure():
        link = f'https://{request.get_host()}/cadastro/active_email/{user.email}/{code}'

    message = f'Use o seguinte link para ativar sua conta: \n {link}'
    from_email = 'noreply@email.com'
    recipient_list = [user.email]
    try:
        send_mail(
            subject, message, from_email, recipient_list, fail_silently=False
        )
        return True
    except Exception as e:
        log(str(e))
        print(str(e))
        return False
