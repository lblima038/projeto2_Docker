#!/usr/bin/env python3
import sqlite3
import os
import sys
import time

# Caminho do banco de dados (mesmo volume compartilhado)
DB_PATH = '/data/database.db'

def read_database():
    """Lê e exibe os dados do banco de dados"""
    print("=" * 60)
    print("Leitor de Banco de Dados - Iniciando...")
    print(f"Caminho do banco: {DB_PATH}")
    print("=" * 60)
    
    # Verificar se o arquivo existe
    if not os.path.exists(DB_PATH):
        print(f"✗ Erro: Banco de dados não encontrado em {DB_PATH}")
        print("Certifique-se de que o container do banco foi executado primeiro.")
        sys.exit(1)
    
    try:
        # Conectar ao banco
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Verificar se a tabela existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
        if not cursor.fetchone():
            print("✗ Erro: Tabela 'usuarios' não encontrada")
            conn.close()
            sys.exit(1)
        
        # Contar registros
        cursor.execute('SELECT COUNT(*) FROM usuarios')
        count = cursor.fetchone()[0]
        
        print(f"\n✓ Banco de dados encontrado!")
        print(f"✓ Total de registros: {count}\n")
        
        if count == 0:
            print("Banco de dados está vazio.")
        else:
            # Ler todos os registros
            print("=" * 60)
            print("DADOS PERSISTIDOS NO VOLUME:")
            print("=" * 60)
            cursor.execute('SELECT * FROM usuarios ORDER BY id')
            usuarios = cursor.fetchall()
            
            for usuario in usuarios:
                print(f"ID: {usuario[0]:<3} | Nome: {usuario[1]:<20} | Email: {usuario[2]:<25} | Criado em: {usuario[3]}")
            
            print("=" * 60)
        
        conn.close()
        
        print("\n✓ Leitura concluída com sucesso!")
        print("Estes dados estão persistidos no volume Docker.")
        print("Mesmo que os containers sejam removidos, os dados permanecerão.")
        print("=" * 60)
        
    except sqlite3.Error as e:
        print(f"✗ Erro ao acessar o banco de dados: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Erro inesperado: {e}")
        sys.exit(1)

if __name__ == '__main__':
    read_database()
