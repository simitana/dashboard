FROM python:3.11-slim

WORKDIR /app

# Instalar dependências
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar arquivos da aplicação
COPY backend/ ./backend/
COPY public/ ./public/
COPY modules/ ./modules/

# Expor porta
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "backend/app.py"]
