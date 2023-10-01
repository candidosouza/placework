import uuid
import secrets
from django.utils import timezone
from datetime import timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.mail import send_mail,BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from placework.models import PasswordResetCode
from common.utils import log


def generate_reset_code(user):
    # Gera um PasswordResetCode com código de redefinição de senha
    code = uuid.uuid4()
    expiration_time = timezone.now() + timedelta(hours=1)
    reset_code = PasswordResetCode(user=user, code=code, expiration_time=expiration_time)
    reset_code.save()
    return code


def is_reset_code_valid(reset_code):
    # Verifique se a hora atual é maior que à hora de expiração
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
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
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
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return True
    except Exception as e:
        log(str(e))
        print(str(e))
        return False
