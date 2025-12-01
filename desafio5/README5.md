# Desafio 5 — Microsserviços com API Gateway

## 📋 Objetivo

Criar uma arquitetura com API Gateway centralizando o acesso a dois microsserviços: um de usuários e outro de pedidos.

## 🏗️ Arquitetura da Solução

A solução consiste em:

1. **Microsserviço de Usuários (`service-users`)**: fornece dados de usuários através de uma API HTTP.
2. **Microsserviço de Pedidos (`service-orders`)**: fornece dados de pedidos através de uma API HTTP.
3. **API Gateway (`gateway`)**: centraliza o acesso aos microsserviços, expondo endpoints `/users` e `/orders` que orquestram as chamadas aos serviços.

Todos os serviços rodam em containers Docker orquestrados via `docker-compose`.

### Estrutura de Arquivos

```
desafio5/
├── service-users/
│   ├── Dockerfile
│   ├── app.py              # Microsserviço de usuários
│   └── requirements.txt
├── service-orders/
│   ├── Dockerfile
│   ├── app.py              # Microsserviço de pedidos
│   └── requirements.txt
├── gateway/
│   ├── Dockerfile
│   ├── app.py              # API Gateway
│   └── requirements.txt
├── docker-compose.yml      # Orquestração dos serviços
└── README5.md
```

## 🔧 Microsserviços

### Microsserviço de Usuários (`service-users`)

- **Tecnologia**: Python + Flask
- **Porta interna**: 5000
- **Responsabilidade**: fornecer dados de usuários

#### Endpoints

- `GET /users`  
  Retorna lista de todos os usuários:

  ```json
  [
    {
      "id": 1,
      "name": "João Silva",
      "email": "joao.silva@email.com",
      "active_since": "2021-01-10"
    },
    {
      "id": 2,
      "name": "Maria Santos",
      "email": "maria.santos@email.com",
      "active_since": "2022-03-05"
    }
  ]
  ```

- `GET /users/<id>`  
  Retorna um usuário específico por ID

- `GET /health`  
  Retorna o status do serviço:

  ```json
  { "status": "ok", "service": "service-users" }
  ```

### Microsserviço de Pedidos (`service-orders`)

- **Tecnologia**: Python + Flask
- **Porta interna**: 5001
- **Responsabilidade**: fornecer dados de pedidos

#### Endpoints

- `GET /orders`  
  Retorna lista de todos os pedidos:

  ```json
  [
    {
      "id": 1,
      "user_id": 1,
      "product": "Notebook Dell",
      "amount": 3500.00,
      "status": "delivered",
      "date": "2024-01-15"
    },
    {
      "id": 2,
      "user_id": 1,
      "product": "Mouse Logitech",
      "amount": 150.00,
      "status": "delivered",
      "date": "2024-02-10"
    }
  ]
  ```

- `GET /orders/<id>`  
  Retorna um pedido específico por ID

- `GET /orders/user/<user_id>`  
  Retorna todos os pedidos de um usuário específico

- `GET /health`  
  Retorna o status do serviço:

  ```json
  { "status": "ok", "service": "service-orders" }
  ```

## 🌐 API Gateway

- **Tecnologia**: Python + Flask + Requests
- **Porta exposta**: 8080
- **Responsabilidade**: centralizar e orquestrar chamadas aos microsserviços

### Endpoints do Gateway

O gateway expõe os seguintes endpoints que fazem proxy para os microsserviços:

#### Usuários

- `GET /users`  
  Retorna lista de usuários (proxy para `service-users`)

- `GET /users/<id>`  
  Retorna um usuário específico (proxy para `service-users`)

#### Pedidos

- `GET /orders`  
  Retorna lista de pedidos (proxy para `service-orders`)

- `GET /orders/<id>`  
  Retorna um pedido específico (proxy para `service-orders`)

- `GET /orders/user/<user_id>`  
  Retorna pedidos de um usuário (proxy para `service-orders`)

#### Health Check

- `GET /health`  
  Retorna o status do gateway e verifica a saúde dos microsserviços:

  ```json
  {
    "status": "ok",
    "service": "gateway",
    "services": {
      "users": { "status": "ok", "service": "service-users" },
      "orders": { "status": "ok", "service": "service-orders" }
    }
  }
  ```

## 🚀 Como Executar

### Pré-requisitos

- Docker instalado
- Docker Compose instalado

### Executando com Docker Compose

1. **Navegue até a pasta do desafio:**

   ```bash
   cd desafio5
   ```

2. **Suba todos os serviços:**

   ```bash
   docker-compose up --build
   ```

   Ou para rodar em background:

   ```bash
   docker-compose up -d --build
   ```

3. **Verifique se os containers estão rodando:**

   ```bash
   docker-compose ps
   ```

   Você deve ver três containers:
   - `desafio5-gateway`
   - `desafio5-service-users`
   - `desafio5-service-orders`

### Testando os Endpoints

Todos os endpoints devem ser acessados através do **Gateway** na porta **8080**:

#### Testando Usuários

```bash
# Listar todos os usuários
curl http://localhost:8080/users

# Obter usuário específico
curl http://localhost:8080/users/1

# Obter usuário inexistente (deve retornar 404)
curl http://localhost:8080/users/999
```

#### Testando Pedidos

```bash
# Listar todos os pedidos
curl http://localhost:8080/orders

# Obter pedido específico
curl http://localhost:8080/orders/1

# Obter pedidos de um usuário
curl http://localhost:8080/orders/user/1
```

#### Testando Health Check

```bash
# Health check do gateway e serviços
curl http://localhost:8080/health
```

### Acessando os Microsserviços Diretamente (Opcional)

Os microsserviços não expõem portas externamente, mas você pode acessá-los dentro da rede Docker:

```bash
# Acessar service-users diretamente (dentro da rede)
docker exec desafio5-gateway curl http://service-users:5000/users

# Acessar service-orders diretamente (dentro da rede)
docker exec desafio5-gateway curl http://service-orders:5001/orders
```

### Parando os Serviços

```bash
# Parar os serviços
docker-compose down

# Parar e remover volumes (se houver)
docker-compose down -v
```

## 🧪 Testes de Integração

### Teste 1: Gateway orquestra chamadas aos microsserviços

1. Faça uma requisição ao gateway:

   ```bash
   curl http://localhost:8080/users
   ```

2. Verifique os logs do gateway:

   ```bash
   docker-compose logs gateway
   ```

3. Verifique os logs do service-users:

   ```bash
   docker-compose logs service-users
   ```

   Você deve ver que a requisição passou pelo gateway e foi encaminhada ao service-users.

### Teste 2: Gateway retorna erro quando microsserviço está indisponível

1. Pare o service-users:

   ```bash
   docker-compose stop service-users
   ```

2. Faça uma requisição ao gateway:

   ```bash
   curl http://localhost:8080/users
   ```

   O gateway deve retornar um erro 502 indicando que não conseguiu comunicar com o serviço.

3. Verifique o health check:

   ```bash
   curl http://localhost:8080/health
   ```

   O serviço `users` deve aparecer como `unavailable`.

4. Reinicie o service-users:

   ```bash
   docker-compose start service-users
   ```

### Teste 3: Gateway funciona mesmo com um serviço parado

1. Pare apenas o service-orders:

   ```bash
   docker-compose stop service-orders
   ```

2. Teste endpoints de usuários (devem funcionar):

   ```bash
   curl http://localhost:8080/users
   ```

3. Teste endpoints de pedidos (devem retornar erro):

   ```bash
   curl http://localhost:8080/orders
   ```

## 📝 Explicação Técnica

### Arquitetura de API Gateway

O API Gateway é um padrão arquitetural que:

- **Centraliza o acesso**: todos os clientes acessam os microsserviços através de um único ponto de entrada
- **Desacopla clientes dos serviços**: os clientes não precisam conhecer as URLs internas dos microsserviços
- **Facilita mudanças**: se um microsserviço mudar de porta ou URL, apenas o gateway precisa ser atualizado
- **Permite adicionar funcionalidades**: autenticação, rate limiting, logging, etc., podem ser adicionados no gateway

### Comunicação entre Serviços

- **Gateway → Microsserviços**: O gateway faz requisições HTTP para os microsserviços usando os nomes dos containers (`service-users`, `service-orders`)
- **Rede Docker**: Todos os serviços estão na mesma rede Docker (`desafio5-network`), permitindo comunicação interna
- **Isolamento**: Os microsserviços não expõem portas externamente, apenas o gateway é acessível do host

### Benefícios desta Arquitetura

1. **Segurança**: Microsserviços não são expostos diretamente à internet
2. **Simplicidade**: Clientes só precisam conhecer uma URL (do gateway)
3. **Flexibilidade**: Fácil adicionar novos microsserviços ou modificar rotas
4. **Monitoramento**: Centralizado no gateway
5. **Escalabilidade**: Cada microsserviço pode ser escalado independentemente

## 🔍 Estrutura do Docker Compose

O `docker-compose.yml` define:

- **3 serviços**: `service-users`, `service-orders`, `gateway`
- **1 rede**: `desafio5-network` (bridge) para comunicação interna
- **Health checks**: Verificação automática da saúde dos serviços
- **Dependências**: Gateway depende dos microsserviços (usando `depends_on`)
- **Restart policies**: Serviços reiniciam automaticamente em caso de falha

## 📚 Recursos Adicionais

- [Documentação Flask](https://flask.palletsprojects.com/)
- [Documentação Docker Compose](https://docs.docker.com/compose/)
- [API Gateway Pattern](https://microservices.io/patterns/apigateway.html)
- [Docker Networking](https://docs.docker.com/network/)

