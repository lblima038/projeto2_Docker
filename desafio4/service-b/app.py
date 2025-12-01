from flask import Flask, jsonify
import os
import requests

app = Flask(__name__)


SERVICE_A_URL = os.getenv("SERVICE_A_URL", "http://service-a:5000")


@app.route("/users/summary")
def users_summary():
    """
    Consome o microsserviço A (/users) e devolve frases amigáveis.
    """
    try:
        resp = requests.get(f"{SERVICE_A_URL}/users", timeout=5)
        resp.raise_for_status()
        users = resp.json()
    except Exception as e:
        return (
            jsonify(
                {
                    "error": "Não foi possível consultar o microsserviço A",
                    "details": str(e),
                }
            ),
            502,
        )

    summaries = [
        f"Usuário {u.get('name')} ativo desde {u.get('active_since')}"
        for u in users
    ]

    return jsonify(
        {
            "source": f"{SERVICE_A_URL}/users",
            "count": len(users),
            "summaries": summaries,
        }
    )


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "service-b"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)