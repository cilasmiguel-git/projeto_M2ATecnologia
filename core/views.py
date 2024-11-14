from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Empresa, Funcionario, Ponto
from django.contrib.auth.hashers import make_password, check_password

# Função decoradora para verificar permissão de administrador
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        funcionario_id = request.session.get('funcionario_id')
        if not funcionario_id:
            return redirect('login_funcionario')
        funcionario = get_object_or_404(Funcionario, id=funcionario_id)
        if funcionario.nivel_acesso != 'admin':
            return redirect('funcionario_home')
        return view_func(request, *args, **kwargs)
    return wrapper

# Página inicial
def home(request):
    return render(request, 'home.html')

# View para login do funcionário
def login_funcionario(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        try:
            funcionario = Funcionario.objects.get(email=email)
            if funcionario.check_senha(senha):
                request.session['funcionario_id'] = funcionario.id

                if funcionario.nivel_acesso == 'admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('funcionario_home')
            else:
                messages.error(request, 'Senha incorreta.')
        except Funcionario.DoesNotExist:
            messages.error(request, 'Funcionário não encontrado.')
    
    return render(request, 'login_funcionario.html')

# View para registro de novos funcionários
def registro(request):
    if 'funcionario_id' in request.session:
        return redirect('home')

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        empresa_id = request.POST.get('empresa_id')
        nivel_acesso = request.POST.get('nivel_acesso', 'comum')

        empresa = get_object_or_404(Empresa, id=empresa_id)
        funcionario = Funcionario(nome=nome, email=email, empresa=empresa, nivel_acesso=nivel_acesso)
        funcionario.senha = make_password(senha)
        funcionario.save()
        messages.success(request, 'Funcionário registrado com sucesso.')
        return redirect('login_funcionario')
    
    empresas = Empresa.objects.all()
    return render(request, 'registro.html', {'empresas': empresas})

class FuncionarioView(View):
    def get(self, request):
        funcionario_id = request.session.get('funcionario_id')
        if not funcionario_id:
            return redirect('login_funcionario')
        
        funcionario = get_object_or_404(Funcionario, id=funcionario_id)
        return render(request, 'funcionario_home.html', {'funcionario': funcionario})

    def post(self, request):
        funcionario_id = request.session.get('funcionario_id')
        if not funcionario_id:
            return redirect('login_funcionario')
        
        funcionario = get_object_or_404(Funcionario, id=funcionario_id)
        
        # Processa o formulário de registro de ponto
        entrada = request.POST.get('entrada')
        saida = request.POST.get('saida')
        
        # Criação do objeto de ponto
        ponto = Ponto(funcionario=funcionario, entrada=entrada, saida=saida)
        ponto.save()
        
        messages.success(request, 'Ponto registrado com sucesso!')
        
        # Renderiza a mesma página, permanecendo no "funcionario_home"
        return render(request, 'funcionario_home.html', {'funcionario': funcionario})


class PontoListView(View):
    def get(self, request):
        funcionario_id = request.session.get('funcionario_id')
        if not funcionario_id:
            return redirect('login_funcionario')
        
        funcionario = get_object_or_404(Funcionario, id=funcionario_id)
        pontos = Ponto.objects.filter(funcionario=funcionario).order_by('-data')
        return render(request, 'consulta_pontos.html', {'pontos': pontos})

@method_decorator(admin_required, name='dispatch')
class AdminDashboardView(View):
    def get(self, request):
        return render(request, 'admin_dashboard.html')

@method_decorator(admin_required, name='dispatch')
class EmpresaListView(View):
    def get(self, request):
        empresas = Empresa.objects.all()
        return render(request, 'admin_empresas.html', {'empresas': empresas})
    
    def post(self, request):
        nome = request.POST.get('nome')
        endereco = request.POST.get('endereco')
        Empresa.objects.create(nome=nome, endereco=endereco)
        messages.success(request, 'Empresa adicionada com sucesso.')
        return redirect('admin_empresas')
    def deletar_empresa(request, id):
        empresa = get_object_or_404(Empresa, id=id)
        empresa.delete()
        messages.success(request, 'Empresa deletada com sucesso.')
        return redirect('admin_empresas')


@method_decorator(admin_required, name='dispatch')
class FuncionarioListView(View):
    def get(self, request):
        empresas = Empresa.objects.all()
        funcionarios = Funcionario.objects.all()
        return render(request, 'admin_funcionarios.html', {
            'empresas': empresas,
            'funcionarios': funcionarios
        })

    def post(self, request):
        # Verifica se o formulário é para exclusão
        funcionario_id = request.POST.get('funcionario_id')
        if funcionario_id:
            funcionario = get_object_or_404(Funcionario, id=funcionario_id)
            funcionario.delete()
            messages.success(request, 'Funcionário deletado com sucesso.')
            return redirect('admin_funcionarios')

        # Caso contrário, adiciona um novo funcionário
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        empresa_id = request.POST.get('empresa')
        nivel_acesso = request.POST.get('nivel_acesso')
        
        empresa = get_object_or_404(Empresa, id=empresa_id)
        funcionario = Funcionario(nome=nome, email=email, empresa=empresa, nivel_acesso=nivel_acesso)
        funcionario.set_senha(senha)
        funcionario.save()
        messages.success(request, 'Funcionário adicionado com sucesso.')
        return redirect('admin_funcionarios')
    
@method_decorator(admin_required, name='dispatch')
class PontoAdminListView(View):
    def get(self, request):
        funcionarios = Funcionario.objects.all()
        pontos = []

        # Filtra pontos por funcionário e data, se ambos forem fornecidos
        funcionario_id = request.GET.get('funcionario_id')
        data = request.GET.get('data')

        if funcionario_id:
            funcionario = get_object_or_404(Funcionario, id=funcionario_id)
            pontos = Ponto.objects.filter(funcionario=funcionario)
            if data:
                pontos = pontos.filter(data=data)

        return render(request, 'admin_pontos.html', {
            'funcionarios': funcionarios,
            'pontos': pontos
        })

def logout_funcionario(request):
    if 'funcionario_id' in request.session:
        del request.session['funcionario_id']
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect('login_funcionario')

@login_required
@admin_required
def deletar_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)
    funcionario.delete()
    messages.success(request, 'Funcionário deletado com sucesso.')
    return redirect('admin_funcionarios')