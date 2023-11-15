from placework.exceptions import ERRORS_MESSAGES_LOGIN, LoginFailedException


class LoginStrategy:
    def handle_attempt(self, profile):
        raise NotImplementedError()


class DefaultLoginStrategy(LoginStrategy):
    def handle_attempt(self, profile):
        profile.error_login += 1
        profile.save()

        if profile.error_login == 5:
            profile.is_blocked = True
            profile.save()

        remaining_attempts = 5 - profile.error_login
        if remaining_attempts <= 0:
            raise LoginFailedException(ERRORS_MESSAGES_LOGIN['LOCKED'])

        return (
            f'Senha incorreta! Você tem mais {remaining_attempts} tentativas.'
        )
