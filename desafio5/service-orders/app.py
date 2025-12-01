from flask import Flask, jsonify

app = Flask(__name__)

ORDERS = [
    {"id": 1, "user_id": 1, "product": "Notebook Dell", "amount": 3500.00, "status": "delivered", "date": "2024-01-15"},
    {"id": 2, "user_id": 1, "product": "Mouse Logitech", "amount": 150.00, "status": "delivered", "date": "2024-02-10"},
    {"id": 3, "user_id": 2, "product": "Teclado Mecânico", "amount": 450.00, "status": "processing", "date": "2024-03-20"},
    {"id": 4, "user_id": 3, "product": "Monitor LG 27\"", "amount": 1200.00, "status": "shipped", "date": "2024-03-25"},
    {"id": 5, "user_id": 2, "product": "Webcam HD", "amount": 280.00, "status": "delivered", "date": "2024-02-28"},
]


@app.route("/orders")
def list_orders():
    """Retorna lista de todos os pedidos"""
    return jsonify(ORDERS)


@app.route("/orders/<int:order_id>")
def get_order(order_id):
    """Retorna um pedido específico por ID"""
    order = next((o for o in ORDERS if o["id"] == order_id), None)
    if order:
        return jsonify(order)
    return jsonify({"error": "Pedido não encontrado"}), 404


@app.route("/orders/user/<int:user_id>")
def get_orders_by_user(user_id):
    """Retorna todos os pedidos de um usuário específico"""
    user_orders = [o for o in ORDERS if o["user_id"] == user_id]
    return jsonify(user_orders)


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "service-orders"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
