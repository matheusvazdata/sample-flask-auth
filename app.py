from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import bcrypt

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://admin:admin123@127.0.0.1:3307/flask-crud"

login_manager = LoginManager()  # Inicializa o gerenciador de login
db.init_app(app)  # Inicializa o banco de dados com a aplicação Flask
# Session - conexão ativa com o banco de dados
login_manager.init_app(app)  # Inicializa o gerenciador de login com a aplicação Flask

# View de login
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        # Login do usuário
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
            # Aqui você deve adicionar a lógica para gerar o token JWT
            # e retornar para o usuário. Por enquanto, vamos apenas retornar uma mensagem de sucesso.
            # Exemplo: token = generate_jwt_token(user)
            # return jsonify({"token": token})
            # Para fins de exemplo, retornamos uma mensagem simples.
            # Lembre-se de que você deve usar HTTPS em produção para proteger as credenciais do usuário.
            login_user(user)
            # Aqui você pode adicionar o código para gerar o token JWT
            print(current_user.is_authenticated)
            return jsonify({"message": "Login bem-sucedido"})

    return jsonify({"message": "Credenciais inválidas!"}), 400

@app.route('/logout', methods=['GET'])
@login_required  # Protege a rota de logout, exigindo que o usuário esteja autenticado
def logout():
    logout_user()
    return jsonify({"message": "Logout bem-sucedido"})

@app.route("/user", methods=["POST"])
@login_required
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        user = User(username=username, password=hashed_password, role='user')
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "Usuário criado com sucesso!"})

    return jsonify({"message": "Dados inválidos!"}), 400

@app.route("/user/<int:user_id>", methods=["GET"])
@login_required
def read_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({"username": user.username})
    return jsonify({"message": "Usuário não encontrado!"}), 404

@app.route("/user/<int:user_id>", methods=["PUT"])
@login_required
def update_user(user_id):
    data = request.json
    user = User.query.get(user_id)

    if user_id != current_user.id and current_user.role == 'user':
        return jsonify({"message": "Você não tem permissão para atualizar este usuário!"}), 403


    if user and data.get("password"):
        user.password = data.get("password", user.password)
        db.session.commit()

        return jsonify({"message": f"Usuário {user_id} atualizado com sucesso!"})

    return jsonify({"message": f"Usuário {user_id} não encontrado!"}), 404

@app.route("/user/<int:user_id>", methods=["DELETE"])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)

    if current_user.role != 'admin':
        return jsonify({"message": "Você não tem permissão para deletar usuários!"}), 403

    if user_id == current_user.id:
        return jsonify({"message": "Você não pode deletar sua própria conta!"}), 403
    
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Usuário {user_id} deletado com sucesso!"})

    return jsonify({"message": f"Usuário {user_id} não encontrado!"}), 404

@app.route("/hello-world", methods=["GET"])
def hello_world():
    return "Hello, World!"

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

if __name__ == "__main__":
    app.run(debug=True)