from django.shortcuts import redirect, get_object_or_404
from django.urls import resolve
from .models import Funcionario

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url_name = resolve(request.path_info).url_name

        # Verifica se o usuário está logado pelo 'funcionario_id' na sessão
        if 'funcionario_id' not in request.session:
            # Permite o acesso apenas às rotas de login e registro para quem não está logado
            if url_name not in ['login_funcionario', 'registro']:
                return redirect('login_funcionario')
        else:
            # Recupera o usuário logado
            funcionario = get_object_or_404(Funcionario, id=request.session['funcionario_id'])

            # Verifica o nível de acesso do usuário
            if funcionario.nivel_acesso == 'admin':
                # Permite que admins acessem qualquer rota relacionada à administração
                admin_urls = ['admin_dashboard', 'admin_empresas', 'admin_funcionarios', 'admin_pontos', 'logout', 'deletar_empresa', 'deletar_funcionario']
                if url_name not in admin_urls:
                    return redirect('admin_dashboard')
            else:
                # Usuários comuns são redirecionados se tentarem acessar rotas de administração
                if url_name in ['admin_dashboard', 'admin_empresas', 'admin_funcionarios', 'admin_pontos']:
                    return redirect('funcionario_home')

        return self.get_response(request)
