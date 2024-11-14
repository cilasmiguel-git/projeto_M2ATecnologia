# Controle de Ponto Eletrônico

Este é um sistema simples de Controle de Ponto Eletrônico que permite gerenciar e registrar batidas de ponto (entrada e saída) para funcionários de diferentes empresas. O projeto foi desenvolvido com Django, seguindo boas práticas de organização de código e segurança.

## 📋 Funcionalidades do Sistema

1. **Página Inicial**
   - Permite que o usuário selecione uma empresa existente ou cadastre uma nova.

2. **Gerenciamento de Empresas**
   - Permite o cadastro, edição e exclusão de informações das empresas que usarão o sistema.

3. **Gerenciamento de Funcionários**
   - Cadastra e gerencia funcionários, associando-os a uma empresa específica.
   - Define o nível de acesso do funcionário como **administrador** ou **comum**:
      - **Administrador**: Acesso completo ao sistema, incluindo o gerenciamento de empresas e funcionários.
      - **Comum**: Acesso restrito apenas ao próprio histórico de pontos.

4. **Registro de Batidas**
   - Permite que um funcionário registre seu ponto de entrada e saída.

5. **Consulta de Batidas**
   - Exibe o histórico de pontos registrados para cada funcionário, com opção de filtro por data e por funcionário.

6. **Autenticação**
   - Sistema de login com permissão para diferentes níveis de acesso (admin e comum).

## 🗄 Estrutura do Projeto

- **`core/`** - Aplicação principal do projeto, onde estão os modelos, views e templates.
- **`templates/`** - Diretório dos templates HTML do projeto.
- **`models.py`** - Define a estrutura dos dados do banco de dados.
- **`views.py`** - Contém a lógica de negócios e controle de fluxo de páginas.
- **`urls.py`** - Configura as rotas e URLs do projeto.
- **`middlewares.py`** - Middleware para gerenciar permissões de acesso.

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.8 ou superior
- Django 5.1.3

### Passo a Passo

1. **Clone o Repositório**
   ```bash
   git clone https://github.com/seu_usuario/controle_ponto.git
   cd controle_ponto

Crie e Ative o Ambiente Virtual

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
Instale as Dependências

pip install -r requirements.txt
Configure o Banco de Dados

python manage.py migrate
Crie um Superusuário (Admin)

python manage.py createsuperuser
Inicie o Servidor

python manage.py runserver
Acesse o Sistema

Acesse http://127.0.0.1:8000/
Faça login com as credenciais do superusuário para acessar o painel administrativo.
📊 Modelos de Dados
1. Empresa
nome (str): Nome da empresa.
endereco (str): Endereço da empresa.
2. Funcionario
nome (str): Nome do funcionário.
email (str): Email único para login.
senha (str): Armazenada de forma segura com hash.
empresa (FK): Relacionamento com a empresa.
nivel_acesso (str): Define se o funcionário é comum ou administrador.
3. Ponto
funcionario (FK): Relacionamento com o funcionário.
data (date): Data da batida.
entrada (time): Hora de entrada.
saida (time): Hora de saída.
horas_trabalhadas (property): Calcula o total de horas trabalhadas no dia.
🔒 Níveis de Acesso
Administrador

Acesso completo ao sistema, incluindo o gerenciamento de empresas e funcionários.
Pode ver, editar e excluir registros de pontos de todos os funcionários.
Comum

Acesso restrito apenas ao próprio histórico de pontos.
Permissão para registrar pontos de entrada e saída.
🌐 Rotas Principais
/admin_empresas/ - Gerenciamento de Empresas.
/admin_funcionarios/ - Gerenciamento de Funcionários.
/admin_pontos/ - Visualização e filtro de pontos registrados.
/login/ - Página de Login.
/funcionario/ - Página inicial do funcionário (apenas para usuários comuns).
/consulta_pontos/ - Histórico de pontos registrados para o funcionário logado.
💡 Middleware de Autorização
O middleware LoginRequiredMiddleware gerencia o acesso ao sistema:

Permite o acesso a páginas de administração apenas para usuários com permissão de administrador.
Redireciona usuários comuns para sua área restrita.
🌈 Interface e Templates
A interface é simples, utilizando CSS básico para usabilidade e estética.

O template admin_pontos.html inclui uma opção para selecionar funcionários e filtrar pontos por data.
Feedback visual (mensagens de sucesso e erro) é fornecido após as ações.
📘 Documentação do Código
O código está documentado com docstrings para facilitar a compreensão de funções e classes.

📝 Melhorias Futuras
Relatórios e Gráficos: Incluir gráficos para visualizar as horas trabalhadas de forma mais visual.
Edição de Registros de Ponto: Permitir a edição de registros de pontos já cadastrados.
API REST: Expor uma API para integração com sistemas externos.
📜 Licença
Este projeto está sob a licença MIT.

Para mais informações sobre o desenvolvimento ou contribuição, sinta-se à vontade para abrir um issue ou enviar um pull request.

Desenvolvido por [Seu Nome].

Este `README.md` está formatado para GitHub ou qualquer outro sistema que renderize Markdown, incluindo informações sobre permissões dos funcionários e estrutura do projeto.