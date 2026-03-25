# 1. Imagen base de Python
FROM python:3.10-slim

# 2. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar archivos de requisitos e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar el resto del código
COPY . .

# 5. Comando para ejecutar la app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]