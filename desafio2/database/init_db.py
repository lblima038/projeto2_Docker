#!/usr/bin/env python3
import sqlite3
import os
from datetime import datetime

# Caminho do banco de dados (montado no volume)
DB_PATH = '/data/database.db'

def init_database():
    """Inicializa o banco de dados e cria a tabela se não existir"""
    print("=" * 60)
    print("Inicializando banco de dados...")
    print(f"Caminho do banco: {DB_PATH}")
    print("=" * 60)
    
    # Garantir que o diretório existe
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # Conectar ao banco (cria se não existir)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Criar tabela se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            data_criacao TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    print("✓ Tabela 'usuarios' criada/verificada com sucesso")
    
    # Verificar se já existem dados
    cursor.execute('SELECT COUNT(*) FROM usuarios')
    count = cursor.fetchone()[0]
    print(f"✓ Total de registros existentes: {count}")
    
    # Inserir alguns dados de exemplo se a tabela estiver vazia
    if count == 0:
        print("\nInserindo dados de exemplo...")
        usuarios_exemplo = [
            ('João Silva', 'joao@example.com'),
            ('Maria Santos', 'maria@example.com'),
            ('Pedro Oliveira', 'pedro@example.com'),
        ]
        
        for nome, email in usuarios_exemplo:
            data_criacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                'INSERT INTO usuarios (nome, email, data_criacao) VALUES (?, ?, ?)',
                (nome, email, data_criacao)
            )
            print(f"  ✓ Inserido: {nome} ({email})")
        
        conn.commit()
        print(f"\n✓ {len(usuarios_exemplo)} registros inseridos com sucesso")
    else:
        print("\nBanco de dados já contém dados. Nenhum registro novo inserido.")
    
    # Mostrar todos os registros
    print("\n" + "=" * 60)
    print("Registros no banco de dados:")
    print("=" * 60)
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    
    for usuario in usuarios:
        print(f"ID: {usuario[0]} | Nome: {usuario[1]} | Email: {usuario[2]} | Criado em: {usuario[3]}")
    
    conn.close()
    print("=" * 60)
    print("Banco de dados inicializado com sucesso!")
    print("Os dados estão persistidos no volume Docker.")
    print("=" * 60)

if __name__ == '__main__':
    init_database()
