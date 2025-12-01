# Desafio 1 — Containers em Rede

## 📋 Objetivo

Criar dois containers Docker que se comunicam através de uma rede Docker customizada, demonstrando comunicação entre containers isolados.

## 🏗️ Arquitetura da Solução

A solução consiste em:

1. **Container Servidor (server)**: Um servidor web Flask rodando na porta 8080
2. **Container Cliente (client)**: Um script Python que faz requisições HTTP periódicas para o servidor
3. **Rede Docker Customizada**: Uma rede bridge nomeada `desafio-network` que conecta ambos os containers

### Estrutura de Arquivos

```
desafio1/
├── server/
│   ├── Dockerfile
│   ├── app.py              # Servidor Flask
│   └── requirements.txt
├── client/
│   ├── Dockerfile
│   ├── requester.py        # Script cliente
│   └── requirements.txt
├── docker-compose.yml      # Orquestração dos containers
└── README.md
```

## 🔧 Componentes

### Servidor Web (Flask)

- **Porta**: 8080
- **Endpoints**:
  - `GET /`: Retorna uma página HTML com informações do servidor
  - `GET /health`: Retorna status de saúde em JSON
- **Logs**: Exibe todas as requisições recebidas

### Cliente HTTP

- **Comportamento**: Faz requisições HTTP a cada 5 segundos (configurável)
- **Funcionalidades**:
  - Conecta ao servidor usando o nome do serviço (`server`)
  - Exibe logs detalhados de cada requisição
  - Mostra estatísticas de sucesso/falha
  - Tratamento de erros de conexão

### Rede Docker

- **Nome**: `desafio-network`
- **Tipo**: Bridge (padrão)
- **Comunicação**: Os containers se comunicam usando os nomes dos serviços definidos no `docker-compose.yml`

## 🚀 Como Executar

### Pré-requisitos

- Docker instalado
- Docker Compose instalado (geralmente vem com o Docker Desktop)

### Passos para Executar

1. **Navegue até a pasta do desafio**:
   ```bash
   cd desafio1
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
   
   # Logs apenas do servidor
   docker-compose logs -f server
   
   # Logs apenas do cliente
   docker-compose logs -f client
   ```

4. **Acessar o servidor diretamente**:
   Abra seu navegador e acesse: `http://localhost:8080`

5. **Parar os containers**:
   ```bash
   docker-compose down
   ```

## 📊 Demonstração da Comunicação

### Logs do Servidor

O servidor exibirá logs como:
```
Servidor Flask iniciando na porta 8080...
Aguardando requisições...
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://172.18.0.2:8080
```

### Logs do Cliente

O cliente exibirá logs como:
```
============================================================
Cliente de Requisições HTTP - Iniciando...
Servidor: http://server:8080
Intervalo: 5 segundos
============================================================

--- Requisição #1 ---
[2024-01-15 10:30:00] Fazendo requisição para http://server:8080...
[2024-01-15 10:30:00] ✓ Resposta recebida - Status: 200
[2024-01-15 10:30:00] ✓ Conteúdo: <html>...
Estatísticas: 1/1 requisições bem-sucedidas
Aguardando 5 segundos até a próxima requisição...
```

## 🔍 Verificando a Rede Docker

Para inspecionar a rede criada:

```bash
# Listar redes
docker network ls

# Inspecionar a rede desafio-network
docker network inspect desafio-network

# Ver containers conectados
docker network inspect desafio-network | grep -A 10 "Containers"
```

## 🧪 Testes Manuais

### Testar o servidor diretamente

```bash
# A partir do host
curl http://localhost:8080

# A partir de outro container (se necessário)
docker run --rm --network desafio-network curlimages/curl:latest curl http://server:8080
```

### Verificar conectividade entre containers

```bash
# Executar um shell no container cliente
docker exec -it desafio1-client /bin/bash

# Dentro do container, testar conectividade
ping server
curl http://server:8080
```

## ⚙️ Configurações

### Alterar intervalo de requisições

Edite o arquivo `docker-compose.yml` e modifique a variável `INTERVAL`:

```yaml
environment:
  - INTERVAL=10  # Requisições a cada 10 segundos
```

### Alterar porta do servidor

Edite o arquivo `docker-compose.yml`:

```yaml
ports:
  - "9090:8080"  # Mapeia porta 9090 do host para 8080 do container
```

## 📝 Explicação Técnica

### Por que usar uma rede customizada?

- **Isolamento**: Containers na mesma rede podem se comunicar pelo nome do serviço
- **Segurança**: Containers fora da rede não têm acesso
- **Organização**: Facilita o gerenciamento de múltiplos containers relacionados

### Como funciona a comunicação?

1. O Docker Compose cria uma rede bridge chamada `desafio-network`
2. Ambos os containers são conectados a essa rede
3. O Docker fornece um DNS interno que resolve o nome `server` para o IP do container servidor
4. O cliente faz requisições para `http://server:8080`, que é resolvido automaticamente pelo DNS do Docker

### Diferença entre `localhost` e nome do serviço

- **`localhost`**: Refere-se ao próprio container
- **`server`**: Refere-se ao container do serviço `server` na mesma rede (resolvido pelo DNS do Docker)

## 🐛 Troubleshooting

### Container cliente não consegue conectar

1. Verifique se ambos os containers estão na mesma rede:
   ```bash
   docker network inspect desafio-network
   ```

2. Verifique se o servidor está rodando:
   ```bash
   docker-compose ps
   ```

3. Verifique os logs do servidor:
   ```bash
   docker-compose logs server
   ```

### Porta 8080 já está em uso

Altere a porta no `docker-compose.yml`:
```yaml
ports:
  - "8081:8080"  # Use 8081 no host
```

## 📚 Recursos Adicionais

- [Documentação Docker Networking](https://docs.docker.com/network/)
- [Documentação Docker Compose](https://docs.docker.com/compose/)
- [Flask Documentation](https://flask.palletsprojects.com/)

