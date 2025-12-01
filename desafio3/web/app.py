from flask import Flask, jsonify
import os
import psycopg2
import redis
from datetime import datetime


app = Flask(__name__)


DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppassword")

REDIS_HOST = os.getenv("REDIS_HOST", "cache")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS visits (
            id SERIAL PRIMARY KEY,
            visited_at TIMESTAMP NOT NULL,
            message TEXT NOT NULL
        )
        """
    )
    conn.commit()
    cur.close()
    conn.close()


def get_redis_client():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


@app.route("/")
def index():
    """
    Endpoint principal:
    - Incrementa um contador de visitas no Redis (cache)
    - Registra uma visita no Postgres (db)
    - Retorna informações agregadas
    """
    # Redis
    r = get_redis_client()
    visit_count = r.incr("visits_count")

    # Postgres
    conn = get_db_connection()
    cur = conn.cursor()
    now = datetime.utcnow()
    msg = f"Visita número {visit_count}"
    cur.execute(
        "INSERT INTO visits (visited_at, message) VALUES (%s, %s)",
        (now, msg),
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(
        {
            "message": "Serviço web em execução com cache e banco de dados!",
            "visits_count": visit_count,
            "last_visit": now.isoformat() + "Z",
        }
    )


@app.route("/stats")
def stats():
    """
    Exibe estatísticas de uso a partir do banco de dados.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM visits")
    total = cur.fetchone()[0]

    cur.execute(
        "SELECT visited_at, message FROM visits ORDER BY visited_at DESC LIMIT 5"
    )
    last = cur.fetchall()

    cur.close()
    conn.close()

    last_visits = [
        {"visited_at": row[0].isoformat() + "Z", "message": row[1]} for row in last
    ]

    return jsonify({"total_visits": total, "last_visits": last_visits})


@app.route("/health")
def health():
    """
    Verifica saúde dos serviços db e cache.
    """
    status = {"web": "ok"}

    # Testar DB
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.fetchone()
        cur.close()
        conn.close()
        status["db"] = "ok"
    except Exception as e:  # pragma: no cover - apenas log simples
        status["db"] = f"error: {e}"

    # Testar Redis
    try:
        r = get_redis_client()
        r.ping()
        status["cache"] = "ok"
    except Exception as e:  # pragma: no cover
        status["cache"] = f"error: {e}"

    return jsonify(status)


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)


