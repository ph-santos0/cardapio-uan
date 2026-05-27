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

# 🚀 Como configurar o projeto no computador

## 1. Clonar o repositório

```bash
git clone https://github.com/ph-santos0/cardapio-uan
```

---

## 2. Entrar na pasta do projeto

```bash
cd cardapio-uan
```

---

## 3. Criar ambiente virtual

```bash
python -m venv venv
```

---

## 4. Ativar ambiente virtual


```bash
venv\Scripts\Activate
```

Se der erro de permissão ABRA O WINDOWS POWER SHELL COM ADMINISTRADOR e cole:

```bash
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Depois execute novamente no vs code:

```bash
venv\Scripts\Activate
```

---

## 5. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## 6. Rodar servidor pra testar

```bash
python manage.py runserver
```
Se deu certo vambora programar!!!

---

# 🌿 Organização das Branches

Vocês devem criar uma branch.

## Criar branch (Individual ou em dupla, vai de vocês)

### Luiz

```bash
git checkout -b luiz
```

### Carlos

```bash
git checkout -b carlos
```

### Ou os dois

```bash
git checkout -b duplinha
```

---

# 🔄 Fluxo de trabalho

## Antes de começar

Atualizar projeto:

```bash
git pull origin main
```

---

## Depois de alterar código

Adicionar alterações:

```bash
git add .
```

Criar commit:

```bash
git commit -m "Descrição da alteração"
```

Enviar para GitHub:

```bash
git push origin nome-da-branch
```

Exemplo:

```bash
git push origin luiz
```

---

# ⚠️ Regras importantes

* NÃO programar diretamente na branch `main`;
* Cada integrante trabalha na própria branch;
* Sempre atualizar antes de começar;
* Evitar editar os mesmos arquivos ao mesmo tempo;
* Commits devem ter descrições claras.

---

# 📁 Estrutura do Projeto

```text
cardapio-uan/
│
├── cardapio/
├── config/
├── manage.py
├── requirements.txt
├── .gitignore
```

---

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
* [ ] Models
* [ ] Login
* [ ] CRUD
* [ ] Templates
* [ ] Interface final
