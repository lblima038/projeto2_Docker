#!/usr/bin/env python3
import requests
import time
from datetime import datetime
import os
import sys

# URL do servidor (usando o nome do serviço do docker-compose)
SERVER_URL = os.environ.get('SERVER_URL', 'http://server:8080')
INTERVAL = int(os.environ.get('INTERVAL', '5'))  # segundos entre requisições

def make_request():
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] Fazendo requisição para {SERVER_URL}...")
        
        response = requests.get(SERVER_URL, timeout=5)
        response.raise_for_status()
        
        print(f"[{timestamp}] ✓ Resposta recebida - Status: {response.status_code}")
        print(f"[{timestamp}] ✓ Conteúdo: {response.text[:100]}...")
        return True
        
    except requests.exceptions.ConnectionError:
        print(f"[{timestamp}] ✗ Erro: Não foi possível conectar ao servidor")
        return False
    except requests.exceptions.Timeout:
        print(f"[{timestamp}] ✗ Erro: Timeout na requisição")
        return False
    except Exception as e:
        print(f"[{timestamp}] ✗ Erro: {str(e)}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Cliente de Requisições HTTP - Iniciando...")
    print(f"Servidor: {SERVER_URL}")
    print(f"Intervalo: {INTERVAL} segundos")
    print("=" * 60)
    print()
    
    request_count = 0
    success_count = 0
    
    try:
        while True:
            request_count += 1
            print(f"\n--- Requisição #{request_count} ---")
            
            if make_request():
                success_count += 1
            
            print(f"Estatísticas: {success_count}/{request_count} requisições bem-sucedidas")
            print(f"Aguardando {INTERVAL} segundos até a próxima requisição...")
            time.sleep(INTERVAL)
            
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("Interrompido pelo usuário")
        print(f"Total: {success_count}/{request_count} requisições bem-sucedidas")
        print("=" * 60)
        sys.exit(0)

