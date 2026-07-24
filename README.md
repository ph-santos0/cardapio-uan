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

### 1. Criação do Ambiente Virtual (venv)

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

### 2. Instalação das Dependências
Com o ambiente virtual ativado, instale as bibliotecas necessárias que estão listadas no arquivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Configuração do Banco de Dados (Migrations)
Sempre que baixar alterações novas, é necessário garantir que o banco de dados está atualizado com as tabelas do projeto. Execute os comandos de migração:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Criação do Superusuário (Acesso ao Painel Admin)
Para gerenciar o sistema pela interface web, crie um usuário administrador. Recomendamos o seguinte padrão para facilitar os testes da equipe:
* **Usuário:** `admin`
* **E-mail:** (pode deixar em branco, basta dar Enter)
* **Senha:** `admin123`

Execute o comando abaixo e siga as instruções na tela:
```bash
python manage.py createsuperuser
```
*(Nota: Ao digitar a senha no terminal, ela não aparecerá na tela. Isso é normal por questões de segurança. Apenas digite e aperte Enter).*

### 5. (Opcional) Popular o Banco de Dados com Dados de Teste
Para evitar que a tela de visualização fique vazia, você deve adicionar dados que correspondam à semana em que você está realizando o teste. 

Abra o shell interativo do Django:
```bash
python manage.py shell
```

Em seguida, **copie e cole todo o código abaixo no terminal e aperte Enter**. Este script calcula automaticamente a semana atual com base no relógio do seu computador e insere o cardápio de "Hoje" e "Amanhã":

```python
import datetime
from django.utils import timezone
from cardapio.models import SemanaCardapio, DiaCardapio, Refeicao, CategoriaItem, ItemCardapio, Cardapio

def popular_banco():
    def inserir(dia, ref, cat, nome, desc):
        item, _ = ItemCardapio.objects.get_or_create(nome_item=nome[:50], descricao=desc[:255])
        Cardapio.objects.get_or_create(id_dia=dia, id_refeicao=ref, id_categoria=cat, id_item=item)

    # Calculando dinamicamente o Domingo da semana atual
    hoje = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    dias_para_domingo = (hoje.weekday() + 1) % 7
    domingo_atual = hoje - datetime.timedelta(days=dias_para_domingo)
    sabado_atual = domingo_atual + datetime.timedelta(days=6, hours=23, minutes=59, seconds=59)

    # 1. Configurando Refeições e Categorias
    cafe, _ = Refeicao.objects.get_or_create(nome_refeicao='Café da Manhã')
    almoco, _ = Refeicao.objects.get_or_create(nome_refeicao='Almoço')
    cat_bebida, _ = CategoriaItem.objects.get_or_create(nome_categoria='Bebida')
    cat_base, _ = CategoriaItem.objects.get_or_create(nome_categoria='Prato Base')
    cat_carne, _ = CategoriaItem.objects.get_or_create(nome_categoria='Carne ou prep. com carne')

    # 2. Criando a Semana Atual
    semana_atual, _ = SemanaCardapio.objects.get_or_create(data_inicio=domingo_atual, data_fim=sabado_atual)

    # 3. Criando os Dias (Hoje e Amanhã)
    amanha = hoje + datetime.timedelta(days=1)
    dia_hoje, _ = DiaCardapio.objects.get_or_create(id_semana=semana_atual, data_dia=hoje, nome_dia='Hoje')
    dia_amanha, _ = DiaCardapio.objects.get_or_create(id_semana=semana_atual, data_dia=amanha, nome_dia='Amanhã')

    # 4. Inserindo Cardápio de Hoje
    inserir(dia_hoje, cafe, cat_bebida, 'Café e Leite', 'Café; Leite Integral')
    inserir(dia_hoje, almoco, cat_base, 'Arroz e Feijão', 'Arroz Simples; Feijão Carioca')
    inserir(dia_hoje, almoco, cat_carne, 'Estrogonofe', 'Estrogonofe de Frango com Champignon')

    # 5. Inserindo Cardápio de Amanhã
    inserir(dia_amanha, cafe, cat_bebida, 'Suco Natural', 'Suco de Laranja da Terra')
    inserir(dia_amanha, almoco, cat_base, 'Macarrão ao Sugo', 'Macarrão tipo Espaguete ao Molho Sugo')
    inserir(dia_amanha, almoco, cat_carne, 'Bife Acebolado', 'Bife de Alcatra Acebolado na Chapa')

    print(f"\n✅ SUCESSO! Banco populado dinamicamente para a semana de {domingo_atual.strftime('%d/%m/%Y')} a {sabado_atual.strftime('%d/%m/%Y')}!")

# Executa a função
popular_banco()
```

Quando a mensagem de `✅ SUCESSO!` aparecer, digite `exit()` para sair do shell.

### 6. Rodar o Servidor
Com o banco populado e configurado, inicie o servidor de desenvolvimento:
```bash
python manage.py runserver
```

**Pronto!** O sistema estará disponível. Acesse no seu navegador:
* **Página Pública do Cardápio:** `http://127.0.0.1:8000/`
* **Painel Administrativo:** `http://127.0.0.1:8000/admin/`

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
