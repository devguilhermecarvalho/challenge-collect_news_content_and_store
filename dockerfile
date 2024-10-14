FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expor a porta onde o FastAPI será executado
EXPOSE 8000

# Comando para rodar o servidor da aplicação FastAPI
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]