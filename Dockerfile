# Usa una imagen oficial de Python
FROM python:3.9-slim

# Establece una variable de entorno para asegurarte de que la salida de Python se envía directamente al terminal
ENV PYTHONUNBUFFERED=1

# Crea y configura el directorio para la aplicación
WORKDIR /app

# Copia el archivo de requisitos y luego instala los requisitos
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el contenido del directorio actual (tu aplicación) al contenedor
COPY . /app

# Comando para ejecutar la aplicación usando Uvicorn cuando el contenedor se inicie
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
