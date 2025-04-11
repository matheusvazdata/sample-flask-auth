from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

login_manager = LoginManager()  # Inicializa o gerenciador de login
db.init_app(app)  # Inicializa o banco de dados com a aplicação Flask
# Session - conexão ativa com o banco de dados
login_manager.init_app(app)  # Inicializa o gerenciador de login com a aplicação Flask

# View de login


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        # Login do usuário
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            # Aqui você deve adicionar a lógica para gerar o token JWT
            # e retornar para o usuário. Por enquanto, vamos apenas retornar uma mensagem de sucesso.
            # Exemplo: token = generate_jwt_token(user)
            # return jsonify({"token": token})
            # Para fins de exemplo, retornamos uma mensagem simples.
            # Lembre-se de que você deve usar HTTPS em produção para proteger as credenciais do usuário.
            return jsonify({"message": "Login bem-sucedido"})

    return jsonify({"message": "Credenciais inválidas"}), 400

@app.route("/hello-world", methods=["GET"])
def hello_world():
    return "Hello, World!"

@app.shell_context_processor
def make_shell_context():
    return {'db': db}

if __name__ == "__main__":
    app.run(debug=True)