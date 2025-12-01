from flask import Flask, jsonify

app = Flask(__name__)

USERS = [
    {"id": 1, "name": "João Silva", "email": "joao.silva@email.com", "active_since": "2021-01-10"},
    {"id": 2, "name": "Maria Santos", "email": "maria.santos@email.com", "active_since": "2022-03-05"},
    {"id": 3, "name": "Pedro Oliveira", "email": "pedro.oliveira@email.com", "active_since": "2020-07-22"},
    {"id": 4, "name": "Ana Costa", "email": "ana.costa@email.com", "active_since": "2023-05-15"},
]


@app.route("/users")
def list_users():
    """Retorna lista de todos os usuários"""
    return jsonify(USERS)


@app.route("/users/<int:user_id>")
def get_user(user_id):
    """Retorna um usuário específico por ID"""
    user = next((u for u in USERS if u["id"] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "Usuário não encontrado"}), 404


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "service-users"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


