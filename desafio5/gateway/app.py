from flask import Flask, jsonify, request
import os
import requests

app = Flask(__name__)

# URLs dos microsserviços
SERVICE_USERS_URL = os.getenv("SERVICE_USERS_URL", "http://service-users:5000")
SERVICE_ORDERS_URL = os.getenv("SERVICE_ORDERS_URL", "http://service-orders:5001")


def make_request(service_url, endpoint, timeout=5):
    """Faz uma requisição HTTP para um microsserviço"""
    try:
        url = f"{service_url}{endpoint}"
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        return resp.json(), resp.status_code
    except requests.exceptions.RequestException as e:
        return {"error": f"Erro ao comunicar com o serviço: {str(e)}"}, 502


@app.route("/users")
def gateway_users():
    """Gateway endpoint para listar usuários"""
    data, status = make_request(SERVICE_USERS_URL, "/users")
    return jsonify(data), status


@app.route("/users/<int:user_id>")
def gateway_user_by_id(user_id):
    """Gateway endpoint para obter usuário por ID"""
    data, status = make_request(SERVICE_USERS_URL, f"/users/{user_id}")
    return jsonify(data), status


@app.route("/orders")
def gateway_orders():
    """Gateway endpoint para listar pedidos"""
    data, status = make_request(SERVICE_ORDERS_URL, "/orders")
    return jsonify(data), status


@app.route("/orders/<int:order_id>")
def gateway_order_by_id(order_id):
    """Gateway endpoint para obter pedido por ID"""
    data, status = make_request(SERVICE_ORDERS_URL, f"/orders/{order_id}")
    return jsonify(data), status


@app.route("/orders/user/<int:user_id>")
def gateway_orders_by_user(user_id):
    """Gateway endpoint para obter pedidos de um usuário"""
    data, status = make_request(SERVICE_ORDERS_URL, f"/orders/user/{user_id}")
    return jsonify(data), status


@app.route("/health")
def gateway_health():
    """Health check do gateway e dos serviços"""
    gateway_status = {"status": "ok", "service": "gateway"}
    
    # Verifica saúde dos microsserviços
    users_health, users_status = make_request(SERVICE_USERS_URL, "/health")
    orders_health, orders_status = make_request(SERVICE_ORDERS_URL, "/health")
    
    gateway_status["services"] = {
        "users": users_health if users_status == 200 else {"status": "unavailable"},
        "orders": orders_health if orders_status == 200 else {"status": "unavailable"}
    }
    
    return jsonify(gateway_status), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

