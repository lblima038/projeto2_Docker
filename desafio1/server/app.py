from flask import Flask
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def hello():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hostname = os.environ.get('HOSTNAME', 'unknown')
    return f'''
    <html>
        <head><title>Servidor Docker</title></head>
        <body>
            <h1>Olá do Container Servidor!</h1>
            <p><strong>Timestamp:</strong> {timestamp}</p>
            <p><strong>Hostname:</strong> {hostname}</p>
            <p><strong>Status:</strong> Servidor funcionando corretamente</p>
        </body>
    </html>
    '''

@app.route('/health')
def health():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}

if __name__ == '__main__':
    print("Servidor Flask iniciando na porta 8080...")
    print("Aguardando requisições...")
    app.run(host='0.0.0.0', port=8080, debug=True)
