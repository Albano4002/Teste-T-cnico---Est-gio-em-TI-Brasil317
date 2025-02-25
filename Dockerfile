# Imagem do Python 3.12
FROM python:3.12

# Dependências necessárias para o ChromeDriver
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libxrender1 \
    libxtst6 \
    libglib2.0-0 \
    libgtk-3-0 \
    libpango1.0-0 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libgbm1 \
    libnspr4 \
    libxss1 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Baixar e instalar o Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos para dentro do container
COPY scraper.py .
COPY schema.sql .
COPY requirements.txt .

# Instala as dependências
RUN pip install -r requirements.txt

# Define o comando para rodar o scraper quando o container iniciar
CMD ["python", "scraper.py"]
