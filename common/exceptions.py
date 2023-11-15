from http import HTTPStatus

from common.utils import log

ERRORS_MESSAGES = {
    'USER_ALEREADY_EXISTS': 'Usuário já cadastrado!',
    'USER_NOT_FOUND': 'Usuário não localizado. Você pode se cadastrar ou fazer o login com um email registrado.',
    'INVALID_CREDENTIALS': 'Credenciais, e-mail ou senha inválidos!',
    'BLOKED': 'Usuário bloqueado! Você errou a senha 5 vezes.',
}


class UserAlreadyExistsException(Exception):
    pass


class UserNotFoudException(Exception):
    def __init__(self, message=ERRORS_MESSAGES['USER_NOT_FOUND']) -> None:
        status_code = HTTPStatus.NOT_FOUND
        log(message)
        super().__init__(message, status_code)
