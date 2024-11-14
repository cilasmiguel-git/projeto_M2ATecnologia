from django.urls import path
from .views import (
    FuncionarioView, PontoListView, AdminDashboardView,
    EmpresaListView, FuncionarioListView, PontoAdminListView,
    registro, home, login_funcionario, logout_funcionario,
)

urlpatterns = [
    path('', home, name='home'),
    path('funcionario/', FuncionarioView.as_view(), name='funcionario_home'),
    path('consulta_pontos/', PontoListView.as_view(), name='consulta_ponto'),
    path('admin_dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin_empresas/', EmpresaListView.as_view(), name='admin_empresas'),
    path('admin_funcionarios/', FuncionarioListView.as_view(), name='admin_funcionarios'),
    path('admin_pontos/', PontoAdminListView.as_view(), name='admin_pontos'),
    path('login/', login_funcionario, name='login_funcionario'),
    path('logout/', logout_funcionario, name='logout'),
    path('registro/', registro, name='registro'),
]
