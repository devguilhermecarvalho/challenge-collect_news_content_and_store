FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["bash", "-c", "python main.py && uvicorn api.main:app --host 0.0.0.0 --port 8000"]