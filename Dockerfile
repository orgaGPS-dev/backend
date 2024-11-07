# Basis-Image
FROM python:3.9-slim

# Arbeitsverzeichnis festlegen
WORKDIR /usr/src/app

# Systemabhängigkeiten installieren
RUN apt-get update && apt-get install -y \
    python3-dev \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install -r requirements.txt

# Anwendungscode kopieren
COPY . .

# Statische Dateien sammeln
RUN python manage.py collectstatic --noinput

# Gunicorn installieren
RUN pip install gunicorn

# Standard-Port für die Anwendung
EXPOSE 8000

# Startbefehl für Gunicorn
CMD ["gunicorn",  "--workers", "3", "--bind", "0.0.0.0:8000", "orgagps.wsgi:application"]
