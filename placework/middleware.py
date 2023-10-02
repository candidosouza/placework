from django.shortcuts import redirect

class CustomRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # verifica se o usuário precisa redefinir a senha, se precisar redireciona para a página de redefinição
        if request.user.is_authenticated and hasattr(request.user, 'user_profile') \
           and request.user.user_profile.reset_password \
           and not request.path.startswith('/password_new/'):
            return redirect('/password_new/')
        response = self.get_response(request)
        return response
