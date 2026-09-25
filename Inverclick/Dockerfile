# Usar imagen oficial de Python en versión slim
FROM python:3.11-slim

# Evitar la creación de archivos .pyc y asegurar salida directa en logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establecer directorio de trabajo en el contenedor
WORKDIR /app

# Instalar utilidades básicas del sistema operativo
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias de Python
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copiar el código fuente del proyecto
COPY . /app/

# Exponer puerto 8000 para la API
EXPOSE 8000

# Comando por defecto para iniciar el servidor de desarrollo/producción
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
