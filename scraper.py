from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep
import psycopg2
import os
from tabulate import tabulate
from datetime import datetime

def setup_webdriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Não visualizar o navegador
    chrome_options.add_argument("--ignore-certificate-errors")  # Ignora erros SSL
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    # Inicializa o WebDriver usando WebDriver Manager
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def scrape_data(nav):
    # Acessa o site
    nav.get('https://www.globo.com/')
    sleep(2)
    
    # Encontra os elementos por classe
    # Verifique a classe correta inspecionando o site
    noticias = nav.find_elements(By.CLASS_NAME, "post__link")
    
    # Armazena os dados extraídos
    dados = []
    for noticia in noticias:
        try:
            link = noticia.get_attribute("href")
            titulo_element = noticia.find_element(By.CLASS_NAME, "post__title")
            titulo = titulo_element.text.strip()
            
            if titulo and link:
                # Tratamento para garantir que os textos sejam UTF-8
                titulo = titulo.encode('utf-8', 'replace').decode('utf-8')
                link = link.encode('utf-8', 'replace').decode('utf-8')
                data_extracao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dados.append((titulo, link, data_extracao))
        except Exception as e:
            print(f"Erro ao extrair dados da notícia: {e}")
    
    return dados

def insert_data_to_db(dados):
    # Obtém a URL do banco de dados a partir da variável de ambiente
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    if not DATABASE_URL:
        print("Erro: A variável de ambiente DATABASE_URL não está definida.")
        return
    
    # Conecta ao banco PostgreSQL e insere os dados
    try:
        conexao = psycopg2.connect(DATABASE_URL)
        cursor = conexao.cursor()
        
        # Insere os dados coletados
        for titulo, link, data_extracao in dados:
            cursor.execute("INSERT INTO noticias (titulo, link, data_extracao) VALUES (%s, %s, %s)", (titulo, link, data_extracao))
        
        conexao.commit()
        cursor.close()
        conexao.close()
        
        print("Dados inseridos no banco com sucesso!")
    except Exception as e:
        print(f"Erro ao inserir no banco: {e}")

def main():
    nav = setup_webdriver()
    try:
        dados = scrape_data(nav)
    except Exception as e:
        print(f"Erro durante a extração de dados: {e}")
    finally:
        nav.quit()
    
    if dados:
        print(tabulate(dados, headers=["Título", "Link", "Data de Extração"], tablefmt="grid"))
        insert_data_to_db(dados)

if __name__ == "__main__":
    main()