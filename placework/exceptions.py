ERRORS_MESSAGES_LOGIN = {
    'USER_ALEREADY_EXISTS': 'Usuário já cadastrado!',
    'USER_NOT_FOUND': 'Usuário não localizado. Você pode se cadastrar ou fazer o login com um email registrado.',
    'INVALID_CREDENTIALS': 'Credenciais, e-mail ou senha inválidos!',
    'LOCKED': 'Usuário bloqueado! Você errou a senha 5 vezes. Clique em "Esqueceu senha" para recuperar.',
    'EMAIL_VERIFICATION': 'Seu email não está verificado. Acesse o link enviado para seu email.',
    'RESET_PASSWORD': 'Você precisa redefinir sua senha.',
}


class LoginFailedException(Exception):
    pass
