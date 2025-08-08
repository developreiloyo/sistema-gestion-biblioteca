# Usar una imagen base oficial de Python
FROM python:3.11-slim

# Configurar el entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear un directorio de trabajo
WORKDIR /app

# Copiar requirements.txt
COPY requirements.txt /app/requirements.txt

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY . /app/

# ⚠️ CORREGIDO: Usa el módulo real de settings
ENV DJANGO_SETTINGS_MODULE=sgb.settings

# Ejecutar collectstatic
RUN python manage.py collectstatic --noinput

# Exponer el puerto
EXPOSE 8000

# Comando para iniciar el servidor
CMD ["gunicorn", "sgb.wsgi:application", "--bind", "0.0.0.0:8000"]
