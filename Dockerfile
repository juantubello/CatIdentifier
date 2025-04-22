FROM python:3.11-slim

# Instalar dependencias del sistema para opencv
RUN apt-get update && apt-get install -y \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY identificador.py .

EXPOSE 5000

CMD ["uvicorn", "identificador:app", "--host", "0.0.0.0", "--port", "5000"]
