# 🍽️ Cardápio UAN — Projeto Django

Sistema simples de gerenciamento de cardápio diário desenvolvido em Django para o desafio de estágio do IFMG - Campus São João Evangelista.

---

# 👥 Equipe

* Pedro Henrique Santos
* Maria Luciana Gomes Silva
* Luise Vieira Castro
* Carlos Eduardo de Melo
* Leonardo Cayke A. Pimenta Prado
* Luiz Andre Fernandes Pego

---

# ⚙️ Tecnologias

* Python
* Django
* SQLite
* HTML/CSS
* Git/GitHub

---

# 🍽️ Guia de Instalação e Testes

Este documento fornece as instruções completas para configurar o ambiente de desenvolvimento, instalar dependências, preparar o banco de dados e popular o sistema com dados de teste.

## 📋 Pré-requisitos
Antes de começar, certifique-se de ter instalado em sua máquina:
* **Python** (versão 3.8 ou superior)
* **Git** (para versionamento)

---

## 🚀 Passo a Passo para Configuração Local

### 1. Clone o repositório (ou baixe o zip do repositorio manualmente)
```bash
git clone [https://github.com/ph-santos0/cardapio-uan.git](https://github.com/ph-santos0/cardapio-uan.git)
cd cardapio-uan
```
### 2. Criação do Ambiente Virtual (venv)

Abra o terminal na pasta raiz do projeto (onde está o arquivo `manage.py`) e execute:

**No Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**No Linux / Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```
*(Você saberá que deu certo quando o nome `(venv)` aparecer no início da linha do seu terminal).*

---

### 3. Instalação das Dependências
Com o ambiente virtual ativado, instale as bibliotecas necessárias que estão listadas no arquivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

### 4. Configuração do Banco de Dados (Migrations)
Sempre que baixar alterações novas, é necessário garantir que o banco de dados está atualizado com as tabelas do projeto. Execute os comandos de migração:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 5. Configurar Usuário Nutricionista (Acesso para Testes)
Para testar o sistema com as permissões corretas de um profissional de nutrição (criar e editar cardápios), criamos um comando automatizado que gera o grupo e o usuário padrão.
Basta executar:

```bash
python manage.py setup_nutricionistas

```

*(Isso criará automaticamente o usuário **`nutri`** com a senha **`nutri123`**).*

---

### 6. Popular o Banco de Dados

Para evitar que a tela inicial fique vazia durante os testes, desenvolvemos um comando que calcula a semana atual dinamicamente e injeta dados no sistema para "Hoje" e "Amanhã".
Execute:

```bash
python manage.py popular_banco

```

---

### 7. Executar o Servidor e Acessar

Com tudo configurado e o banco populado, inicie o servidor do projeto:

```bash
python manage.py runserver
```
Utilize o login:<br/>
Usuário: **`nutri`** <br/>
Senha: **`nutri123`** <br/> <br/>
**Pronto! O sistema está no ar. Acesse os endereços abaixo:**
* **Página Inicial (Escolha de Perfil):** `http://127.0.0.1:8000/`
* **Página Pública do Cardápio:** `http://127.0.0.1:8000/usuario/`
* **Login do Nutricionista:** `http://127.0.0.1:8000/login/`
* **Dashboard do Nutricionista:** `http://127.0.0.1:8000/dashboard/`
* **Painel de Controle (Admin):** `http://127.0.0.1:8000/admin/`

---

**📌 Observação: Acesso Total ao Sistema (Superusuário)**
O login `nutri` possui permissões limitadas, focadas apenas na gestão do cardápio. Caso você precise de acesso administrativo total para liberar todas as opções do Django, pare o servidor no terminal (Ctrl + C) e crie um superusuário executando:

```bash
python manage.py createsuperuser

```

Siga as instruções na tela para definir login e senha, e depois acesse o painel de controle com essa nova conta.


# 📌 Objetivo do Sistema

O sistema permitirá:

* Cadastro de cardápio diário;
* Login administrativo;
* Exibição pública do cardápio;
* Cadastro de almoço e jantar;
* Organização simples e funcional.

---

# ✅ Status Atual

* [x] Estrutura inicial criada
* [x] Projeto Django configurado
* [x] App principal criado
* [x] GitHub configurado
* [x] Models
* [x] Login
* [x] CRUD
* [x] Templates
* [x] Interface final
