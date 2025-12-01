from flask import Flask, jsonify

app = Flask(__name__)


USERS = [
    {"id": 1, "name": "João Silva", "active_since": "2021-01-10"},
    {"id": 2, "name": "Maria Santos", "active_since": "2022-03-05"},
    {"id": 3, "name": "Pedro Oliveira", "active_since": "2020-07-22"},
]


@app.route("/users")
def list_users():
    return jsonify(USERS)


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "service-a"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)