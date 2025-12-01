# Desafio 4 — Microsserviços Independentes

## 📋 Objetivo

Criar dois microsserviços independentes que se comunicam via HTTP, cada um com seu próprio Dockerfile e executáveis de forma separada.

## 🏗️ Arquitetura da Solução

A solução consiste em:

1. **Microsserviço A (`service-a`)**: expõe uma API HTTP que retorna uma lista de usuários em JSON.
2. **Microsserviço B (`service-b`)**: consome o serviço A via HTTP e expõe um endpoint que retorna frases combinadas sobre os usuários.

Não há API Gateway ainda: a comunicação é direta entre os serviços via HTTP.

### Estrutura de Arquivos

```
desafio4/
├── service-a/
│   ├── Dockerfile
│   ├── app.py              # Microsserviço A - lista de usuários
│   └── requirements.txt
├── service-b/
│   ├── Dockerfile
│   ├── app.py              # Microsserviço B - consome A e monta frases
│   └── requirements.txt
└── README4.md
```

## 🔧 Microsserviços

### Microsserviço A (`service-a`)

- **Tecnologia**: Python + Flask.
- **Porta interna**: 5000.
- **Responsabilidade**: fornecer uma lista de usuários em JSON.

#### Endpoints

- `GET /users`  
  Retorna uma lista fixa de usuários:

  ```json
  [
    { "id": 1, "name": "João Silva", "active_since": "2021-01-10" },
    { "id": 2, "name": "Maria Santos", "active_since": "2022-03-05" },
    { "id": 3, "name": "Pedro Oliveira", "active_since": "2020-07-22" }
  ]
  ```

- `GET /health`  
  Retorna o status básico do serviço:

  ```json
  { "status": "ok", "service": "service-a" }
  ```

### Microsserviço B (`service-b`)

- **Tecnologia**: Python + Flask + Requests.
- **Porta interna**: 5001.
- **Responsabilidade**: consumir o microsserviço A e expor informações combinadas em forma de frases.
- **Variáveis de ambiente**:
  - `SERVICE_A_URL` (opcional, padrão: `http://service-a:5000`).

#### Endpoints

- `GET /users/summary`  
  - Faz uma requisição HTTP para `SERVICE_A_URL + /users`;
  - Lê a lista de usuários retornada por A;
  - Monta frases como:
    - `"Usuário João Silva ativo desde 2021-01-10"`;
    - `"Usuário Maria Santos ativo desde 2022-03-05"`;
  - Resposta aproximada:

  ```json
  {
    "source": "http://service-a:5000/users",
    "count": 3,
    "summaries": [
      "Usuário João Silva ativo desde 2021-01-10",
      "Usuário Maria Santos ativo desde 2022-03-05",
      "Usuário Pedro Oliveira ativo desde 2020-07-22"
    ]
  }
  ```

- `GET /health`  
  Retorna o status básico do serviço:

  ```json
  { "status": "ok", "service": "service-b" }
  ```

## 🚀 Como Executar (usando docker run)

Aqui vamos rodar os dois serviços de forma independente, apenas usando a rede Docker para eles se enxergarem.

### 1. Criar uma rede Docker

```bash
docker network create desafio4-network
```

### 2. Construir as imagens

Na raiz de `desafio4`:

```bash
# Microsserviço A
docker build -t desafio4-service-a ./service-a

# Microsserviço B
docker build -t desafio4-service-b ./service-b
```

### 3. Subir o microsserviço A

```bash
docker run --rm -d \
  --name service-a \
  --network desafio4-network \
  -p 5000:5000 \
  desafio4-service-a
```

Testar A diretamente:

```bash
curl http://localhost:5000/users
curl http://localhost:5000/health
```

### 4. Subir o microsserviço B

```bash
docker run --rm -d \
  --name service-b \
  --network desafio4-network \
  -p 5001:5001 \
  -e SERVICE_A_URL=http://service-a:5000 \
  desafio4-service-b
```

Testar B:

```bash
curl http://localhost:5001/users/summary
curl http://localhost:5001/health
```

### 5. Parar os serviços

```bash
docker stop service-b
docker stop service-a
```

## 🧪 Testes de Comunicação HTTP

### Testar que o B realmente consome o A

1. Com ambos rodando, faça:

   ```bash
   curl http://localhost:5001/users/summary
   ```

2. Em outro terminal, veja os logs do `service-a`:

   ```bash
   docker logs service-a
   ```

Você deverá ver requisições chegando em `/users` sempre que chamar `/users/summary` no serviço B.

### Testar erro quando A está desligado

1. Pare o serviço A:

   ```bash
   docker stop service-a
   ```

2. Chame o endpoint de B:

   ```bash
   curl http://localhost:5001/users/summary
   ```

O serviço B deverá retornar um JSON de erro (HTTP 502) informando que não conseguiu acessar o serviço A.

## ⚙️ Rodando sem rede customizada (apenas para testes simples)

Você também pode rodar os serviços apontando diretamente para `localhost`:

1. Subir A no host:

   ```bash
   docker run --rm -d \
     --name service-a \
     -p 5000:5000 \
     desafio4-service-a
   ```

2. Subir B apontando para `http://host.docker.internal:5000` (no Docker Desktop):

   ```bash
   docker run --rm -d \
     --name service-b \
     -p 5001:5001 \
     -e SERVICE_A_URL=http://host.docker.internal:5000 \
     desafio4-service-b
   ```

> Em Linux, seria necessário apontar o IP do host manualmente ou usar uma rede bridge e se comunicar via nome do container.

## 📝 Explicação Técnica

### Microsserviços independentes

- Cada serviço:
  - Tem seu próprio código (`app.py`);
  - Tem suas próprias dependências (`requirements.txt`);
  - Tem seu próprio `Dockerfile`;
  - Pode ser versionado, escalado e implantado separadamente.

### Comunicação via HTTP

- O microsserviço B não acessa diretamente o banco de dados do A nem o código interno;
- A única dependência entre eles é o **contrato da API HTTP** (`GET /users`);
- Isso facilita:
  - Evoluir o serviço A sem quebrar o B (desde que o contrato seja mantido);
  - Trocar a implementação interna de A (banco, linguagem, etc.) sem impactar o consumidor.

### Sem API Gateway (ainda)

- A comunicação é direta:
  - Cliente → B;
  - B → A.
- Em arquiteturas maiores, um API Gateway poderia:
  - Centralizar autenticação, rate limiting, logging, etc.;
  - Fazer roteamento para vários microsserviços.

## 📚 Recursos Adicionais

- [Documentação Flask](https://flask.palletsprojects.com/)
- [Documentação Docker](https://docs.docker.com/)
- [Docker Networking](https://docs.docker.com/network/)
- [Patterns de Microsserviços](https://microservices.io/)


