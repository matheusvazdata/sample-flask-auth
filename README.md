# 🔐 Sample Flask Auth API

Este é um projeto de API RESTful desenvolvido com **Flask** que implementa autenticação de usuários, controle de permissões por papel (`admin` e `user`) e operações CRUD básicas. Utiliza `Flask-Login` para gerenciamento de sessões e `bcrypt` para hashing de senhas.

## 🚀 Tecnologias Utilizadas

- [Python 3.9+](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Flask-Login](https://flask-login.readthedocs.io/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [bcrypt](https://pypi.org/project/bcrypt/)
- [MySQL](https://www.mysql.com/)
- [Docker + Docker Compose](https://docs.docker.com/compose/)

## 🧱 Estrutura do Projeto

```
sample-flask-auth/
├── app.py                  # Aplicação principal Flask
├── database.py             # Instância e configuração do SQLAlchemy
├── models/
│   └── user.py             # Modelo de usuário (ORM)
├── database.db             # Arquivo local de banco (opcional)
├── docker-compose.yml      # Orquestração com MySQL (opcional)
├── requirements.txt        # Dependências do projeto
└── README.md               # Este arquivo
```

## ⚙️ Configuração e Execução

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/sample-flask-auth.git
cd sample-flask-auth
```

### 2. Criar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Rodar com Docker (opcional)
```bash
docker-compose up -d
```

> 🔐 Certifique-se de que a URI do banco em `app.py` está compatível com as credenciais do container MySQL.

## 🔐 Endpoints Disponíveis

| Método | Rota                | Protegida? | Descrição |
|--------|---------------------|------------|-----------|
| POST   | `/login`            | ❌         | Autenticação com login/senha |
| GET    | `/logout`           | ✅         | Logout da sessão atual |
| POST   | `/user`             | ✅ (admin) | Criação de novo usuário |
| GET    | `/user/<id>`        | ✅         | Consulta de usuário por ID |
| PUT    | `/user/<id>`        | ✅         | Atualiza senha do usuário (hash via bcrypt) |
| DELETE | `/user/<id>`        | ✅ (admin) | Deleta um usuário (exceto si mesmo) |
| GET    | `/hello-world`      | ❌         | Rota pública de teste |

## 🔐 Controle de Acesso

- **Usuário comum (`role='user'`)**:
  - Pode consultar e atualizar **apenas a própria conta**.
  - Não pode criar nem excluir outros usuários.

- **Administrador (`role='admin'`)**:
  - Pode criar e excluir usuários.
  - Não pode excluir a própria conta.

## ✅ Testes Manuais com cURL (exemplos)

```bash
# Login
curl -X POST http://localhost:5000/login \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123"}'

# Criar usuário (requer login como admin)
curl -X POST http://localhost:5000/user \
     -H "Content-Type: application/json" \
     -d '{"username": "joao", "password": "123"}'
```

## 📌 Notas Finais

- **Senha criptografada** com `bcrypt` (não armazenada em texto).
- **Sessões gerenciadas via Flask-Login** (cookies, não JWT).
- Evite usar `debug=True` em produção.
- Ideal para evoluir para autenticação com JWT (`flask-jwt-extended`) ou OAuth.

## 📄 Licença

Este projeto está sob a licença MIT.