# Dad Jokes App

## Sobre
Este projeto foi desenvolvido como parte do módulo de conteinerização do curso de DevOps da ADA. A aplicação Dad Jokes App foi criada em Python e Flask e tem como objetivo consumir piadas da API "Icanhazdajokes", armazená-las em um banco de dados MySQL e exibi-las em uma página web. A aplicação possui funcionalidades como obtenção de novas piadas, exibição da quantidade total de piadas disponíveis, um contador regressivo para a próxima busca automática de piadas e um controle de taxa para limitar as solicitações dos usuários.

## Requisitos do Projeto
Os requisitos para nosso projeto Docker são os seguintes:

Utilizar uma aplicação web de preferência na linguagem Python com Flask.
Criar um Dockerfile para a aplicação.
Criar um docker-compose.yaml com os seguintes requisitos:
Incluir um banco de dados (MySQL ou PostgreSQL) como um serviço.
Ter dois serviços no total:
O serviço da aplicação.
Um serviço de volume para persistência de dados do banco de dados.
Criar e referenciar uma network para conectar os serviços.
Garantir que os serviços da aplicação dependam do serviço do banco de dados.
Mostrar que a aplicação está funcionando na porta 80.

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
Creating network "dadjokes_myapp_network" with the default driver
Creating mysql_db ... done
Creating python-server ... done

```

Para conferirmos que ambos os aplicativos compartilham a mesma rede, podemos primeiro inspecionar as redes disponíveis e procurar pelo nome da rede que foi definido no nosso arquivo .yml:
````bash
docker network ls | grep dadjokes
f35e063c8334   dadjokes_myapp_network   bridge    local
````

Podemos então verificar os processos que estão em execução na rede:
````bash
docker ps --filter network=dadjokes_myapp_network
CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS                     PORTS                                                  NAMES
df19c35c0f51   dadjokes_app   "/bin/sh -c 'python …"   5 minutes ago   Up 5 minutes (unhealthy)   127.0.0.1:80->80/tcp                                   python-server
d67a47546c3f   mysql:latest   "docker-entrypoint.s…"   5 minutes ago   Up 5 minutes (healthy)     0.0.0.0:3306->3306/tcp, :::3306->3306/tcp, 33060/tcp   mysql_db
````

Como queríamos demonstrar.

Verifica-se que o volume foi criado da mesma maneira:
````bash
docker volume ls | grep dadjokes
local     dadjokes_db_data
````

Por fim, podemos verificar que a aplicação está funcionando conforme o esperado acessando http://localhost:80. No entanto, esse processo já foi automatizado na própria configuração do YML, como podemos ver aqui:
```yaml
    container_name: python-server
    environment:
      DB_HOST: mysql_db
      DB_NAME: myappdb
      DB_USER: ada
      DB_PASSWORD: test
    ports:
      -  127.0.0.1:80:80
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

A seção acima define uma dependência entre o serviço da aplicação e o serviço do banco de dados. A aplicação só iniciará após o serviço do banco de dados ser considerado saudável, isto é, caso o serviço do MySQL esteja em execução na máquina local (como você pode ver no mesmo campo de "health check" do serviço de banco de dados). Além disso, também verificamos a integridade da aplicação antes de executá-la, determinando se a rota do servidor do Flask está disponível por meio de uma requisição com curl. Isso significa que a imagem do Docker só iniciará a aplicação se for capaz de acessar a rota do servidor do Flask com sucesso, atendendo ao requisito de demonstrar que a aplicação está funcionando e acessível na porta 80.

Para parar e remover os contêineres da aplicação e limpar os volumes associados, execute o seguinte comando no diretório raiz do projeto:

````bash
docker-compose down -v
````


Isso vai parar todos os contêineres relacionados à aplicação e também removerá os volumes Docker associados. Lembre-se de que isso também excluirá todos os dados do banco de dados. Se quiser que os dados persistam, basta remover o `-v`.

Mesmo depois de remover os contêineres, a imagem Docker da aplicação ainda estará disponível localmente, permitindo que você a reconstrua e execute novamente a qualquer momento.

Agora você pode clonar o repositório, seguir as instruções do README e executar a aplicação com facilidade.