# Dad Jokes App

## Sobre

Este projeto foi desenvolvido como parte do módulo de conteinerização do curso de DevOps da ADA. A aplicação Dad Jokes App foi criada em Python e Flask e tem como objetivo consumir piadas da API "Icanhazdajokes", armazená-las em um banco de dados MySQL e exibi-las em uma página web.

## Requisitos do Projeto

Os requisitos para nosso projeto Docker são os seguintes:

- Utilizar uma aplicação web de preferência.
- Criar um Dockerfile para a aplicação.
- Criar um docker-compose.yaml com os seguintes requisitos:
- Incluir um banco de dados (MySQL ou PostgreSQL) como um serviço.
- Ter dois serviços no total: o serviço da aplicação e o banco de dados.
- Criar um volume para persistência de dados do banco de dados.
- Criar e referenciar uma rede para interligar os serviços.
- Garantir que os serviços da aplicação dependam do serviço do banco de dados.
- Mostrar que a aplicação está funcionando na porta 80.

## Como rodar a aplicação

- Clone este repositório para o seu ambiente de desenvolvimento.

- Certifique-se de ter o Docker e o Docker Compose instalados na sua máquina.

- Abra um terminal e navegue até o diretório raiz do projeto.

- Execute o seguinte comando para construir a imagem Docker:
```bash
docker-compose build
```
Após a construção bem-sucedida da imagem, execute os contêineres com o comando:

```bash
docker-compose up -d
```
Se tudo tiver dado certo, você verá o seguinte resultado:
```bash
Creating network "ada_docker_myapp_network" with the default driver
Creating volume "ada_docker_db_data" with default driver
Creating mysql_db ... done
Creating python-server ... done

```

Para conferirmos que ambos os aplicativos compartilham a mesma rede, podemos primeiro inspecionar as redes disponíveis e procurar pelo nome da rede:
````bash
$ docker network ls
NETWORK ID     NAME                       DRIVER    SCOPE
d61447f35c71   ada_docker_myapp_network   bridge    local
````

Podemos em seguida verificar os processos que estão em execução nessa mesma rede e verificar que há dois serviços que compartilham dela:
````bash
$ docker ps --filter network=ada_docker_myapp_network
CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS                     PORTS                                                  NAMES
df19c35c0f51   adadocker_app   "/bin/sh -c 'python …"   5 minutes ago   Up 5 minutes (unhealthy)   127.0.0.1:80->80/tcp                                   python-server
d67a47546c3f   mysql:latest   "docker-entrypoint.s…"   5 minutes ago   Up 5 minutes (healthy)     0.0.0.0:3306->3306/tcp, :::3306->3306/tcp, 33060/tcp   mysql_db
````

Como queríamos demonstrar.

Comprova-se que o volume foi criado da mesma maneira:
````bash
$ docker volume ls
DRIVER    VOLUME NAME
local     ada_docker_db_data
````

Por fim, podemos verificar que a aplicação está funcionando conforme o esperado acessando http://localhost:80. No entanto, esse processo já foi automatizado na própria configuração do YML, como podemos ver aqui nesta seção do serviço do aplicativo:
```yaml
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
        test: ["CMD-SHELL", "curl -f http://localhost:80/jokes"]
        interval: 10s
        timeout: 5s
        retries: 3
    volumes:
     - .:/app
```

O código acima define uma dependência entre o serviço da aplicação e o serviço do banco de dados. A aplicação só iniciará após o serviço do banco de dados ser considerado saudável, isto é, caso o serviço do MySQL esteja em execução na máquina local (como definido na mesma seção do serviço de banco de dados no arquivo de compose). Além disso, também verificamos a integridade da aplicação antes de executá-la, determinando se a rota do servidor do Flask está disponível por meio de uma requisição com curl. Isso significa que a imagem do Docker só iniciará a aplicação se for capaz de acessar a rota do servidor do Flask com sucesso, atendendo ao requisito de demonstrar que a aplicação está funcionando e acessível na porta 80:

![image](https://github.com/mdgjohnny/ada_docker/assets/55006172/25c11213-b7a1-4df7-82bb-52859e38d784)


Se quiser parar os processos e remover os contêineres da aplicação, limpando os volumes associados, execute o seguinte comando no diretório raiz do projeto:

````bash
docker-compose down -v
````

Isso vai desmontar todos os contêineres relacionados à aplicação e também remover os volumes Docker associados. Lembre-se de que isso também exclui todos os dados obtidos anteriormente. Se quiser que os dados persistam, basta remover o `-v`. De todo modo, a imagem Docker da aplicação ainda estará disponível localmente, permitindo que você a reconstrua e execute novamente a qualquer momento.
