# Projeto Docker - Microsserviços e Containers

## 📖 Sobre o Projeto

Este projeto contém uma série de desafios práticos para aprender Docker, Docker Compose e arquitetura de microsserviços. Cada desafio apresenta conceitos progressivos, desde comunicação básica entre containers até arquiteturas complexas com API Gateway.

## 🎯 Objetivos de Aprendizado

- Compreender containers Docker e isolamento de aplicações
- Trabalhar com redes Docker e comunicação entre containers
- Utilizar Docker Compose para orquestração de múltiplos serviços
- Implementar arquiteturas de microsserviços
- Entender padrões como API Gateway

## 📚 Desafios Disponíveis

### Desafio 1 — Containers em Rede
**Conceitos**: Comunicação entre containers, redes Docker customizadas  
**Descrição**: Dois containers (servidor e cliente) se comunicam através de uma rede Docker.

### Desafio 2 — Aplicação com Banco de Dados
**Conceitos**: Volumes Docker, persistência de dados, multi-stage builds  
**Descrição**: Aplicação que lê dados de um banco de dados SQLite em um volume Docker.

### Desafio 3 — Aplicação Web com Docker Compose
**Conceitos**: Docker Compose, orquestração de serviços  
**Descrição**: Aplicação web simples orquestrada com Docker Compose.

### Desafio 4 — Microsserviços Independentes
**Conceitos**: Microsserviços, comunicação HTTP entre serviços  
**Descrição**: Dois microsserviços independentes que se comunicam via HTTP.

### Desafio 5 — Microsserviços com API Gateway
**Conceitos**: API Gateway, centralização de acesso, orquestração de chamadas  
**Descrição**: Arquitetura com API Gateway centralizando o acesso a dois microsserviços (usuários e pedidos).

## 🚀 Como Executar um Desafio

### Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Docker**: [Instalar Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: Geralmente vem junto com o Docker Desktop

Para verificar se estão instalados:

```bash
docker --version
docker-compose --version
```

### Passo a Passo

1. **Navegue até a pasta do desafio desejado:**

   ```bash
   cd desafio[NÚMERO]
   ```

   Por exemplo:
   ```bash
   cd desafio5
   ```

2. **Leia a documentação do desafio:**

   Cada desafio possui um arquivo `README[NÚMERO].md` com explicações detalhadas:
   
   ```bash
   # No Windows (PowerShell)
   cat README5.md
   
   # Ou abra o arquivo no seu editor
   ```

3. **Execute o desafio:**

   A maioria dos desafios usa Docker Compose. Para executar:

   ```bash
   docker-compose up --build
   ```

   O parâmetro `--build` garante que as imagens sejam construídas antes de iniciar.

   Para executar em background (detached mode):

   ```bash
   docker-compose up -d --build
   ```

4. **Teste os endpoints ou funcionalidades:**

   Cada desafio possui instruções específicas de teste no seu README.

5. **Parar os serviços:**

   ```bash
   docker-compose down
   ```

## 💡 Exemplo Prático: Desafio 5

Vamos executar o **Desafio 5 — Microsserviços com API Gateway** como exemplo completo:

### 1. Navegar até a pasta

```bash
cd desafio5
```

### 2. Subir os serviços

```bash
docker-compose up --build
```

Você verá os logs dos três serviços sendo iniciados:
- `service-users` (microsserviço de usuários)
- `service-orders` (microsserviço de pedidos)
- `gateway` (API Gateway)

### 3. Verificar se os containers estão rodando

Em outro terminal:

```bash
docker-compose ps
```

Você deve ver três containers com status "Up".

### 4. Testar os endpoints

O gateway expõe a porta **8080**. Teste os endpoints:

```bash
# Listar todos os usuários
curl http://localhost:8080/users

# Listar todos os pedidos
curl http://localhost:8080/orders

# Obter um usuário específico
curl http://localhost:8080/users/1

# Obter pedidos de um usuário
curl http://localhost:8080/orders/user/1

# Health check do gateway e serviços
curl http://localhost:8080/health
```

### 5. Ver os logs

Para acompanhar o que está acontecendo:

```bash
# Logs de todos os serviços
docker-compose logs

# Logs apenas do gateway
docker-compose logs gateway

# Logs em tempo real (follow)
docker-compose logs -f
```

### 6. Parar os serviços

Quando terminar:

```bash
docker-compose down
```

Para remover também os volumes (se houver):

```bash
docker-compose down -v
```

## 📖 Documentação Detalhada

Cada desafio possui sua própria documentação completa:

- `desafio1/README1.md` - Containers em Rede
- `desafio2/README2.md` - Aplicação com Banco de Dados
- `desafio3/README3.md` - Aplicação Web com Docker Compose
- `desafio4/README4.md` - Microsserviços Independentes
- `desafio5/README5.md` - Microsserviços com API Gateway

## 🔧 Comandos Úteis

### Docker Compose

```bash
# Subir serviços
docker-compose up

# Subir em background
docker-compose up -d

# Reconstruir imagens
docker-compose up --build

# Parar serviços
docker-compose down

# Ver logs
docker-compose logs

# Ver status dos containers
docker-compose ps

# Executar comando em um container
docker-compose exec [SERVIÇO] [COMANDO]
```

### Docker

```bash
# Listar containers rodando
docker ps

# Listar todas as imagens
docker images

# Ver logs de um container
docker logs [CONTAINER_NAME]

# Entrar em um container
docker exec -it [CONTAINER_NAME] /bin/bash

# Limpar recursos não utilizados
docker system prune
```

## 📚 Recursos Adicionais

- [Documentação Docker](https://docs.docker.com/)
- [Documentação Docker Compose](https://docs.docker.com/compose/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Microservices Patterns](https://microservices.io/)

## 📝 Estrutura do Projeto

```
projeto2_Docker/
├── desafio1/          # Containers em Rede
├── desafio2/          # Aplicação com Banco de Dados
├── desafio3/          # Aplicação Web com Docker Compose
├── desafio4/          # Microsserviços Independentes
├── desafio5/          # Microsserviços com API Gateway
└── README.md          # Este arquivo
```

---

**Bons estudos! 🐳**

