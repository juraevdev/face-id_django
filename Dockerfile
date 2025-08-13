# Python bazaviy image
FROM python:3.11-slim

# Ishchi papkani o‘rnatish
WORKDIR /app

# Sistem paketlari (dlib uchun)
RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    && rm -rf /var/lib/apt/lists/*

# Requirements yuklash
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . .

# Django uchun environment sozlamalari
ENV DJANGO_SETTINGS_MODULE=config.settings

# Collect static (agar kerak bo‘lsa)
# RUN python manage.py collectstatic --noinput

# Port
EXPOSE 8000

# Run server
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
