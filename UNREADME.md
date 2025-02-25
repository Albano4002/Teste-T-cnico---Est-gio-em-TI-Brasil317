# Projeto de Web Scraping com Selenium, PostgreSQL e Docker

Este projeto coleta informações das notícias do site Globo.com usando Selenium e insere os dados (títulos e links) em um banco de dados PostgreSQL. Todo o ambiente é executado em containers Docker para facilitar a instalação e a execução.

## Requisitos

- **Docker** e **Docker Compose** instalados e funcionando.
- (Opcional) Caso queira rodar o scraper sem Docker, é necessário ter o **Python 3** e o **PostgreSQL** instalados.
- Internet para acessar o site e baixar as imagens do Docker Hub.

## Estrutura do Projeto

```
meu-scraper/
├── scraper.py           # Código do scraper que coleta as notícias e insere no banco
├── schema.sql           # Script SQL para criação da tabela 'noticias'
├── Dockerfile           # Configuração do container Python com o scraper
├── docker-compose.yml   # Definição dos serviços (PostgreSQL e scraper)
└── README.md            # Este arquivo com instruções de execução
```

## Como Rodar o Projeto

### 1. Usando Docker Compose

Este método executa automaticamente tanto o banco de dados PostgreSQL quanto o scraper.

1. **Verifique se o Docker está rodando**

   Abra um terminal e execute:
   ```sh
   docker info
   ```
   Se o Docker estiver ativo, serão exibidas informações sobre o daemon.

2. **Suba os containers do projeto**

   No diretório do projeto, execute:
   ```sh
   docker-compose up --build
   ```
   Esse comando:
   - Constrói a imagem do scraper (usando o Dockerfile).
   - Inicia o container do PostgreSQL.
   - Executa o script `scraper.py` no container do scraper, que coleta as notícias e insere os dados no banco.

3. **Verificar os dados inseridos**

   Para acessar o PostgreSQL e verificar os dados:
   ```sh
   docker exec -it meu_postgres psql -U meuusuario -d meubanco
   ```
   No prompt do PostgreSQL, execute:
   ```sql
   SELECT * FROM noticias;
   ```

4. **Encerrar os containers**

   Quando desejar parar o projeto, pressione `Ctrl + C` no terminal onde o Docker Compose está rodando ou execute:
   ```sh
   docker-compose down
   ```

### 2. Rodar o Scraper Diretamente (Sem Docker)

Se preferir rodar o scraper diretamente no seu ambiente (desde que o PostgreSQL já esteja em execução):

1. **Certifique-se de que o PostgreSQL está rodando**

   Pode ser no seu sistema ou em um container Docker.

2. **Execute o scraper**

   No terminal, execute:
   ```sh
   python scraper.py
   ```
   O script abrirá o navegador em modo headless, coletará as notícias e inserirá os dados no banco de dados.

## Problemas Comuns

- **Erro de conexão com o PostgreSQL:**  
  Verifique se o serviço do PostgreSQL está rodando e se as credenciais (nome do banco, usuário, senha e host) estão corretas no `scraper.py`.

- **Erros de SSL ou Encoding:**  
  O `scraper.py` foi configurado para ignorar erros de SSL e tratar problemas de encoding. Caso persistam, revise as opções de `chrome_options` e o tratamento dos dados extraídos.

- **Arquivo `scraper.py` não encontrado:**  
  Certifique-se de que o arquivo esteja no diretório correto e que o Dockerfile o copie para o container.