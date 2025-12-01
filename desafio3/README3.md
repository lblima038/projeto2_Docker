# Desafio 3 — Docker Compose Orquestrando Serviços

## 📋 Objetivo

Usar Docker Compose para orquestrar múltiplos serviços dependentes (web, banco de dados e cache), configurando dependências, variáveis de ambiente e rede interna.

## 🏗️ Arquitetura da Solução

A solução consiste em 3 serviços principais:

1. **Serviço Web (`web`)**: Aplicação Flask que expõe uma API HTTP.
2. **Serviço de Banco de Dados (`db`)**: Banco PostgreSQL.
3. **Serviço de Cache (`cache`)**: Redis para armazenar contagem de visitas em memória.

Todos os serviços são orquestrados via `docker-compose.yml`, compartilham uma **rede interna** e usam `depends_on` para garantir a ordem básica de inicialização.

### Estrutura de Arquivos

```
desafio3/
├── web/
│   ├── Dockerfile
│   ├── app.py               # Aplicação Flask (web)
│   └── requirements.txt
├── docker-compose.yml       # Orquestração dos serviços (web, db, cache)
└── README3.md
```

## 🔧 Componentes

### Serviço Web (`web`)

- **Tecnologia**: Python + Flask.
- **Porta no container**: 5000.
- **Porta no host**: 8082 (mapeada para 5000).
- **Dependências externas**:
  - Banco de dados PostgreSQL (`db`);
  - Cache Redis (`cache`).
- **Variáveis de ambiente usadas** (definidas no `docker-compose.yml`):
  - `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`;
  - `REDIS_HOST`, `REDIS_PORT`.

#### Endpoints principais

- `GET /`  
  - Incrementa um contador de visitas no Redis (`visits_count`);
  - Registra a visita no banco Postgres (tabela `visits`);
  - Retorna JSON com:
    - Mensagem de status;
    - Número total de visitas (contador do Redis);
    - Data/hora da última visita.

- `GET /stats`  
  - Lê do banco de dados:
    - Total de visitas registradas;
    - Últimas 5 visitas;
  - Retorna essas informações em JSON.

- `GET /health`  
  - Verifica se o banco e o cache estão respondendo;
  - Retorna um JSON com o status de `web`, `db` e `cache`.

### Serviço de Banco de Dados (`db`)

- **Imagem**: `postgres:15-alpine`.
- **Banco**: `appdb`.
- **Usuário**: `appuser`.
- **Senha**: `apppassword`.
- **Volume**: `desafio3-db-data` montado em `/var/lib/postgresql/data` (persistência dos dados).
- **Função**:
  - Armazenar o histórico de visitas na tabela `visits`;
  - Permitir consultas pelo serviço web.

### Serviço de Cache (`cache`)

- **Imagem**: `redis:7-alpine`.
- **Porta interna**: 6379.
- **Função**:
  - Manter um contador de visitas em memória (`visits_count`);
  - Responder rapidamente à aplicação web.

### Rede Interna

- **Nome**: `desafio3-network`.
- **Tipo**: Bridge.
- **Comunicação**:
  - O serviço `web` acessa o banco via host `db` (DNS interno do Docker);
  - O serviço `web` acessa o cache via host `cache`.

## 🚀 Como Executar

### Pré-requisitos

- Docker instalado;
- Docker Compose instalado (geralmente vem com o Docker Desktop).

### Passos para Executar

1. **Navegue até a pasta do desafio**:

   ```bash
   cd desafio3
   ```

2. **Construir e iniciar os serviços**:

   ```bash
   docker-compose up --build
   ```

   Ou para rodar em background:

   ```bash
   docker-compose up -d --build
   ```

3. **Ver logs dos serviços**:

   ```bash
   # Logs de todos os serviços
   docker-compose logs -f

   # Apenas web
   docker-compose logs -f web

   # Apenas db
   docker-compose logs -f db

   # Apenas cache
   docker-compose logs -f cache
   ```

4. **Acessar o serviço web**:

   - Abra o navegador em: `http://localhost:8082/`
   - Ou via `curl`:

   ```bash
   curl http://localhost:8082/
   ```

5. **Ver estatísticas de visitas**:

   ```bash
   curl http://localhost:8082/stats
   ```

6. **Verificar saúde dos serviços**:

   ```bash
   curl http://localhost:8082/health
   ```

7. **Parar e remover containers (mantendo dados do banco)**:

   ```bash
   docker-compose down
   ```

## 📊 Demonstração da Comunicação entre Serviços

### Fluxo de uma requisição para `/`

1. O cliente (navegador ou `curl`) faz requisição para `http://localhost:8082/`;
2. O Docker encaminha para o container `web` na porta 5000;
3. A aplicação Flask:
   - Conecta ao Redis (`cache`) via host `cache:6379`;
   - Incrementa o contador `visits_count`;
   - Conecta ao Postgres (`db`) via host `db:5432`;
   - Insere um registro na tabela `visits` com data/hora da visita;
4. O serviço web retorna um JSON com informações da visita.

### Exemplo de resposta de `/`

```json
{
  "message": "Serviço web em execução com cache e banco de dados!",
  "visits_count": 3,
  "last_visit": "2024-01-15T10:30:00.123456Z"
}
```

### Exemplo de resposta de `/stats`

```json
{
  "total_visits": 3,
  "last_visits": [
    {
      "visited_at": "2024-01-15T10:30:00.123456Z",
      "message": "Visita número 3"
    },
    {
      "visited_at": "2024-01-15T10:29:58.000000Z",
      "message": "Visita número 2"
    }
  ]
}
```

## 🔍 Testando Comunicação entre os Serviços

### Testar comunicação web → db

1. Faça algumas requisições para `/`:

   ```bash
   curl http://localhost:8082/
   curl http://localhost:8082/
   ```

2. Acesse o container do banco:

   ```bash
   docker exec -it desafio3-db psql -U appuser -d appdb
   ```

3. Dentro do psql, rode:

   ```sql
   SELECT COUNT(*) FROM visits;
   SELECT * FROM visits ORDER BY visited_at DESC LIMIT 5;
   ```

Você verá os registros inseridos pela aplicação web.

### Testar comunicação web → cache

1. Acesse o container do Redis:

   ```bash
   docker exec -it desafio3-cache redis-cli
   ```

2. Dentro do Redis CLI, rode:

   ```redis
   GET visits_count
   ```

O valor retornado deve bater com o `visits_count` da resposta do endpoint `/`.

### Ver rede interna e containers conectados

```bash
# Listar redes
docker network ls

# Inspecionar rede do desafio
docker network inspect desafio3-network
```

## ⚙️ Arquivo docker-compose.yml (Resumo)

O arquivo `docker-compose.yml` define:

- **Serviço `web`**:
  - `build: ./web`;
  - `depends_on: [db, cache]`;
  - `environment` com variáveis para conexão ao banco e cache;
  - `ports: "8082:5000"`.

- **Serviço `db`** (Postgres):
  - `image: postgres:15-alpine`;
  - `environment` com `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`;
  - `volumes` para `desafio3-db-data`.

- **Serviço `cache`** (Redis):
  - `image: redis:7-alpine`.

- **Rede interna**:
  - Todos os serviços usam a rede `desafio3-network`.

## 📝 Explicação Técnica

### Por que usar Docker Compose aqui?

- **Orquestração simples**: subir vários serviços com um único comando;
- **Ambiente reproduzível**: mesma configuração para todos os desenvolvedores;
- **Rede interna automática**: serviços se enxergam pelos nomes (`web`, `db`, `cache`);
- **Isolamento**: serviços isolados do host e de outros projetos.

### Uso de `depends_on`

- Garante que os containers `db` e `cache` sejam iniciados **antes** do `web`;
- Importante: `depends_on` **não** garante que o serviço esteja pronto, apenas que o container foi iniciado;
- Em cenários reais, costuma-se usar healthchecks ou lógica de retry na aplicação para aguardar o banco/cache ficarem disponíveis.

### Rede interna e resolução de nomes

- Todos os containers conectados à rede `desafio3-network` têm um DNS interno;
- O host `db` resolve para o IP do container Postgres;
- O host `cache` resolve para o IP do container Redis;
- A aplicação Flask utiliza esses nomes de host para se conectar aos serviços.

## 🐛 Troubleshooting

### Erro de conexão com o banco de dados

1. Verifique logs do banco:

   ```bash
   docker-compose logs -f db
   ```

2. Acesse o container do web e teste conexão manualmente (opcional):

   ```bash
   docker exec -it desafio3-web /bin/bash
   # Dentro do container, ver variáveis de ambiente
   env | grep DB_
   ```

### Erro ao conectar no Redis

1. Verifique se o container `cache` está rodando:

   ```bash
   docker-compose ps
   ```

2. Veja os logs do cache:

   ```bash
   docker-compose logs -f cache
   ```

### Porta 8082 já está em uso

1. Edite o arquivo `docker-compose.yml`:

   ```yaml
   services:
     web:
       ports:
         - "8090:5000"  # altera a porta do host para 8090
   ```

2. Suba novamente os serviços:

   ```bash
   docker-compose down
   docker-compose up --build
   ```

## 📚 Recursos Adicionais

- [Documentação Docker Compose](https://docs.docker.com/compose/)
- [Documentação do Compose file](https://docs.docker.com/compose/compose-file/)
- [Documentação Flask](https://flask.palletsprojects.com/)
- [Documentação PostgreSQL](https://www.postgresql.org/docs/)
- [Documentação Redis](https://redis.io/documentation)


