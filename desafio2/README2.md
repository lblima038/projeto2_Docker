# Desafio 2 — Volumes e Persistência

## 📋 Objetivo

Demonstrar persistência de dados usando volumes Docker, garantindo que os dados permaneçam disponíveis mesmo após a remoção dos containers.

## 🏗️ Arquitetura da Solução

A solução consiste em:

1. **Container Database (database)**: Container que inicializa um banco de dados SQLite e insere dados de exemplo
2. **Container Reader (reader)**: Container que lê e exibe os dados persistidos no volume
3. **Volume Docker**: Volume nomeado `desafio2-db-data` que armazena os dados do banco de forma persistente

### Estrutura de Arquivos

```
desafio2/
├── database/
│   ├── Dockerfile
│   └── init_db.py          # Script para criar e popular o banco
├── reader/
│   ├── Dockerfile
│   └── read_db.py          # Script para ler dados do banco
├── docker-compose.yml       # Orquestração com volumes
└── README2.md
```

## 🔧 Componentes

### Container Database

- **Função**: Inicializa o banco de dados SQLite e insere dados de exemplo
- **Volume**: Monta o volume `/data` onde o banco de dados é armazenado
- **Comportamento**:
  - Cria a tabela `usuarios` se não existir
  - Insere dados de exemplo apenas se o banco estiver vazio
  - Exibe todos os registros após a inicialização
  - Os dados são salvos no volume Docker

### Container Reader

- **Função**: Lê e exibe os dados persistidos no banco de dados
- **Volume**: Acessa o mesmo volume `/data` compartilhado com o container database
- **Comportamento**:
  - Verifica se o banco de dados existe
  - Lê e exibe todos os registros da tabela `usuarios`
  - Demonstra que os dados persistem no volume

### Volume Docker

- **Nome**: `desafio2-db-data`
- **Tipo**: Local (armazenado no sistema de arquivos do host)
- **Localização**: Gerenciado pelo Docker (geralmente em `/var/lib/docker/volumes/` no Linux)
- **Persistência**: Os dados permanecem mesmo após remover os containers

## 🚀 Como Executar

### Pré-requisitos

- Docker instalado
- Docker Compose instalado (geralmente vem com o Docker Desktop)

### Passos para Executar

1. **Navegue até a pasta do desafio**:
   ```bash
   cd desafio2
   ```

2. **Construa e inicie os containers**:
   ```bash
   docker-compose up --build
   ```

   Ou para rodar em background:
   ```bash
   docker-compose up -d --build
   ```

3. **Visualizar os logs**:
   ```bash
   # Logs de ambos os containers
   docker-compose logs -f
   
   # Logs apenas do database
   docker-compose logs -f database
   
   # Logs apenas do reader
   docker-compose logs -f reader
   ```

4. **Parar os containers**:
   ```bash
   docker-compose down
   ```

## 📊 Demonstração da Persistência

### Passo 1: Inicializar o Banco de Dados

Ao executar `docker-compose up`, o container `database` será executado primeiro:

```
============================================================
Inicializando banco de dados...
Caminho do banco: /data/database.db
============================================================
✓ Tabela 'usuarios' criada/verificada com sucesso
✓ Total de registros existentes: 0

Inserindo dados de exemplo...
  ✓ Inserido: João Silva (joao@example.com)
  ✓ Inserido: Maria Santos (maria@example.com)
  ✓ Inserido: Pedro Oliveira (pedro@example.com)

✓ 3 registros inseridos com sucesso

============================================================
Registros no banco de dados:
============================================================
ID: 1 | Nome: João Silva | Email: joao@example.com | Criado em: 2024-01-15 10:30:00
ID: 2 | Nome: Maria Santos | Email: maria@example.com | Criado em: 2024-01-15 10:30:00
ID: 3 | Nome: Pedro Oliveira | Email: pedro@example.com | Criado em: 2024-01-15 10:30:00
============================================================
Banco de dados inicializado com sucesso!
Os dados estão persistidos no volume Docker.
============================================================
```

### Passo 2: Ler os Dados Persistidos

O container `reader` será executado automaticamente após o `database`:

```
============================================================
Leitor de Banco de Dados - Iniciando...
Caminho do banco: /data/database.db
============================================================

✓ Banco de dados encontrado!
✓ Total de registros: 3

============================================================
DADOS PERSISTIDOS NO VOLUME:
============================================================
ID: 1   | Nome: João Silva        | Email: joao@example.com        | Criado em: 2024-01-15 10:30:00
ID: 2   | Nome: Maria Santos      | Email: maria@example.com      | Criado em: 2024-01-15 10:30:00
ID: 3   | Nome: Pedro Oliveira    | Email: pedro@example.com      | Criado em: 2024-01-15 10:30:00
============================================================

✓ Leitura concluída com sucesso!
Estes dados estão persistidos no volume Docker.
Mesmo que os containers sejam removidos, os dados permanecerão.
============================================================
```

## 🔍 Verificando a Persistência

### Teste 1: Remover Containers e Recriar

1. **Remover os containers**:
   ```bash
   docker-compose down
   ```

2. **Verificar que o volume ainda existe**:
   ```bash
   docker volume ls
   # Você verá: desafio2-db-data
   ```

3. **Recriar os containers**:
   ```bash
   docker-compose up
   ```

4. **Observar os logs**: O container `database` mostrará que já existem 3 registros e não inserirá novos dados. O container `reader` conseguirá ler os mesmos dados que foram criados anteriormente.

### Teste 2: Inspecionar o Volume

```bash
# Listar volumes
docker volume ls

# Inspecionar o volume
docker volume inspect desafio2-db-data

# Ver o caminho do volume no sistema de arquivos
docker volume inspect desafio2-db-data | grep Mountpoint
```

### Teste 3: Acessar o Volume Manualmente

```bash
# Criar um container temporário para acessar o volume
docker run --rm -v desafio2-db-data:/data -it python:3.11-slim /bin/bash

# Dentro do container, verificar o banco
ls -la /data/
sqlite3 /data/database.db "SELECT * FROM usuarios;"
```

## 🧪 Testes Manuais

### Executar apenas o container database

```bash
# Executar apenas o serviço database
docker-compose up database

# Em outro terminal, executar o reader
docker-compose up reader
```

### Adicionar mais dados manualmente

```bash
# Executar um container interativo com acesso ao volume
docker run --rm -v desafio2-db-data:/data -it python:3.11-slim /bin/bash

# Dentro do container
python3
```

```python
import sqlite3
from datetime import datetime

conn = sqlite3.connect('/data/database.db')
cursor = conn.cursor()

# Inserir novo registro
cursor.execute(
    'INSERT INTO usuarios (nome, email, data_criacao) VALUES (?, ?, ?)',
    ('Novo Usuário', 'novo@example.com', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
)
conn.commit()

# Verificar
cursor.execute('SELECT * FROM usuarios')
print(cursor.fetchall())

conn.close()
```

### Limpar o volume (remover todos os dados)

```bash
# Parar e remover containers
docker-compose down

# Remover o volume (CUIDADO: isso apaga todos os dados!)
docker volume rm desafio2-db-data

# Recriar tudo do zero
docker-compose up --build
```

## ⚙️ Configurações

### Alterar o caminho do banco de dados

Edite os arquivos `init_db.py` e `read_db.py` e modifique a variável `DB_PATH`:

```python
DB_PATH = '/data/meu_banco.db'  # Novo caminho
```

### Usar um volume bind mount (mapear para pasta local)

Edite o `docker-compose.yml`:

```yaml
services:
  database:
    volumes:
      - ./local-data:/data  # Mapeia para pasta local
```

Isso criará a pasta `local-data` no diretório atual e você poderá ver o arquivo `database.db` diretamente.

## 📝 Explicação Técnica

### Por que usar volumes Docker?

- **Persistência**: Dados sobrevivem à remoção de containers
- **Compartilhamento**: Múltiplos containers podem acessar os mesmos dados
- **Backup**: Fácil fazer backup dos volumes
- **Performance**: Volumes têm melhor performance que bind mounts em alguns casos

### Tipos de Volumes

1. **Named Volumes** (usado neste desafio):
   - Gerenciado pelo Docker
   - Melhor para produção
   - Localização: `/var/lib/docker/volumes/`

2. **Bind Mounts**:
   - Mapeia diretamente para uma pasta do host
   - Útil para desenvolvimento
   - Exemplo: `./pasta-local:/data`

3. **Anonymous Volumes**:
   - Criado automaticamente sem nome
   - Removido quando o container é removido (a menos que use `--rm`)

### Como funciona a persistência?

1. O Docker cria um volume nomeado `desafio2-db-data`
2. O volume é montado em `/data` dentro dos containers
3. Quando o banco de dados é criado, ele é salvo no volume
4. Mesmo removendo os containers, o volume permanece
5. Ao recriar os containers, o mesmo volume é montado novamente
6. Os dados anteriores estão disponíveis imediatamente

### Diferença entre volumes e sistema de arquivos do container

- **Sistema de arquivos do container**: É efêmero, perdido quando o container é removido
- **Volumes**: Persistem independentemente do ciclo de vida dos containers

## 🐛 Troubleshooting

### Container reader não encontra o banco de dados

1. Verifique se o container `database` foi executado primeiro:
   ```bash
   docker-compose logs database
   ```

2. Verifique se o volume foi criado:
   ```bash
   docker volume ls | grep desafio2
   ```

3. Verifique se ambos os containers estão usando o mesmo volume:
   ```bash
   docker-compose config
   ```

### Dados não persistem após remover containers

1. Verifique se você está usando `docker-compose down` (não `docker-compose down -v`):
   - `docker-compose down`: Remove containers mas mantém volumes
   - `docker-compose down -v`: Remove containers E volumes (apaga dados!)

2. Verifique se o volume existe:
   ```bash
   docker volume ls
   ```

### Erro de permissão ao acessar o volume

No Windows/Mac, isso geralmente não é um problema. No Linux, se houver problemas:

```bash
# Verificar permissões do volume
docker volume inspect desafio2-db-data
```

## 📚 Recursos Adicionais

- [Documentação Docker Volumes](https://docs.docker.com/storage/volumes/)
- [Documentação Docker Compose Volumes](https://docs.docker.com/compose/compose-file/compose-file-v3/#volumes)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Python sqlite3 Module](https://docs.python.org/3/library/sqlite3.html)

